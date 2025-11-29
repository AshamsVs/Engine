# quality_checker.py
import ast
import os
import json
import re


def get_python_files(folder="."):
    for root, dirs, files in os.walk(folder):
        for f in files:
            if f.endswith(".py"):
                yield os.path.join(root, f)


def get_file_lines(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()


# ---------------------------------------------------
# 1. Missing Docstring Check
# ---------------------------------------------------
def load_docstring_suggestions(path="docstring_suggestions.json"):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    missing = {}
    for item in data:
        file = item["file"]
        func = item["function"]
        missing.setdefault(file, []).append(func)
    return missing


# ---------------------------------------------------
# 2. Long Function Check
# ---------------------------------------------------
def detect_long_functions(tree, file_path, threshold=30):
    long_funcs = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if hasattr(node, "lineno") and hasattr(node, "end_lineno"):
                length = node.end_lineno - node.lineno
                if length > threshold:
                    long_funcs.append({
                        "function": node.name,
                        "length": length,
                        "threshold": threshold
                    })
    return long_funcs


# ---------------------------------------------------
# 3. Too Many Parameters
# ---------------------------------------------------
def detect_too_many_params(tree, threshold=4):
    bad_funcs = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            count = len(node.args.args)
            if count > threshold:
                bad_funcs.append({
                    "function": node.name,
                    "param_count": count,
                    "threshold": threshold
                })
    return bad_funcs


# ---------------------------------------------------
# 4. Deep Nesting
# ---------------------------------------------------
def calculate_nesting(node, depth=0):
    max_depth = depth
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
            max_depth = max(max_depth, calculate_nesting(child, depth + 1))
        else:
            max_depth = max(max_depth, calculate_nesting(child, depth))
    return max_depth


def detect_deep_nesting(tree, threshold=3):
    deep_funcs = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            depth = calculate_nesting(node)
            if depth > threshold:
                deep_funcs.append({
                    "function": node.name,
                    "nesting_depth": depth,
                    "threshold": threshold
                })
    return deep_funcs


# ---------------------------------------------------
# 5. TODO / FIXME detection
# ---------------------------------------------------
todo_pattern = re.compile(r"#\s*(TODO|FIXME|BUG)", re.IGNORECASE)

def detect_todo_comments(file_path):
    todos = []
    lines = get_file_lines(file_path)
    for i, line in enumerate(lines, start=1):
        if todo_pattern.search(line):
            todos.append({"line": i, "text": line.strip()})
    return todos


# ---------------------------------------------------
# Main Quality Analyzer
# ---------------------------------------------------
def analyze_quality():
    results = {}

    missing_docs = load_docstring_suggestions()

    for file_path in get_python_files("."):
        with open(file_path, "r", encoding="utf-8") as f:
            src = f.read()

        try:
            tree = ast.parse(src)
        except Exception:
            continue

        results[file_path] = {
            "missing_docstrings": missing_docs.get(file_path, []),
            "long_functions": detect_long_functions(tree, file_path),
            "too_many_parameters": detect_too_many_params(tree),
            "deep_nesting": detect_deep_nesting(tree),
            "todo_comments": detect_todo_comments(file_path),
        }

    # SAVE JSON
    with open("quality_report.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    # SAVE MARKDOWN
    with open("quality_report.md", "w", encoding="utf-8") as f:
        for file, issues in results.items():
            f.write(f"## File: {file}\n")
            for key, val in issues.items():
                f.write(f"### {key}\n")
                if not val:
                    f.write("No issues found.\n\n")
                else:
                    f.write(json.dumps(val, indent=2))
                    f.write("\n\n")

    print("Wrote quality_report.json and quality_report.md")
    return results


if __name__ == "__main__":
    analyze_quality()
