
import json, os

def norm(p):
    return os.path.basename(p.replace("\\", "/"))

def classify(s):
    s = s.lower()
    if "was added" in s:
        return "added"
    if "refactor" in s:
        return "refactored"
    return "modified"

def build():
    if not os.path.exists("diff_explanations.json"):
        return {}

    data = json.load(open("diff_explanations.json"))
    out = {}

    for e in data:
        f = norm(e.get("file", ""))
        fn = e.get("function")
        c = e.get("commit")

        if not f or not fn or not c:
            continue

        out.setdefault(f, {})
        out[f].setdefault(fn, [])
        out[f][fn].append({
            "commit": c[:7],
            "type": classify(e.get("summary", ""))
        })
    return out

def save():
    t = build()
    json.dump(t, open("function_timeline.json", "w"), indent=2)
    print("[OK] wrote function_timeline.json")

if __name__ == "__main__":
    save()
