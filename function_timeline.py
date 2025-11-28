import json

def load_commit_changes():
    with open("commit_changes.json", "r") as f:
        return json.load(f)

def build_timeline():
    commits = load_commit_changes()

    # Reverse order → oldest commit first
    commits = list(reversed(commits))

    timeline = {}

    for entry in commits:
        commit_id = entry["commit"][:7]  # short hash
        message = entry["message"]
        changed_funcs = entry["changed_functions"]

        for func in changed_funcs:
            timeline.setdefault(func, [])
            timeline[func].append({
                "commit": commit_id,
                "message": message
            })

    return timeline

if __name__ == "__main__":
    timeline = build_timeline()
    print(json.dumps(timeline, indent=2))

    with open("function_timeline.json", "w") as f:
        json.dump(timeline, f, indent=2)

    print("\nWrote function_timeline.json")
