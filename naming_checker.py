# naming_checker.py

import ast
import os
import re
import json

SNAKE_CASE = re.compile(r'^[a-z_][a-z0-9_]*$')
PASCAL_CASE = re.compile(r'^[A-Z][a-zA-Z0-9]+$')
UPPER_CASE = re.compile(r'^[A-Z_][A-Z0-9_]*$')

def get_python_files(folder):
    for root, _, files in os.walk(folder):
        for f in files:
            if f.endswith(".py"):
                yield os.path.join(root, f)

def analyze_names(tree):
    issues = {
        "bad_functions": [],
        "bad_variables": [],
        "bad_classes": [],
        "bad_constants": []
    }

    # FUNCTIONS
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if not SNAKE_CASE.match(node.name):
                issues["bad_functions"].append(node.name)

        # VARIABLES (assignments)
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    name = target.id
                    if name.isupper():  # constant
                        if not UPPER_CASE.match(name):
                            issues["bad_constants"].append(name)
                    else:  # normal variable
                        if not SNAKE_CASE.match(name):
                            issues["bad_variables"].append(name)

        # ARGUMENTS
        if isinstance(node, ast.FunctionDef):
            for arg in node.args.args:
                if not SNAKE_CASE.match(arg.arg):
                    issues["bad_variables"].append(arg.arg)

        # CLASSES
        if isinstance(node, ast.ClassDef):
            if not PASCAL_CASE.match(node.name):
                issues["bad_classes"].append(node.name)

    return issues

def analyze_folder(folder):
    report = {}

    for file_path in get_python_files(folder):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                tree = ast.parse(f.read())
            except:
                continue  # skip broken files

        report[file_path] = analyze_names(tree)

    return report

if __name__ == "__main__":
    result = analyze_folder(".")
    with open("naming_report.json", "w") as f:
        json.dump(result, f, indent=4)

    print("Wrote naming_report.json")
