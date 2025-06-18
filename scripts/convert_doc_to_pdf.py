import sys
from pathlib import Path
import markdown
from xhtml2pdf import pisa


def convert_markdown_to_pdf(md_path: str, pdf_path: str) -> None:
    """Convert a Markdown file to a grayscale PDF."""
    text = Path(md_path).read_text(encoding="utf-8")
    html_body = markdown.markdown(text, extensions=["extra"])
    css = """
    <style>
    body { font-family: Helvetica, Arial, sans-serif; color: #000; }
    h1, h2, h3, h4, h5, h6 { color: #111; }
    </style>
    """
    html = f"<html><head>{css}</head><body>{html_body}</body></html>"
    with open(pdf_path, "wb") as target:
        pisa.CreatePDF(html, dest=target)


def main(args: list[str]) -> None:
    if len(args) != 2:
        print("Usage: convert_doc_to_pdf.py input.md output.pdf")
        raise SystemExit(1)
    convert_markdown_to_pdf(args[0], args[1])


if __name__ == "__main__":
    main(sys.argv[1:])
