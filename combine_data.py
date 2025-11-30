# combine_data.py
import json
import os
from analyze_project import analyze_project
from extract_commit_changes import extract_commit_changes


def build_index_by_file(code_data):
    """Turn analyze_project output into a dict keyed by file path for easy merging."""
    index = {}
    for f in code_data:
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
    Attach commit metadata into files and functions.
    commit_changes = transformed list:
    {
        commit_id, message, date, per_file_function_changes:[{file, functions}]
    }
    """
    for commit in commit_changes:
        cid = commit["commit_id"]
        msg = commit["message"]
        date = commit["date"]  # already ISO string

        # Preferred format: per_file_function_changes
        for change in commit.get("per_file_function_changes", []):
            fpath = os.path.normpath(change["file"])
            funcs = change.get("functions", [])

            if fpath in file_index:
                # attach to file history
                file_index[fpath]["file_history"].append({
                    "commit": cid,
                    "message": msg,
                    "date": date,
                    "insertions": change.get("insertions", 0),
                    "deletions": change.get("deletions", 0)
                })

                # attach to individual functions inside that file
                for fn in funcs:
                    for func_obj in file_index[fpath]["functions"]:
                        if func_obj["name"] == fn:
                            func_obj.setdefault("changed_in_commits", []).append({
                                "commit": cid,
                                "message": msg,
                                "date": date
                            })


def combine(project_path="."):
    # ---- Phase 1: Code analysis ----
    code_data = analyze_project(project_path)

    # ---- Phase 2: Git commit data ----
    commit_changes = extract_commit_changes(project_path)
    # commit_changes looks like:
    # { commit, message, date, changed_functions }

    # Build file index
    file_index = build_index_by_file(code_data)

    # Transform commit_changes → format usable by attach_commit_changes()
    per_commit_transformed = []
    for c in commit_changes:
        mapping = []

        for fpath, file_obj in file_index.items():
            func_names = [fn["name"] for fn in file_obj.get("functions", [])]

            # which changed functions belong to this file?
            changed_here = [
                fn for fn in c.get("changed_functions", [])
                if fn in func_names
            ]

            if changed_here:
                mapping.append({
                    "file": fpath,
                    "functions": changed_here,
                    "insertions": 0,
                    "deletions": 0
                })

        per_commit_transformed.append({
            "commit_id": c["commit"],
            "message": c["message"],
            "date": c["date"],                      # keep date
            "changed_functions": c["changed_functions"],
            "per_file_function_changes": mapping
        })

    # Attach commit info to files and functions
    attach_commit_changes(file_index, per_commit_transformed)

    # ---- Final Combined Output Format ----
    combined = {
        "project": {
            "name": os.path.basename(os.path.abspath(project_path)),
            "root_path": os.path.abspath(project_path)
        },

        "files": list(file_index.values()),

        "commit_index": [
            {"commit": c["commit"], "message": c["message"], "date": c["date"]}
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
        json.dump(combined, fh, indent=2)
    print(f"Wrote {out_path}")
