"""Build A2_Blog_Draft_v1.pdf from A2_Blog_Draft_v1.md.

Style goals (kept consistent with the previously approved layout):
- A4, 1.8cm margins
- Serif (Liberation Serif), justified body at 11pt
- H1 (title) 20pt bold, H2 14pt bold
- Italic emphasis renders inline at body size (no centered block treatment)
- Author name "LU Chuanyu (Marcus)" appears at the top-left of page 1
  at normal text size (11pt, regular weight)
"""

from pathlib import Path

import markdown
from weasyprint import CSS, HTML

ROOT = Path(__file__).parent
MD_FILE = ROOT / "A2_Blog_Draft_v1.md"
PDF_FILE = ROOT / "A2_Blog_Draft_v1.pdf"

AUTHOR = "LU Chuanyu (Marcus)"

CSS_STR = """
@page {
    size: A4;
    margin: 1.8cm;
}
@page :first {
    @top-left {
        content: "LU Chuanyu (Marcus)";
        font-family: "Liberation Serif", serif;
        font-size: 11pt;
        font-weight: normal;
        color: #000;
        margin-bottom: 0.4cm;
    }
}
html, body {
    font-family: "Liberation Serif", serif;
    font-size: 11pt;
    line-height: 1.4;
    color: #000;
}
body { text-align: justify; hyphens: auto; }
h1 {
    font-size: 20pt;
    font-weight: bold;
    text-align: left;
    margin: 0 0 0.4em 0;
    line-height: 1.2;
}
/* Subtitle: a paragraph immediately after the H1 that is entirely italic */
h1 + p em:only-child {
    display: block;
    text-align: center;
    font-size: 10pt;
    margin: 0.2em 0 1em 0;
}
h2 {
    font-size: 14pt;
    font-weight: bold;
    margin: 1em 0 0.4em 0;
}
p { margin: 0 0 0.6em 0; }
em { font-style: italic; }
strong { font-weight: bold; }
img { max-width: 100%; display: block; margin: 0.6em auto; }

a { color: #000; text-decoration: none; word-break: break-all; }
"""


def main() -> None:
    md_text = MD_FILE.read_text(encoding="utf-8")
    html_body = markdown.markdown(
        md_text,
        extensions=["extra", "sane_lists"],
        output_format="html5",
    )
    html_doc = f"""<!doctype html>
<html lang=\"en\">
<head><meta charset=\"utf-8\"><title>A2 Blog Draft</title></head>
<body>{html_body}</body>
</html>
"""
    HTML(string=html_doc, base_url=str(ROOT)).write_pdf(
        target=str(PDF_FILE),
        stylesheets=[CSS(string=CSS_STR)],
    )
    print(f"Wrote {PDF_FILE} ({PDF_FILE.stat().st_size} bytes); author header: {AUTHOR}")


if __name__ == "__main__":
    main()
