
import json
import argparse
from llm_writer import generate_sections


def parse_args():
    parser = argparse.ArgumentParser(description="Generate AI documentation sections.")
    parser.add_argument("--input", "-i", default="combined_data_v3.json",
                        help="Path to combined_data_v3.json")
    parser.add_argument("--out", "-o", default="combined_data_v3_with_ai.json",
                        help="Output JSON file with AI sections added")
    parser.add_argument("--md", default="ai_summary.md",
                        help="Markdown file for human-readable AI summary")
    return parser.parse_args()


def main():
    args = parse_args()

    print("[INFO] Loading combined data:", args.input)
    with open(args.input, "r", encoding="utf-8") as f:
        combined = json.load(f)

    print("[INFO] Generating AI documentation sections...")
    ai_sections = generate_sections(combined)

    print("[OK] AI sections generated.")
    print("[INFO] Writing ai_summary.md")

    with open(args.md, "w", encoding="utf-8") as f:
        f.write("# AI-Generated Documentation Summary\n\n")
        for key, value in ai_sections.items():
            f.write(f"## {key.capitalize()}\n\n")
            f.write(value.strip() + "\n\n")

    print("[INFO] Embedding AI sections into combined JSON...")

    combined.setdefault("report", {})
    combined["report"]["ai_summary"] = ai_sections

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)

    print(f"[OK] Wrote updated combined JSON → {args.out}")
    print(f"[OK] Wrote Markdown summary → {args.md}")
    print("\nYour AI documentation is ready!")


if __name__ == "__main__":
    main()
