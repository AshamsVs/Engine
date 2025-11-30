import os
import json
import sys
import tempfile
import traceback

from combine_data import combine
from exporter import export_markdown, export_html, export_pdf

# ---- SAFETY VALIDATOR ----
def validate_combined_data(data):
    """
    Ensure combined data contains all required keys.
    Fill defaults so exporter never crashes.
    """
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except Exception:
            data = {}

    if not isinstance(data, dict):
        data = {}

    data.setdefault("metadata", {})
    data["metadata"].setdefault("project_path", "")
    data["metadata"].setdefault("generated_at", "")

    data.setdefault("dependencies", {})
    data["dependencies"].setdefault("files", {})
    data["dependencies"].setdefault("functions", {})

    data.setdefault("git_history", [])
    data.setdefault("change_impact", {})
    data.setdefault("evolution_timeline", {})
    data.setdefault("diff_explanations", [])
    data.setdefault("docstrings", [])
    data.setdefault("quality_issues", {})
    data.setdefault("naming_issues", {})
    data.setdefault("duplicate_functions", {})
    data.setdefault("unused_functions", {})

    return data



def run_engine(project_path, output_basename="report"):
    try:
        # 1. Normalize path
        project_path = os.path.abspath(project_path)

        # 2. Run analysis (Phase 1 + Phase 2)
        data = combine(project_path)
        data = validate_combined_data(data)

        # 3. Export folder
        output_dir = os.path.join(project_path, "autodoc_output")
        os.makedirs(output_dir, exist_ok=True)

        # 4. Template used for report
        template_path = os.path.join("templates", "report_template.md")

        # 5. Export
        md = export_markdown(data, template_path, os.path.join(output_dir, output_basename))
        html = export_html(md, os.path.join(output_dir, output_basename))
        pdf = export_pdf(html, os.path.join(output_dir, output_basename))

        # 6. Output JSON
        json_path = os.path.join(output_dir, f"{output_basename}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        return {
            "status": "success",
            "output_dir": output_dir,
            "files": {
                "md": md,
                "html": html,
                "pdf": pdf,
                "json": json_path
            }
        }

    except Exception as e:
        traceback.print_exc()
        return {
            "status": "error",
            "message": str(e)
        }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_engine.py <project_folder>")
        sys.exit(1)

    project_path = sys.argv[1]
    result = run_engine(project_path)
    print(result)
