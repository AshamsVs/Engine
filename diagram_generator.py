import json

def load_dependencies():
    with open("dependency_data.json", "r") as f:
        return json.load(f)

def generate_file_dependency_mermaid(files):
    lines = ["flowchart TD"]

    for src, deps in files.items():
        src_label = src.replace(".\\", "")
        for dep in deps:
            dep_label = dep.replace(".\\", "")
            lines.append(f"    {src_label} --> {dep_label}")

    return "\n".join(lines)

def generate_function_dependency_mermaid(funcs):
    lines = ["flowchart TD"]

    for src, deps in funcs.items():
        for dep in deps:
            lines.append(f"    {src} --> {dep}")

    return "\n".join(lines)

if __name__ == "__main__":
    deps = load_dependencies()

    file_diagram = generate_file_dependency_mermaid(deps["files"])
    func_diagram = generate_function_dependency_mermaid(deps["functions"])

    with open("file_dependencies.mmd", "w") as f:
        f.write(file_diagram)

    with open("function_dependencies.mmd", "w") as f:
        f.write(func_diagram)

    print("Generated file_dependencies.mmd")
    print("Generated function_dependencies.mmd")
