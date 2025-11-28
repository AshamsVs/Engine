import ast
import os
import json

# ----------------------------
# Utility: Get python files
# ----------------------------
def get_python_files(folder):
    py_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    return py_files


# ----------------------------
# Part 1: File → File imports
# ----------------------------
def get_module_name(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]

def build_module_to_file_map(folder):
    module_map = {}
    for file in get_python_files(folder):
        module_map[get_module_name(file)] = file
    return module_map

def analyze_imports(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())

    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module.split('.')[0])
    return imports

def build_file_dependency_graph(folder):
    graph = {}
    module_map = build_module_to_file_map(folder)

    for file in get_python_files(folder):
        raw = analyze_imports(file)
        resolved = [module_map[m] for m in raw if m in module_map]
        graph[file] = resolved

    return graph


# ----------------------------
# Part 2: Function → Function
# ----------------------------
def extract_defined_functions(tree):
    funcs = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            funcs.add(node.name)
    return funcs

def extract_calls(func_node):
    calls = []
    for node in ast.walk(func_node):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                calls.append(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                calls.append(node.func.attr)
    return calls

def build_filtered_call_graph(folder):
    graph = {}
    all_functions = set()
    file_trees = {}

    # Gather function definitions
    for file in get_python_files(folder):
        with open(file, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
            file_trees[file] = tree
            all_functions.update(extract_defined_functions(tree))

    # Build call graph
    for file, tree in file_trees.items():
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                caller = node.name
                all_calls = extract_calls(node)
                filtered = [c for c in all_calls if c in all_functions]
                graph[caller] = filtered

    return graph


# ----------------------------
# Main: Combine into JSON
# ----------------------------
def build_dependency_data(folder="."):
    return {
        "files": build_file_dependency_graph(folder),
        "functions": build_filtered_call_graph(folder)
    }


if __name__ == "__main__":
    deps = build_dependency_data(".")
    print(json.dumps(deps, indent=2))
    with open("dependency_data.json", "w") as f:
        json.dump(deps, f, indent=2)
    print("\nWrote dependency_data.json")
