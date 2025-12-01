#!/usr/bin/env python3
import argparse, json, os, sys
from datetime import datetime
from typing import Dict, List
from difflib import SequenceMatcher

try:
    from analyze_project import analyze_project
    from extract_commit_changes import extract_commit_changes
except Exception as e:
    print(f"[ERROR] Import failed: {e}", file=sys.stderr)
    raise

VERSION = "3.0"


def normalize(path: str) -> str:
    if not path:
        return ""
    return os.path.normpath(path).replace("\\", "/")


def build_index(code_data: List[Dict]) -> Dict[str, Dict]:
    idx = {}
    if not code_data:
        return idx
    for entry in code_data:
        path = normalize(entry.get("file") or entry.get("path") or entry.get("filename"))
        if not path:
            continue
        funcs = entry.get("functions") or []
        clean_funcs = []
        for fn in funcs:
            name = fn.get("name") if isinstance(fn, dict) else fn
            if name:
                clean_funcs.append({"name": name, **(fn if isinstance(fn, dict) else {})})
        idx[path] = {
            "path": path,
            "functions": clean_funcs,
            "classes": entry.get("classes") or [],
            "file_history": []
        }
    return idx


def sim(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def map_changes(file_index: Dict[str, Dict], commits: List[Dict],
                mode="strict", fuzzy_threshold=0.75, max_commits=None):
    if not commits:
        return []
    if max_commits:
        commits = commits[:max_commits]

    file_to_funcs = {
        fpath: [fn["name"] for fn in fobj["functions"]]
        for fpath, fobj in file_index.items()
    }

    out = []
    for c in commits:
        changed = c.get("changed_functions") or []
        mapping = []

        if changed and file_to_funcs:
            for fpath, fnames in file_to_funcs.items():
                matched = []
                for ch in changed:
                    if mode == "strict":
                        if ch in fnames:
                            matched.append(ch)
                    else:
                        best = 0
                        best_name = None
                        for fn in fnames:
                            sc = sim(ch, fn)
                            if sc > best:
                                best = sc
                                best_name = fn
                        if best >= fuzzy_threshold:
                            matched.append(best_name)

                matched = sorted(set(matched))
                if matched:
                    mapping.append({
                        "file": fpath,
                        "functions": matched,
                        "insertions": c.get("insertions", 0),
                        "deletions": c.get("deletions", 0)
                    })

        out.append({
            "commit_id": c.get("commit"),
            "message": c.get("message"),
            "date": c.get("date"),
            "changed_functions": sorted(set(changed)),
            "per_file_function_changes": mapping
        })

    return out


def attach(file_index: Dict[str, Dict], mapped_commits: List[Dict]):
    for commit in mapped_commits:
        cid, msg, date = commit["commit_id"], commit["message"], commit["date"]
        for ch in commit["per_file_function_changes"]:
            fpath = normalize(ch["file"])
            if fpath not in file_index:
                continue
            file_index[fpath]["file_history"].append({
                "commit": cid, "message": msg, "date": date,
                "insertions": ch.get("insertions", 0),
                "deletions": ch.get("deletions", 0)
            })
            for fn in ch["functions"]:
                for fobj in file_index[fpath]["functions"]:
                    if fobj["name"] == fn:
                        fobj.setdefault("changed_in_commits", []).append({
                            "commit": cid, "message": msg, "date": date
                        })


def build(project_path=".", mode="strict", fuzzy_threshold=0.75, max_commits=None):
    project_path = os.path.abspath(project_path)
    print(f"[INFO] Combining data for {project_path}")

    try:
        code = analyze_project(project_path) or []
    except Exception:
        code = []

    try:
        commits = extract_commit_changes(project_path) or []
    except Exception:
        commits = []

    file_index = build_index(code)
    mapped = map_changes(file_index, commits, mode, fuzzy_threshold, max_commits)
    attach(file_index, mapped)

    return {
        "project": {
            "name": os.path.basename(project_path),
            "root_path": project_path
        },
        "files": sorted(file_index.values(), key=lambda x: x["path"]),
        "commit_index": [
            {"commit": c.get("commit"), "message": c.get("message"), "date": c.get("date")}
            for c in commits
        ],
        "summary": {
            "num_files": len(file_index),
            "num_functions": sum(len(f["functions"]) for f in file_index.values()),
            "num_commits": len(commits)
        },
        "metadata": {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "version": VERSION,
            "match_mode": mode,
            "fuzzy_threshold": fuzzy_threshold if mode == "fuzzy" else None,
            "max_commits": max_commits
        }
    }


def write_json(data: Dict, out_path: str):
    d = os.path.dirname(out_path)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[OK] Wrote {out_path}")


def parse():
    p = argparse.ArgumentParser()
    p.add_argument("--project", "-p", default=".")
    p.add_argument("--out", "-o", default="combined_data.json")
    p.add_argument("--match", "-m", choices=["strict", "fuzzy"], default="strict")
    p.add_argument("--fuzzy-threshold", type=float, default=0.75)
    p.add_argument("--max-commits", type=int, default=None)
    return p.parse_args()


def main():
    args = parse()
    data = build(
        project_path=args.project,
        mode=args.match,
        fuzzy_threshold=args.fuzzy_threshold,
        max_commits=args.max_commits,
    )
    write_json(data, args.out)


if __name__ == "__main__":
    main()
