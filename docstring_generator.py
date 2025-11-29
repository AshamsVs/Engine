# docstring_generator.py
import ast
import os
import json

def get_python_files(folder="."):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".py"):
                yield os.path.join(root, file)

def detect_return_type(node):
    """Return True if function has a return value."""
    for child in ast.walk(node):
        if isinstance(child, ast.Return) and child.value is not None:
            return True
    return False

def build_docstring(func_name, args, has_return):
    # simple English sentence
    description = f"{func_name.replace('_', ' ').capitalize()}."

    # parameters section
    params = ""
    if args:
        params += "Parameters:\n"
        for a in args:
            params += f"    {a} (any): Description.\n"

    # return section
    ret = ""
    if has_return:
        ret += "Returns:\n"
        ret += "    any: Description.\n"

    doc = f'""" {description}\n\n'
    if params:
        doc += params + "\n"
    if ret:
        doc += ret + "\n"
    doc += '"""'

    return doc

def analyze_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        src = f.read()

    tree = ast.parse(src)
    suggestions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            name = node.name
            args = [a.arg for a in node.args.args]
            doc = ast.get_docstring(node)

            # detect return
            has_return = detect_return_type(node)

            if doc is None or len(doc.strip()) < 5:
                new_doc = build_docstring(name, args, has_return)

                suggestions.append({
                    "file": file_path,
                    "function": name,
                    "arguments": args,
                    "has_return": has_return,
                    "existing_doc": doc,
                    "suggested_docstring": new_doc
                })

    return suggestions

def generate_docstrings():
    all_suggestions = []

    for file in get_python_files("."):
        suggestions = analyze_file(file)
        all_suggestions.extend(suggestions)

    # Save JSON
    with open("docstring_suggestions.json", "w", encoding="utf-8") as f:
        json.dump(all_suggestions, f, indent=2)

    # Save Markdown (readable)
    with open("docstring_suggestions.md", "w", encoding="utf-8") as f:
        for s in all_suggestions:
            f.write(f"### File: {s['file']}\n")
            f.write(f"**Function:** `{s['function']}`\n")
            f.write("Suggested Docstring:\n")
            f.write("```\n")
            f.write(s["suggested_docstring"])
            f.write("\n```\n\n")

    print("Wrote docstring_suggestions.json and docstring_suggestions.md")
    return all_suggestions

if __name__ == "__main__":
    generate_docstrings()
