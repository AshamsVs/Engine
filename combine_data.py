# combine_data.py
import json
import os
from datetime import datetime
from analyze_project import analyze_project
from extract_commit_changes import extract_commit_changes

def build_index_by_file(code_data):
    """Turn analyze_project output into a dict keyed by file path for easy merging."""
    index = {}
    for f in code_data:
        # normalize path
        path = os.path.normpath(f["file"])
        index[path] = {
            "path": path,
            "functions": f.get("functions", []),
            "classes": f.get("classes", []),
            "file_history": []
        }
    return index

def attach_commit_changes(file_index, commit_changes):
    """
    commit_changes is a list of commits with changed_functions and message/date info
    We attach commits to file entries and to the specific functions inside those files.
    """
    for commit in commit_changes:
        cid = commit["commit_id"]
        msg = commit["message"]
        date = commit["date"].isoformat() if hasattr(commit["date"], "isoformat") else str(commit["date"])
        files_changed = commit.get("files_changed", [])  # optional; our extract may not populate this
        # If your extract_commit_changes didn't include files_changed, we still have changed_functions per file via earlier logic
        for fc in commit.get("file_changes", []):  # prefer file_changes if present
            path = os.path.normpath(fc.get("file_path"))
            if path in file_index:
                file_index[path]["file_history"].append({
                    "commit": cid, "message": msg, "date": date,
                    "insertions": fc.get("insertions", 0), "deletions": fc.get("deletions", 0)
                })

        # Also add commit info to functions listed in changed_functions
        for change in commit.get("per_file_function_changes", []):
            # change example: {"file": "demo.py", "functions": ["greet","farewell"]}
            fpath = os.path.normpath(change["file"])
            funcs = change.get("functions", [])
            if fpath in file_index:
                # attach to file history (if not already)
                file_index[fpath]["file_history"].append({
                    "commit": cid, "message": msg, "date": date,
                    "insertions": change.get("insertions", 0), "deletions": change.get("deletions", 0)
                })
                # attach to functions
                for fn in funcs:
                    for func_obj in file_index[fpath]["functions"]:
                        if func_obj["name"] == fn:
                            func_obj.setdefault("changed_in_commits", []).append({
                                "commit": cid, "message": msg, "date": date
                            })

def combine(project_path="."):
    # Phase 1
    code_data = analyze_project(project_path)

    # Phase 2: This function expects extract_commit_changes to return a list of commits
    # with keys: commit_id, message, date, and ideally per-file function change detail.
    commit_changes = extract_commit_changes(project_path, os.path.join(project_path, "demo.py"))

    file_index = build_index_by_file(code_data)

    # simple mapping: try to map commit_changes into a per-file structure
    # The extract_commit_changes we wrote earlier returned commits with changed_functions and message/date.
    # We'll transform that into the per_file_function_changes format to simplify merging.
    per_commit_transformed = []
    for c in commit_changes:
        # For each commit, we need to find which file(s) each changed function belongs to.
        mapping = []
        for fpath, file_obj in file_index.items():
            func_names = [fn["name"] for fn in file_obj.get("functions", [])]
            changed_here = [fn for fn in c.get("changed_functions", []) if fn in func_names]
            if changed_here:
                mapping.append({
                    "file": fpath,
                    "functions": changed_here,
                    "insertions": 0,
                    "deletions": 0
                })
        per_commit_transformed.append({
            "commit_id": c["commit_id"],
            "message": c["message"],
            "date": c["date"],
            "per_file_function_changes": mapping
        })

    # attach commit info into file_index and function entries
    attach_commit_changes(file_index, per_commit_transformed)

    # Build the final schema
    combined = {
        "project": {
            "name": os.path.basename(os.path.abspath(project_path)),
            "root_path": os.path.abspath(project_path)
        },
        "files": list(file_index.values()),
        "commit_index": [
            {"commit": c["commit_id"], "message": c["message"], "date": str(c["date"])}
            for c in commit_changes
        ],
        "summary": {
            "num_files": len(file_index),
            "num_functions": sum(len(f["functions"]) for f in file_index.values()),
            "num_commits": len(commit_changes)
        }
    }

    return combined

if __name__ == "__main__":
    combined = combine(".")
    out_path = "combined_data.json"
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(combined, fh, indent=2, default=str)
    print(f"Wrote {out_path}")
