
import argparse
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any
from difflib import SequenceMatcher

# local imports
try:
    from analyze_project import analyze_project
    from extract_commit_changes import extract_commit_changes
except Exception as e:
    print(f"[ERROR] Import failed: {e}", file=sys.stderr)
    # re-raise to fail loud in CI if modules missing
    raise

VERSION = "3.2"


# ---------- helpers ----------
def normalize_path(path: str) -> str:
    if not path:
        return ""
    return os.path.normpath(path).replace("\\", "/")


def safe_load_json(path: str) -> Any:
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except Exception as e:
            print(f"[WARN] Failed to load JSON '{path}': {e}")
            return None
    return None


def safe_load_text(path: str) -> str:
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as fh:
                return fh.read()
        except Exception as e:
            print(f"[WARN] Failed to load text '{path}': {e}")
            return ""
    return ""


# ---------- build index ----------
def build_index_by_file(code_data: List[Dict]) -> Dict[str, Dict]:
    index = {}
    for entry in (code_data or []):
        raw_path = entry.get("file") or entry.get("path") or entry.get("filename") or ""
        path = normalize_path(raw_path)
        if not path:
            continue
        functions = entry.get("functions") or []
        classes = entry.get("classes") or []
        normalized_funcs = []
        for fn in functions:
            if isinstance(fn, dict):
                name = fn.get("name")
                if name:
                    normalized_funcs.append(fn)
            else:
                normalized_funcs.append({"name": fn})
        index[path] = {
            "path": path,
            "functions": normalized_funcs,
            "classes": classes,
            "file_history": []
        }
    return index


