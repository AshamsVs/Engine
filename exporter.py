import json
import argparse
from markdown import markdown
from jinja2 import Template

try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except Exception:
    WEASYPRINT_AVAILABLE = False


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_template(path):
    with open(path, "r", encoding="utf-8") as f:
        return Template(f.read())


def export_markdown(data, template_path, output_path):
    template = load_template(template_path)
    rendered = template.render(data=data)

    md_path = output_path + ".md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"[OK] Wrote Markdown: {md_path}")
    return rendered


def export_html(markdown_text, output_path):
    html_text = markdown(markdown_text, extensions=['fenced_code', 'tables'])

    html_path = output_path + ".html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_text)

    print(f"[OK] Wrote HTML: {html_path}")
    return html_text


def export_pdf(html_text, output_path):
    if not WEASYPRINT_AVAILABLE:
        print("[WARN] WeasyPrint not installed. Skipping PDF export.")
        return

    pdf_path = output_path + ".pdf"
    HTML(string=html_text).write_pdf(pdf_path)
    print(f"[OK] Wrote PDF: {pdf_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--template", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    data = load_json(args.data)

    md = export_markdown(data, args.template, args.out)
    html = export_html(md, args.out)
    export_pdf(html, args.out)


if __name__ == "__main__":
    main()
