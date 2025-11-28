import json
from git import Repo
from detect_changed_functions import detect_changed_functions

def extract_commit_changes():
    repo = Repo(".")
    all_changes = []

    for commit in repo.iter_commits():
        diff_text = repo.git.show(commit.hexsha, color=False)

        # detect functions changed IN ALL python files
        # you already built detect_changed_functions(file, diff)
        changed_funcs = []

        for file in commit.stats.files.keys():
            if file.endswith(".py"):
                try:
                    funcs = detect_changed_functions(file, diff_text)
                    changed_funcs.extend(funcs)
                except Exception:
                    pass

        # remove duplicates
        changed_funcs = list(set(changed_funcs))

        all_changes.append({
            "commit": commit.hexsha,
            "message": commit.message.strip(),
            "changed_functions": changed_funcs
        })

    return all_changes


if __name__ == "__main__":
    data = extract_commit_changes()

    # print to console
    print(json.dumps(data, indent=2))

    # save file for CIA
    with open("commit_changes.json", "w") as f:
        json.dump(data, f, indent=2)

    print("\nWrote commit_changes.json")
