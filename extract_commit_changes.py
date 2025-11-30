# extract_commit_changes.py
import json
from git import Repo
from detect_changed_functions import detect_changed_functions


def extract_commit_changes(project_path):
    repo = Repo(project_path)
    all_changes = []

    # iterate through commits newest → oldest
    for commit in repo.iter_commits():

        diff_text = repo.git.show(commit.hexsha, color=False)
        changed_funcs = []

        # iterate through modified files in the commit
        for file in commit.stats.files.keys():
            if file.endswith(".py"):
                try:
                    funcs = detect_changed_functions(file, diff_text)
                    changed_funcs.extend(funcs)
                except Exception:
                    pass

        changed_funcs = list(set(changed_funcs))  # remove duplicates

        all_changes.append({
            "commit": commit.hexsha,
            "message": commit.message.strip(),
            "date": commit.committed_datetime.isoformat(),   # <<< ADDED
            "changed_functions": changed_funcs
        })

    return all_changes


if __name__ == "__main__":
    project_path = "."
    data = extract_commit_changes(project_path)

    print(json.dumps(data, indent=2))

    with open("commit_changes.json", "w") as f:
        json.dump(data, f, indent=2)

    print("\nWrote commit_changes.json")
