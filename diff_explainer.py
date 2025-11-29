# diff_explainer.py
import re
import json
from git import Repo
from function_ranges import get_function_ranges
from parse_diff import get_changed_lines

repo = Repo(".")

def load_commit_changes(path="commit_changes.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_hunks(diff_text):
    """
    Returns a list of hunks. Each hunk is dict:
      {"old_start": int, "old_len": int, "new_start": int, "new_len": int,
       "lines": [ (type, text, new_line_no_or_None) ... ] }
    type is '+' or '-' or ' ' (context). new_line_no is the line number in the NEW file for '+' and ' ' lines.
    """
    hunks = []
    cur = None
    new_line = None

    for line in diff_text.splitlines():
        m = re.match(r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", line)
        if m:
            old_start = int(m.group(1))
            old_len = int(m.group(2)) if m.group(2) else 1
            new_start = int(m.group(3))
            new_len = int(m.group(4)) if m.group(4) else 1
            cur = {"old_start": old_start, "old_len": old_len, "new_start": new_start, "new_len": new_len, "lines": []}
            new_line = new_start
            hunks.append(cur)
            continue

        if cur is None:
            continue

        # line types
        if line.startswith("+") and not line.startswith("+++"):
            cur["lines"].append(("+", line[1:], new_line))
            new_line = None if new_line is None else new_line + 1
        elif line.startswith("-") and not line.startswith("---"):
            cur["lines"].append(("-", line[1:], None))
            # removed line does not advance new_line
        else:
            # context line (may be " " or other)
            text = line[1:] if line.startswith(" ") else line
            cur["lines"].append((" ", text, new_line))
            new_line = None if new_line is None else new_line + 1

    return hunks

def collect_added_removed_lines_in_func(hunks, func_start, func_end):
    """Return lists of added and removed lines (strings) that fall within function's new-file line range."""
    added = []
    removed = []
    for h in hunks:
        for typ, txt, new_ln in h["lines"]:
            # For '+' lines we have new_ln; for '-' lines we don't; but we approximate: if hunk new range overlaps function range, include removed lines too.
            if typ == "+" and new_ln is not None and func_start <= new_ln <= func_end:
                added.append(txt.strip())
            elif typ == "-" :
                # Approximate: include removed lines if the hunk's new range intersects function range
                # Check whether hunk's new_start .. new_start+new_len overlaps func range
                new_hunk_start = h["new_start"]
                new_hunk_end = h["new_start"] + (h["new_len"] if h["new_len"] else 1)
                if (new_hunk_start <= func_end and new_hunk_end >= func_start):
                    removed.append(txt.strip())
    return added, removed

def normalize_code_line(s):
    # lower and remove whitespace and punctuation for rough similarity
    return re.sub(r'[^0-9a-zA-Z]', '', s).lower()

def detect_punctuation_change(added, removed):
    # Find pairs of lines that are similar except punctuation differences
    for r in removed:
        for a in added:
            if normalize_code_line(r) == normalize_code_line(a) and r != a:
                return True, r, a
    return False, None, None

def detect_signature_change(added, removed, func_name):
    # look for "def func_name(" in added or removed lines
    for r in removed:
        if re.match(rf"\s*def\s+{re.escape(func_name)}\s*\(", r):
            for a in added:
                if re.match(rf"\s*def\s+{re.escape(func_name)}\s*\(", a) and r != a:
                    return True, r.strip(), a.strip()
    return False, None, None

def detect_docstring_change(added, removed):
    # detect presence of triple-quote lines added/removed
    added_doc = any(('"""' in x or "'''" in x) for x in added)
    removed_doc = any(('"""' in x or "'''" in x) for x in removed)
    if added_doc and not removed_doc:
        return "added"
    if removed_doc and not added_doc:
        return "removed"
    if added_doc and removed_doc:
        return "modified"
    return None

def detect_return_change(added, removed):
    # detect changes to return statements
    if any(l.strip().startswith("return ") for l in added) or any(l.strip().startswith("return ") for l in removed):
        return True
    return False

def detect_logic_change(added, removed):
    keywords = ("if ", "for ", "while ", "try:", "except", "elif ", "else:")
    if any(any(k in l for k in keywords) for l in added + removed):
        return True
    return False

def explain_changes_for_function(file_path, func_name, diff_text):
    hunks = extract_hunks(diff_text)
    # get function ranges for file
    try:
        ranges = get_function_ranges(file_path)
    except Exception:
        ranges = []

    func_range = None
    for f in ranges:
        if f["name"] == func_name:
            func_range = f
            break

    # if we cannot find range, fallback: search for def line in added/removed
    if not func_range:
        # try to still get added/removed lines from hunks for file-wide
        all_added = []
        all_removed = []
        for h in hunks:
            for typ, txt, new_ln in h["lines"]:
                if typ == "+":
                    all_added.append(txt.strip())
                elif typ == "-":
                    all_removed.append(txt.strip())
        added, removed = all_added, all_removed
    else:
        added, removed = collect_added_removed_lines_in_func(hunks, func_range["start"], func_range["end"])

    reasons = []

    # docstring
    doc_change = detect_docstring_change(added, removed)
    if doc_change == "added":
        reasons.append("A docstring was added to the function.")
    elif doc_change == "removed":
        reasons.append("The function docstring was removed.")
    elif doc_change == "modified":
        reasons.append("The function docstring was modified.")

    # signature change
    sig_changed, old_sig, new_sig = detect_signature_change(added, removed, func_name)
    if sig_changed:
        reasons.append(f"Function signature changed from `{old_sig}` to `{new_sig}`.")

    # punctuation/string formatting change
    punct, rline, aline = detect_punctuation_change(added, removed)
    if punct:
        reasons.append(f"String/formatting change detected. Example removed: `{rline}` → added: `{aline}`.")

    # return changes
    if detect_return_change(added, removed):
        reasons.append("Return statement or returned value was modified.")

    # logic changes
    if detect_logic_change(added, removed):
        reasons.append("Control-flow or logic was changed (if/for/while/try/except).")

    # added function definition?
    added_defs = [a for a in added if re.match(r"\s*def\s+\w+\s*\(", a)]
    removed_defs = [r for r in removed if re.match(r"\s*def\s+\w+\s*\(", r)]
    for a in added_defs:
        if func_name in a:
            reasons.append(f"Function `{func_name}` was added: `{a.strip()}`.")
    for r in removed_defs:
        if func_name in r:
            reasons.append(f"Function `{func_name}` was removed: `{r.strip()}`.")

    # fallback: if nothing specific found, provide a general summary
    if not reasons:
        # show a small sample of added/removed for human reading
        sample_added = added[:3]
        sample_removed = removed[:3]
        if sample_added or sample_removed:
            snippet = []
            if sample_removed:
                snippet.append("removed: " + " | ".join(f"`{s}`" for s in sample_removed))
            if sample_added:
                snippet.append("added: " + " | ".join(f"`{s}`" for s in sample_added))
            reasons.append("Small code edits detected (" + "; ".join(snippet) + ").")
        else:
            reasons.append("Changes detected but could not be classified by heuristics.")

    # Compose final explanation text using templates
    explanation = []
    explanation.append(f"**Function `{func_name}`** in `{file_path}`:")
    for r in reasons:
        explanation.append("- " + r)
    # Add short one-line summary
    summary = " ".join([re.sub(r'\s+', ' ', r) for r in reasons])
    return "\n".join(explanation), summary

def build_explanations(output_md="diff_explanations.md", output_json="diff_explanations.json"):
    commits = load_commit_changes()
    results = []

    for entry in commits:
        cid = entry["commit"]
        msg = entry.get("message", "")
        changed_funcs = entry.get("changed_functions", [])

        # get raw diff
        try:
            diff_text = repo.git.show(cid, color=False)
        except Exception as e:
            diff_text = ""

        per_commit = {"commit": cid, "message": msg, "functions": []}

        for func in changed_funcs:
            # We need file path for the function. Try to find file by scanning all python files for the function def.
            file_path = None
            for f in get_python_files("."):
                try:
                    ranges = get_function_ranges(f)
                    if any(r["name"] == func for r in ranges):
                        file_path = f
                        break
                except Exception:
                    continue

            if not file_path:
                file_path = "<unknown>"

            explain_md, summary = explain_changes_for_function(file_path, func, diff_text)

            per_commit["functions"].append({
                "function": func,
                "file": file_path,
                "explanation_md": explain_md,
                "summary": summary
            })
            results.append({
                "commit": cid,
                "function": func,
                "file": file_path,
                "summary": summary
            })

    # write outputs
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # produce a readable markdown
    with open(output_md, "w", encoding="utf-8") as f:
        for entry in results:
            f.write(f"### Commit {entry['commit']}\n")
            f.write(f"- Function: `{entry['function']}`\n")
            f.write(f"- File: `{entry['file']}`\n")
            f.write(f"- Summary: {entry['summary']}\n\n")

    return results

# helper to get python files (re-implemented to avoid circular import)
import os
def get_python_files(folder):
    py_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    return py_files

if __name__ == "__main__":
    res = build_explanations()
    print("Wrote diff_explanations.json and diff_explanations.md")
    # print a short human-friendly preview
    for r in res:
        print(f"Commit {r['commit']} | Function {r['function']} | File {r['file']}")
        print(" Summary:", r["summary"])
        print("-" * 60)
