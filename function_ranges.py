import ast

def get_function_ranges(file_path):
    with open(file_path, "r") as f:
        tree = ast.parse(f.read())

    functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append({
                "name": node.name,
                "start": node.lineno,
                "end": node.end_lineno
            })

    return functions

# Test
if __name__ == "__main__":
    print(get_function_ranges("demo.py"))
