# exporter.py
import json
import argparse
import os
from markdown import markdown
from jinja2 import Template, TemplateError

try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except Exception:
    WEASYPRINT_AVAILABLE = False


def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"[ERROR] JSON file not found: {path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"[ERROR] Invalid JSON format in {path}: {e}")


def load_template(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"[ERROR] Template not found: {path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            return Template(f.read())
    except TemplateError as e:
        raise ValueError(f"[ERROR] Jinja template error in {path}: {e}")


def ensure_output_dir(output_path):
    directory = os.path.dirname(output_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


def export_markdown(data, template_path, output_path):
    template = load_template(template_path)

    try:
        rendered = template.render(data=data)
    except Exception as e:
        raise RuntimeError(f"[ERROR] Failed to render markdown template: {e}")

    md_path = output_path + ".md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"[OK] Wrote Markdown: {md_path}")
    return rendered


def export_html(markdown_text, output_path):
    try:
        html_text = markdown(markdown_text, extensions=['fenced_code', 'tables'])
    except Exception as e:
        raise RuntimeError(f"[ERROR] Markdown-to-HTML conversion failed: {e}")

    html_path = output_path + ".html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_text)

    print(f"[OK] Wrote HTML: {html_path}")
    return html_text


def export_pdf(html_text, output_path):
    if not WEASYPRINT_AVAILABLE:
        print("[WARN] WeasyPrint not available. Skipping PDF export.")
        return

    pdf_path = output_path + ".pdf"
    try:
        HTML(string=html_text).write_pdf(pdf_path)
        print(f"[OK] Wrote PDF: {pdf_path}")
    except Exception as e:
        print(f"[WARN] Failed to generate PDF: {e}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--template", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    # ensure output directory exists
    ensure_output_dir(args.out)

    data = load_json(args.data)
    md = export_markdown(data, args.template, args.out)
    html = export_html(md, args.out)
    export_pdf(html, args.out)


if __name__ == "__main__":
    main()
