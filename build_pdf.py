"""Build A2_Blog_Draft_v1.pdf from A2_Blog_Draft_v1.md.

Style goals (kept consistent with the previously approved layout):
- A4, 1.4cm margins
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
    margin: 1.4cm;
}
@page :first {
    margin-top: 1.0cm;
    @top-left {
        content: "LU Chuanyu (Marcus)";
        font-family: "Liberation Serif", serif;
        font-size: 11pt;
        font-weight: normal;
        color: #000;
        vertical-align: bottom;
    }
}
html, body {
    font-family: "Liberation Serif", serif;
    font-size: 11pt;
    line-height: 1.5;
    color: #000;
}
body { text-align: justify; hyphens: auto; }
hr {
    border: none;
    height: 0.75pt;
    background-color: #cccccc;
    color: #cccccc;
    margin: 0.5em 0;
}
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
    margin: 0.6em 0 0.25em 0;
}
p { margin: 0 0 0.45em 0; }
em { font-style: italic; }
strong { font-weight: bold; }
img { max-width: 100%; display: block; margin: 0.3em auto 0 auto; }
/* When the markdown processor wraps an image in its own paragraph, the
   paragraph's bottom margin would push the figure caption away from the
   image. Zero it out so the caption sits snug under the figure. */
p.figure-image { margin: 0; }
/* Figure captions: a paragraph immediately following an image-only paragraph
   that begins with "Figure ..." renders centered in soft gray italic. */
figcaption,
p.figure-caption {
    text-align: center;
    font-style: italic;
    color: #666666;
    font-size: 11pt;
    margin: 0.1em 0 0.7em 0;
}

a { color: #000; text-decoration: none; word-break: break-all; }
.word-count {
    text-align: right;
    font-style: italic;
    color: #666666;
    font-size: 10pt;
    margin-top: 0.2em;
}
"""


def main() -> None:
    md_text = MD_FILE.read_text(encoding="utf-8")
    html_body = markdown.markdown(
        md_text,
        extensions=["extra", "sane_lists"],
        output_format="html5",
    )
    # Tag figure-caption paragraphs. Python-Markdown joins an image and a
    # following italic caption ("*Figure ...*") into one <p>; split that into
    # a separate centered, soft-gray italic caption paragraph.
    import re
    html_body = re.sub(
        r'<p>(<img[^>]*>)\s*<em>(Figure [^<]*)</em>\s*</p>',
        r'<p class="figure-image">\1</p>\n<p class="figure-caption"><em>\2</em></p>',
        html_body,
    )
    # Also catch the standalone form, in case markdown ever emits it.
    html_body = re.sub(
        r'<p>(<em>Figure [^<]*</em>)</p>',
        r'<p class="figure-caption">\1</p>',
        html_body,
    )
    # Tag any remaining paragraphs that contain only an image so their
    # bottom margin doesn't add extra whitespace before the caption.
    html_body = re.sub(
        r'<p>(<img[^>]*>)</p>',
        r'<p class="figure-image">\1</p>',
        html_body,
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