# ---------- fuzzy matcher ----------
def fuzzy_match(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


# ---------- map commit changes to files ----------
def map_commit_changes_to_files(
        file_index: Dict[str, Dict],
        commit_changes: List[Dict],
        match_mode: str = "strict",
        fuzzy_threshold: float = 0.75,
        max_commits: int | None = None):
    per_commit = []
    file_to_funcs = {
        fpath: [fn.get("name") for fn in fobj.get("functions", []) if fn.get("name")]
        for fpath, fobj in file_index.items()
    }
    commits = commit_changes or []
    if max_commits is not None:
        commits = commits[:max_commits]
    for c in commits:
        changed = c.get("changed_functions", []) or []
        mapping = []
        for fpath, func_list in file_to_funcs.items():
            matched = []
            for fn in changed:
                if match_mode == "strict":
                    if fn in func_list:
                        matched.append(fn)
                elif match_mode == "fuzzy":
                    best_score = 0.0
                    best = None
                    for real_fn in func_list:
                        score = fuzzy_match(fn, real_fn)
                        if score > best_score:
                            best_score = score
                            best = real_fn
                    if best_score >= fuzzy_threshold and best:
                        matched.append(best)
                else:
                    if fn in func_list:
                        matched.append(fn)
            matched = sorted(set(matched))
            if matched:
                mapping.append({
                    "file": fpath,
                    "functions": matched,
                    "insertions": c.get("insertions", 0),
                    "deletions": c.get("deletions", 0)
                })
        per_commit.append({
            "commit_id": c.get("commit"),
            "message": c.get("message"),
            "date": c.get("date"),
            "changed_functions": sorted(set(changed)),
            "per_file_function_changes": mapping
        })
    return per_commit


# ---------- attach history ----------
def attach_commit_changes(file_index: Dict[str, Dict], per_commit: List[Dict]) -> None:
    for commit in per_commit:
        cid = commit.get("commit_id")
        msg = commit.get("message")
        date = commit.get("date")
        for change in commit.get("per_file_function_changes", []):
            fpath = normalize_path(change.get("file", ""))
            funcs = change.get("functions", [])
            if fpath not in file_index:
                # defensive: the file was not found in static analysis
                continue
            file_index[fpath]["file_history"].append({
                "commit": cid,
                "message": msg,
                "date": date,
                "insertions": change.get("insertions", 0),
                "deletions": change.get("deletions", 0)
            })
            for fn in funcs:
                for func_obj in file_index[fpath].get("functions", []):
                    if func_obj.get("name") == fn:
                        func_obj.setdefault("changed_in_commits", []).append({
                            "commit": cid,
                            "message": msg,
                            "date": date
                        })


# ---------- build commit evolution timeline ----------
def build_commit_evolution_timeline(file_index: Dict[str, Dict], commit_changes: List[Dict]) -> Dict[str, List[Dict]]:
    func_to_file = {}
    for fpath, fdata in file_index.items():
        for fn in fdata.get("functions", []):
            name = fn.get("name")
            if name:
                func_to_file[name] = fpath
    timeline = {}
    for c in commit_changes or []:
        cid = (c.get("commit") or "")[:7]
        date = c.get("date")
        msg = c.get("message")
        changed = c.get("changed_functions", []) or []
        for fn in changed:
            fpath = func_to_file.get(fn)
            if not fpath:
                continue
            timeline.setdefault(fpath, []).append({
                "commit": cid,
                "date": date,
                "message": msg,
                "function": fn
            })
    return timeline


# ---------- main builder ----------
def build_combined(project_path: str = ".",
                   match_mode: str = "strict",
                   fuzzy_threshold: float = 0.75,
                   max_commits: int | None = None) -> Dict[str, Any]:
    project_path = os.path.abspath(project_path)
    print(f"[INFO] Building combined_data for: {project_path}")

    # run static analyzer
    try:
        code_data = analyze_project(project_path) or []
    except Exception as e:
        print(f"[WARN] analyze_project failed: {e}")
        code_data = []

    # load commit changes (use extractor if available)
    try:
        commit_changes = extract_commit_changes(project_path) or []
    except Exception as e:
        print(f"[WARN] extract_commit_changes failed: {e}")
        commit_changes = []

    # index files
    file_index = build_index_by_file(code_data)

    # map commits -> files/functions
    per_commit_transformed = map_commit_changes_to_files(
        file_index,
        commit_changes,
        match_mode=match_mode,
        fuzzy_threshold=fuzzy_threshold,
        max_commits=max_commits
    )
        # map commits -> files/functions
    per_commit_transformed = map_commit_changes_to_files(
        file_index,
        commit_changes,
        match_mode=match_mode,
        fuzzy_threshold=fuzzy_threshold,
        max_commits=max_commits
    )

    # ------------------------------------------
    # NEW: Build dependency graphs (file + call)
    # ------------------------------------------
    try:
        from dependency_graph import build_dependency_data
        from diagram_generator import (
            generate_file_dependency_mermaid,
            generate_function_dependency_mermaid
        )
    except Exception as e:
        print("[WARN] Could not import dependency graph modules:", e)
        deps = {"files": {}, "functions": {}}
    else:
        deps = build_dependency_data(project_path)

    # Generate Mermaid diagrams
    try:
        file_mermaid = generate_file_dependency_mermaid(deps["files"])
        func_mermaid = generate_function_dependency_mermaid(deps["functions"])
    except Exception as e:
        print("[WARN] Mermaid graph generation failed:", e)
        file_mermaid = "flowchart TD;\nA[Graph unavailable]"
        func_mermaid = "flowchart TD;\nA[Graph unavailable]"


    # attach history
    attach_commit_changes(file_index, per_commit_transformed)

    # build evolution timeline (per-file)
    evolution_timeline = build_commit_evolution_timeline(file_index, commit_changes)

    # --------------------
    # Load auxiliary JSON reports (safe)
    # --------------------
    dependency_data = safe_load_json("dependency_data.json") or {}
    diff_explanations = safe_load_json("diff_explanations.json") or []
    quality_issues = safe_load_json("quality_report.json") or {}
    naming_issues = safe_load_json("naming_report.json") or {}
    unused_functions = safe_load_json("unused_functions.json") or []
    duplicate_functions = safe_load_json("duplicate_report.json") or {}
    docstring_suggestions = safe_load_json("docstring_suggestions.json") or []
    impact_report = safe_load_json("impact_report.json") or {}
    combined_v2 = safe_load_json("combined_data_v2.json") or {}
    report_json = safe_load_json("report.json")  # optional

    # load mermaid diagrams (if present)
    file_dependency_graph = safe_load_text("file_dependencies.mmd")
    function_dependency_graph = safe_load_text("function_dependencies.mmd")

    # --------------------
    # Build final combined object (schema friendly to template)
    # --------------------
    combined = {
        # metadata & basic project info
        "metadata": {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "version": VERSION,
            "project_root": project_path,
            "project_name": os.path.basename(project_path),
            "match_mode": match_mode,
            "fuzzy_threshold": fuzzy_threshold if match_mode == "fuzzy" else None,
            "max_commits": max_commits
        },

        # existing analysis + computed indices
        "project_structure": safe_load_json("project_data.json") or {},   # optional
        "dependencies": dependency_data,
        "commit_history": commit_changes,
        "diff_explanations": diff_explanations,
        "quality_issues": quality_issues,
        "naming_issues": naming_issues,
        "unused_functions": unused_functions,
        "duplicate_functions": duplicate_functions,
        "docstring_suggestions": docstring_suggestions,
        "evolution_timeline": evolution_timeline,
        "impact_report": impact_report,

        # backward compatibility
        "combined_v2": combined_v2,
        "report": report_json or {},

        # computed runtime artifacts
        "files": sorted(list(file_index.values()), key=lambda x: x.get("path", "")),
        "summary": {
            "num_files": len(file_index),
            "num_functions": sum(len(f.get("functions", [])) for f in file_index.values()),
            "num_commits": len(commit_changes or [])
        },

        # NEW: Mermaid diagrams (generated earlier)
        "file_dependency_graph": file_mermaid,
        "function_dependency_graph": func_mermaid
    }

    return combined



# ---------- write helper ----------
def write_json_safe(obj: Dict[str, Any], out_path: str) -> None:
    out_dir = os.path.dirname(out_path) or "."
    os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2, ensure_ascii=False)
    print(f"[OK] Wrote combined JSON → {out_path}")


# ---------- CLI ----------
def parse_args():
    p = argparse.ArgumentParser(prog="combine_data_v3.py")
    p.add_argument("--project", "-p", default=".")
    p.add_argument("--out", "-o", default="combined_data_v3.json")
    p.add_argument("--match", "-m", choices=["strict", "fuzzy"], default="strict")
    p.add_argument("--fuzzy-threshold", type=float, default=0.75)
    p.add_argument("--max-commits", type=int, default=None)
    return p.parse_args()


def main():
    args = parse_args()
    combined = build_combined(
        project_path=args.project,
        match_mode=args.match,
        fuzzy_threshold=args.fuzzy_threshold,
        max_commits=args.max_commits
    )
    write_json_safe(combined, args.out)


if __name__ == "__main__":
    main()
