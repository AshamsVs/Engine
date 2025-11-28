import ast
import os

def get_python_files(folder):
    py_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    return py_files

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
            # function calls: func()
            if isinstance(node.func, ast.Name):
                calls.append(node.func.id)
            # method calls: obj.method()
            elif isinstance(node.func, ast.Attribute):
                calls.append(node.func.attr)
    return calls

def build_filtered_call_graph(folder):
    graph = {}
    all_functions = set()

    # 1. Extract all defined functions from the project
    file_trees = {}
    for file in get_python_files(folder):
        with open(file, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
            file_trees[file] = tree
            all_functions.update(extract_defined_functions(tree))

    # 2. Build call graph only for project functions
    for file, tree in file_trees.items():
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                caller = node.name
                all_calls = extract_calls(node)
                
                # Keep only calls to project functions
                filtered = [c for c in all_calls if c in all_functions]

                graph[caller] = filtered

    return graph

if __name__ == "__main__":
    graph = build_filtered_call_graph(".")
    print("Filtered Function Call Dependencies:\n")
    for func, deps in graph.items():
        print(f"{func} → {deps}")
