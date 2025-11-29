# duplicate_detector.py

import ast
import os
import json
import hashlib

def get_python_files(folder):
    for root, _, files in os.walk(folder):
        for f in files:
            if f.endswith(".py"):
                yield os.path.join(root, f)

def normalize_body(body_list):
    """Convert function body (list of AST nodes) into a normalized hashable form."""
    # Wrap body in an AST Module so ast.dump() can process it
    module = ast.Module(body=body_list, type_ignores=[])
    return ast.dump(module, annotate_fields=False, include_attributes=False)

def analyze_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read())
        except:
            return []

    functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):

            body_str = normalize_body(node.body)
            body_hash = hashlib.md5(body_str.encode()).hexdigest()

            functions.append({
                "file": file_path,
                "name": node.name,
                "hash": body_hash
            })

    return functions

def detect_duplicates():
    all_functions = []

    for f in get_python_files("."):
        all_functions.extend(analyze_file(f))

    # group by hash
    hash_map = {}
    for fn in all_functions:
        hash_map.setdefault(fn["hash"], []).append(fn)

    duplicates = {h: fns for h, fns in hash_map.items() if len(fns) > 1}

    with open("duplicate_report.json", "w") as f:
        json.dump(duplicates, f, indent=4)

    print("Wrote duplicate_report.json")

if __name__ == "__main__":
    detect_duplicates()
