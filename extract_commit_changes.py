# extract_commit_changes.py
import json
import os
from git import Repo, GitCommandError
from detect_changed_functions import detect_changed_functions


def extract_commit_changes(project_path):
    repo = Repo(project_path)
    all_changes = []

    # iterate through commits newest → oldest
    for commit in repo.iter_commits():

        # Try to get the commit show (diff + metadata). If not possible (shallow clone / missing objects),
        # fall back to empty diff_text but continue gracefully.
        try:
            diff_text = repo.git.show(commit.hexsha, color=False)
        except GitCommandError:
            diff_text = ""

        changed_funcs = []

        # Protect against commit.stats failing in shallow/detached states
        try:
            changed_files = list(commit.stats.files.keys())
        except GitCommandError:
            changed_files = []

        for file_rel in changed_files:
            # keep file relative path as reported by git
            if file_rel.endswith(".py"):
                # try to find the actual file on disk; if deleted/renamed it may not exist
                file_path = os.path.normpath(os.path.join(project_path, file_rel))
                if not os.path.exists(file_path):
                    # skip deleted/renamed files (no local source to analyze)
                    continue

                try:
                    funcs = detect_changed_functions(file_path, diff_text)
                    if funcs:
                        changed_funcs.extend(funcs)
                except Exception:
                    # don't crash on parser errors; skip this file
                    pass

        # dedupe and normalize
        changed_funcs = sorted(set(changed_funcs))

        all_changes.append({
            "commit": commit.hexsha,
            "message": commit.message.strip(),
            "date": commit.committed_datetime.isoformat(),
            "changed_functions": changed_funcs
        })

    return all_changes


if __name__ == "__main__":
    project_path = "."
    data = extract_commit_changes(project_path)

    print(json.dumps(data, indent=2))

    with open("commit_changes.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print("\nWrote commit_changes.json")
