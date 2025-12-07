import os
import json
import sys
import shutil
import traceback

# --- AutoDoc components ---
from combine_data_v3 import build_combined
from llm_generate import main as generate_ai_docs
from exporter import export_markdown, export_html, export_pdf


# ---------------------------------------------------------------
#  Clean output directory helper
# ---------------------------------------------------------------
def prepare_output_dir(output_dir="autodoc_output"):
    """Recreate output directory cleanly."""
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    return os.path.abspath(output_dir)


# ---------------------------------------------------------------
#   Unified AutoDoc Engine Runner
# ---------------------------------------------------------------
def run_engine(project_path, output_basename="report"):
    try:
        print("\n====================================================")
        print("            AUTO-DOCUMENTATION ENGINE")
        print("====================================================\n")

        # Normalize path
        project_path = os.path.abspath(project_path)
        print(f"[INFO] Project: {project_path}")

        # 1. Prepare output folder
        print("[INFO] Preparing clean output directory...")
        output_dir = prepare_output_dir(os.path.join(project_path, "autodoc_output"))

        # 2. Run static + dependency + commit analysis
        print("[1/4] Running static analysis + dependency graph + commit mining...")
        data = build_combined(project_path)
        print("[INFO] Static analysis complete.")

        # Save intermediate combined data before AI
        combined_path = os.path.join(output_dir, "combined_data_v3.json")
        with open(combined_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"[INFO] Saved raw combined data → {combined_path}")

        # 3. Run AI generator
        print("\n[2/4] Generating AI documentation (LLM)...")
        try:
            generate_ai_docs()  # produces combined_data_v3_with_ai.json
            ai_output_file = "combined_data_v3_with_ai.json"

            if os.path.exists(ai_output_file):
                with open(ai_output_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                print("[INFO] AI-enhanced combined data loaded.")
            else:
                print("[WARN] AI output JSON not found, continuing with static data.")

        except Exception as e:
            print("[WARN] AI documentation generator failed:")
            traceback.print_exc()

        # Save final combined JSON
        final_json_path = os.path.join(output_dir, "combined_data_final.json")
        with open(final_json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"[INFO] Saved AI-enhanced combined JSON → {final_json_path}")

        # 4. Export final documentation (MD + HTML + PDF)
        print("\n[3/4] Exporting final documentation (MD, HTML, PDF)...")

        template_path = os.path.join("templates", "report_template.md")
        output_base = os.path.join(output_dir, output_basename)

        md = export_markdown(data, template_path, output_base)
        html = export_html(md, output_base)
        pdf = export_pdf(html, output_base)

        print("[INFO] Export step complete.")

        # 5. Finish
        print("\n[4/4] AutoDoc Engine completed successfully!")
        print(f"[OUTPUT] All files available in: {output_dir}\n")

        return {
            "status": "success",
            "output_dir": output_dir,
            "files": {
                "md": output_base + ".md",
                "html": output_base + ".html",
                "pdf": output_base + ".pdf",
                "json": final_json_path
            }
        }

    except Exception as e:
        print("\n[ERROR] AutoDoc Engine failed:")
        traceback.print_exc()
        return {"status": "error", "message": str(e)}


# ---------------------------------------------------------------
#   Command-line entry point
# ---------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:\n   python run_engine.py <project_folder>\n")
        sys.exit(1)

    project_path = sys.argv[1]
    result = run_engine(project_path)
    print(result)
