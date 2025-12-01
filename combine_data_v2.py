# combine_data_v2.py
import json
import os
from datetime import datetime


def load_json(path):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            # If file exists but is invalid, return empty structure and warn
            print(f"[WARN] Invalid JSON at {path}, skipping.")
            return {}
    return {}


def build_combined_v2():
    combined = {
        "project_structure": load_json("project_data.json"),
        "dependencies": load_json("dependency_data.json"),
        "git_history": load_json("commit_changes.json"),
        "change_impact": load_json("impact_report.json"),
        "evolution_timeline": load_json("function_timeline.json"),
        "diff_explanations": load_json("diff_explanations.json"),
        "docstrings": load_json("docstring_suggestions.json"),
        "quality_issues": load_json("quality_report.json"),
        "naming_issues": load_json("naming_report.json"),
        "duplicate_functions": load_json("duplicate_report.json"),
        "unused_functions": load_json("unused_report.json"),
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "project_path": os.path.abspath("."),
            "version": "2.0"
        }
    }

    out_path = "combined_data_v2.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=4)

    print(f"Wrote {out_path}")


if __name__ == "__main__":
    build_combined_v2()
