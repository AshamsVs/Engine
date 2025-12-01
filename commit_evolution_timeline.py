import json
import os


def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def build_commit_evolution_timeline():
    # Load combined data (has file/function mapping)
    combined = load_json("combined_data_v3.json")
    files = combined.get("files", [])
    commits = combined.get("commit_index", [])

    # Build function -> file lookup
    func_to_file = {}
    for f in files:
        fpath = f.get("path")
        for fn in f.get("functions", []):
            name = fn.get("name")
            if name:
                func_to_file[name] = fpath

    timeline = {}

    # Iterate through commits newest → oldest
    for c in commits:
        cid = c.get("commit", "")[:7]
        date = c.get("date")
        msg = c.get("message")
        changed_functions = c.get("changed_functions", [])

        for fn in changed_functions:
            file_path = func_to_file.get(fn)
            if not file_path:
                continue  # function not mapped to any file

            timeline.setdefault(file_path, []).append({
                "commit": cid,
                "date": date,
                "message": msg,
                "function": fn
            })

    return timeline


if __name__ == "__main__":
    timeline = build_commit_evolution_timeline()
    with open("commit_evolution_timeline.json", "w", encoding="utf-8") as f:
        json.dump(timeline, f, indent=2)
    print("Wrote commit_evolution_timeline.json")
