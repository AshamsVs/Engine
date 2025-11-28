import os
import ast

def get_python_files(folder_path):
    python_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files


def analyze_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        code = file.read()

    tree = ast.parse(code)

    result = {
        "file": file_path,
        "functions": [],
        "classes": []
    }

    # Loop through AST nodes
    for node in ast.walk(tree):

        # Detect Functions
        if isinstance(node, ast.FunctionDef):
            args = [arg.arg for arg in node.args.args]
            doc = ast.get_docstring(node)

            result["functions"].append({
                "name": node.name,
                "args": args,
                "doc": doc
            })

        # Detect Classes
        elif isinstance(node, ast.ClassDef):
            class_doc = ast.get_docstring(node)
            class_info = {
                "name": node.name,
                "doc": class_doc,
                "methods": []
            }

            # Detect methods inside class
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    method_args = [arg.arg for arg in item.args.args]
                    method_doc = ast.get_docstring(item)

                    class_info["methods"].append({
                        "name": item.name,
                        "args": method_args,
                        "doc": method_doc
                    })

            result["classes"].append(class_info)

    return result


def analyze_project(folder_path):
    files = get_python_files(folder_path)
    project_data = []

    for file_path in files:
        project_data.append(analyze_file(file_path))

    return project_data

def generate_markdown(project_data, output_file="documentation.md"):
    with open(output_file, "w", encoding="utf-8") as md:
        md.write("# Project Documentation\n\n")

        for file_data in project_data:
            md.write(f"## File: {file_data['file']}\n\n")

            # Functions
            if file_data["functions"]:
                md.write("### Functions:\n")
                for func in file_data["functions"]:
                    md.write(f"- **{func['name']}({', '.join(func['args'])})**\n")
                    doc = func['doc'] or "_No description available_"
                    md.write(f"  \n  {doc}\n\n")
            else:
                md.write("### Functions:\n_No functions found_\n\n")

            # Classes
            if file_data["classes"]:
                md.write("### Classes:\n")
                for cls in file_data["classes"]:
                    md.write(f"- **{cls['name']}**\n")
                    class_doc = cls['doc'] or "_No description available_"
                    md.write(f"  \n  {class_doc}\n")

                    for method in cls["methods"]:
                        md.write(f"  - Method: **{method['name']}({', '.join(method['args'])})**\n")
                        method_doc = method['doc'] or "_No description available_"
                        md.write(f"    \n    {method_doc}\n")
                    md.write("\n")
            else:
                md.write("### Classes:\n_No classes found_\n\n")

            md.write("\n---\n\n")


# Test run
if __name__ == "__main__":
    folder = "./"   # current directory
    data = analyze_project(folder)
    generate_markdown(data)
    for file_data in data:
        print("=" * 50)
        print("FILE:", file_data["file"])
        print("-" * 50)

        for func in file_data["functions"]:
            print("FUNCTION:", func["name"])
            print("ARGS:", func["args"])
            print("DOC:", func["doc"])
            print()

        for cls in file_data["classes"]:
            print("CLASS:", cls["name"])
            print("DOC:", cls["doc"])
            for m in cls["methods"]:
                print("   METHOD:", m["name"])
                print("   ARGS:", m["args"])
                print("   DOC:", m["doc"])
                print()
