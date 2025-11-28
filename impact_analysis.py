import json

def load_dependencies():
    with open("dependency_data.json", "r") as f:
        return json.load(f)

def load_commit_changes():
    with open("commit_changes.json", "r") as f:
        return json.load(f)

def build_reverse_dependency_graph(func_graph):
    reverse = {}
    for caller, callees in func_graph.items():
        for callee in callees:
            reverse.setdefault(callee, []).append(caller)
    return reverse

def get_full_impact(changed_function, reverse_graph):
    impacted = set()
    queue = [changed_function]

    while queue:
        current = queue.pop(0)

        if current in reverse_graph:
            for dep in reverse_graph[current]:
                if dep not in impacted:
                    impacted.add(dep)
                    queue.append(dep)

    return list(impacted)

def calculate_risk_level(impact_list):
    count = len(impact_list)

    if count == 0:
        return "LOW"
    if count <= 2:
        return "MEDIUM"
    return "HIGH"

def build_cia_report():
    deps = load_dependencies()
    func_graph = deps["functions"]
    reverse_graph = build_reverse_dependency_graph(func_graph)

    commit_changes = load_commit_changes()
    cia = {}

    for entry in commit_changes:
        commit_id = entry["commit"]
        changed_funcs = entry["changed_functions"]

        cia[commit_id] = {}

        for func in changed_funcs:
            impact = get_full_impact(func, reverse_graph)
            risk = calculate_risk_level(impact)

            cia[commit_id][func] = {
                "direct_and_indirect_impact": impact,
                "risk": risk
            }

    return cia

if __name__ == "__main__":
    report = build_cia_report()
    print(json.dumps(report, indent=2))

    with open("impact_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print("\nWrote impact_report.json")
