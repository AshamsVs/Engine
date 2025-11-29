# unused_function_detector.py
import ast
import os
import json

def get_python_files(folder="."):
    for root, dirs, files in os.walk(folder):
        for f in files:
            if f.endswith(".py"):
                yield os.path.join(root, f)


# ------------------------------------------
# Extract defined functions
# ------------------------------------------
def extract_defined_functions(tree):
    funcs = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            funcs.append(node.name)
    return funcs


# ------------------------------------------
# Extract function calls
# ------------------------------------------
def extract_called_functions(tree):
    calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                calls.append(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                calls.append(node.func.attr)
    return calls


# ------------------------------------------
# Filter out special/ignored functions
# ------------------------------------------
def is_ignored(func_name):
    if func_name.startswith("_"):  # private or dunder
        return True
    if func_name.startswith("__") and func_name.endswith("__"):
        return True
    return False


# ------------------------------------------
# Main detector
# ------------------------------------------
def detect_unused_functions():
    defined_all = {}
    called_all = []

    for file in get_python_files("."):
        try:
            src = open(file, "r", encoding="utf-8").read()
            tree = ast.parse(src)
        except Exception:
            continue

        # list of defined functions in this file
        defs = extract_defined_functions(tree)
        defined_all[file] = defs

        # add all calls found
        calls = extract_called_functions(tree)
        called_all.extend(calls)

    # Now check unused
    unused = {}

    for file, funcs in defined_all.items():
        for f in funcs:
            if not is_ignored(f) and f not in called_all:
                unused.setdefault(file, []).append(f)

    # Save json
    with open("unused_functions.json", "w", encoding="utf-8") as f:
        json.dump(unused, f, indent=2)

    # Save md readable format
    with open("unused_functions.md", "w", encoding="utf-8") as f:
        for file, funcs in unused.items():
            f.write(f"## File: {file}\n")
            if funcs:
                for fn in funcs:
                    f.write(f"- `{fn}` might be unused.\n")
            else:
                f.write("No unused functions.\n")
            f.write("\n")

    print("Wrote unused_functions.json and unused_functions.md")
    return unused


if __name__ == "__main__":
    detect_unused_functions()
