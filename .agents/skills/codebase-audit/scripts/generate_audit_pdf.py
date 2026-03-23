#!/usr/bin/env python3
"""
Convert a codebase audit markdown report into a styled PDF (ReportLab).

Expects a single markdown file with optional sections:
  ## Codebase Map
  ## Audit Report
  ## Functional Documentation

Dependencies: pip install reportlab

Example:
  python generate_audit_pdf.py --input report.md --title "My App" --author "Jane Doe"
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from datetime import date
from pathlib import Path

from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    PageBreak,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
    Paragraph,
)
from reportlab.platypus.doctemplate import SimpleDocTemplate
from reportlab.platypus.tableofcontents import TableOfContents

PRIMARY = HexColor("#334bec")
SECONDARY = HexColor("#1f2e9a")

SECTION_HEADERS = ("Codebase Map", "Audit Report", "Functional Documentation")
SECTION_PATTERN = re.compile(
    r"^##\s+(" + "|".join(re.escape(s) for s in SECTION_HEADERS) + r")\s*$",
    re.MULTILINE,
)


def slugify(name: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", name.strip().lower()).strip("-")
    return s or "project"


def inline_markup(line: str) -> str:
    """Apply **bold** and `inline code` after escaping plain text segments."""
    pattern = re.compile(r"(`[^`]+`|\*\*[^*]+\*\*)")
    parts = pattern.split(line)
    out: list[str] = []
    for part in parts:
        if not part:
            continue
        if part.startswith("`") and part.endswith("`"):
            inner = html.escape(part[1:-1])
            out.append(f'<font name="Courier" color="#1f2e9a">{inner}</font>')
        elif part.startswith("**") and part.endswith("**"):
            inner = html.escape(part[2:-2])
            out.append(f"<b>{inner}</b>")
        else:
            out.append(html.escape(part))
    return "".join(out)


def build_styles():
    base = getSampleStyleSheet()
    styles = {name: base[name] for name in base.byName}

    styles["Normal"] = ParagraphStyle(
        "Normal",
        parent=base["Normal"],
        fontSize=10,
        leading=12,
        textColor=black,
    )
    styles["Bullet"] = ParagraphStyle(
        "Bullet",
        parent=styles["Normal"],
        bulletText="•",
        leftIndent=22,
        bulletIndent=8,
        firstLineIndent=0,
    )
    styles["Title"] = ParagraphStyle(
        "Title",
        parent=base["Title"],
        fontSize=22,
        leading=28,
        textColor=PRIMARY,
        spaceAfter=12,
        alignment=1,
    )
    styles["Subtitle"] = ParagraphStyle(
        "Subtitle",
        parent=base["Heading2"],
        fontSize=12,
        leading=15,
        textColor=black,
        alignment=1,
        spaceAfter=6,
    )
    for level, size, space in ((1, 16, 10), (2, 14, 8), (3, 12, 6)):
        styles[f"Heading{level}"] = ParagraphStyle(
            f"Heading{level}",
            parent=base[f"Heading{level}"],
            fontSize=size,
            leading=size + 4,
            textColor=PRIMARY,
            spaceAfter=space,
            spaceBefore=4 if level > 1 else 0,
        )
    styles["AuditChapter"] = ParagraphStyle(
        "AuditChapter",
        parent=styles["Heading1"],
        fontSize=18,
        leading=22,
        textColor=PRIMARY,
        spaceBefore=18,
        spaceAfter=12,
    )
    styles["CodeBlock"] = ParagraphStyle(
        "CodeBlock",
        fontName="Courier",
        fontSize=8,
        leading=10,
        textColor=white,
    )
    return styles


def code_block_table(pre: Preformatted, content_width: float) -> Table:
    tbl = Table([[pre]], colWidths=[content_width])
    tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), SECONDARY),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return tbl


def parse_markdown_body(body: str, styles: dict, content_width: float) -> list:
    """Parse markdown subset into flowables."""
    flowables: list = []
    lines = body.split("\n")
    i = 0
    para_buf: list[str] = []

    def flush_paragraph():
        nonlocal para_buf
        if not para_buf:
            return
        text = " ".join(para_buf).strip()
        para_buf = []
        if not text:
            return
        flowables.append(Paragraph(inline_markup(text), styles["Normal"]))
        flowables.append(Spacer(1, 6))

    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()

        if stripped.startswith("```"):
            flush_paragraph()
            block: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                block.append(lines[i])
                i += 1
            if i < len(lines) and lines[i].strip().startswith("```"):
                i += 1
            code_text = "\n".join(block)
            pre = Preformatted(code_text, styles["CodeBlock"], maxLineLength=120)
            flowables.append(Spacer(1, 6))
            flowables.append(code_block_table(pre, content_width))
            flowables.append(Spacer(1, 10))
            continue

        if not stripped:
            flush_paragraph()
            flowables.append(Spacer(1, 6))
            i += 1
            continue

        if stripped.startswith("#### "):
            flush_paragraph()
            flowables.append(Paragraph(inline_markup(stripped[5:]), styles["Heading3"]))
            i += 1
            continue
        if stripped.startswith("### "):
            flush_paragraph()
            flowables.append(Paragraph(inline_markup(stripped[4:]), styles["Heading3"]))
            i += 1
            continue
        if stripped.startswith("## "):
            flush_paragraph()
            flowables.append(Paragraph(inline_markup(stripped[3:]), styles["Heading2"]))
            i += 1
            continue
        if stripped.startswith("# "):
            flush_paragraph()
            flowables.append(Paragraph(inline_markup(stripped[2:]), styles["Heading1"]))
            i += 1
            continue

        if stripped.startswith("- ") or stripped.startswith("* "):
            flush_paragraph()
            item = stripped[2:].strip()
            flowables.append(Paragraph(inline_markup(item), styles["Bullet"]))
            flowables.append(Spacer(1, 4))
            i += 1
            continue

        para_buf.append(stripped)
        i += 1

    flush_paragraph()
    return flowables


def split_sections(markdown: str) -> dict[str, str]:
    """Extract known ## sections; returns title -> body (trimmed)."""
    matches = list(SECTION_PATTERN.finditer(markdown))
    if not matches:
        return {"Full report": markdown.strip()}

    preamble = markdown[: matches[0].start()].strip()
    sections: dict[str, str] = {}
    for idx, m in enumerate(matches):
        title = m.group(1)
        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(markdown)
        body = markdown[start:end].strip()
        if idx == 0 and preamble:
            body = f"{preamble}\n\n{body}".strip()
        sections[title] = body
    return sections


class AuditDocTemplate(SimpleDocTemplate):
    """Registers chapter titles for TableOfContents."""

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name == "AuditChapter":
            text = flowable.getPlainText()
            self.notify("TOCEntry", (0, text, self.page))


def build_story(
    sections: dict[str, str],
    styles: dict,
    content_width: float,
    toc: TableOfContents,
):
    story: list = []
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph("<b>Table of contents</b>", styles["Heading2"]))
    story.append(Spacer(1, 12))
    story.append(toc)
    story.append(PageBreak())

    chapter_order = [h for h in SECTION_HEADERS if h in sections]
    for key in sections:
        if key not in chapter_order and key != "Full report":
            chapter_order.append(key)
    if "Full report" in sections:
        chapter_order = ["Full report"]

    for chapter_title in chapter_order:
        body = sections[chapter_title]
        story.append(Paragraph(html.escape(chapter_title), styles["AuditChapter"]))
        story.extend(parse_markdown_body(body, styles, content_width))
        story.append(PageBreak())

    if story and isinstance(story[-1], PageBreak):
        story.pop()
    return story


def make_toc(styles: dict) -> TableOfContents:
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle(
            name="TOC0",
            parent=styles["Normal"],
            fontSize=11,
            leading=14,
            leftIndent=0,
            firstLineIndent=0,
            spaceBefore=3,
            textColor=PRIMARY,
        ),
    ]
    return toc


def run(
    input_path: Path,
    output_path: Path,
    title: str,
    author: str,
    audit_date: str | None,
) -> None:
    markdown = input_path.read_text(encoding="utf-8")
    sections = split_sections(markdown)
    styles = build_styles()

    margin = 0.85 * inch
    doc = AuditDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=margin,
        rightMargin=margin,
        topMargin=margin,
        bottomMargin=margin,
        title=title,
    )
    content_width = A4[0] - doc.leftMargin - doc.rightMargin

    toc = make_toc(styles)
    story = build_story(sections, styles, content_width, toc)

    cover = [
        Spacer(1, 2.2 * inch),
        Paragraph(html.escape(title), styles["Title"]),
        Spacer(1, 0.35 * inch),
        Paragraph(
            f"<b>Codebase audit</b><br/>{html.escape(audit_date or date.today().isoformat())}",
            styles["Subtitle"],
        ),
        Spacer(1, 0.25 * inch),
        Paragraph(html.escape(author), styles["Subtitle"]),
        PageBreak(),
    ]

    full_story = cover + story
    doc.multiBuild(full_story)


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate codebase audit PDF from markdown.")
    p.add_argument(
        "--input",
        "-i",
        type=Path,
        required=True,
        help="Path to markdown file containing audit sections",
    )
    p.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Output PDF path (default: <slug>-audit-<date>.pdf next to input)",
    )
    p.add_argument("--title", "-t", required=True, help="Application or project name (title page)")
    p.add_argument("--author", "-a", required=True, help="Author name for title page")
    p.add_argument(
        "--date",
        "-d",
        default=None,
        help="Audit date (YYYY-MM-DD). Defaults to today.",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if not args.input.is_file():
        print(f"Input not found: {args.input}", file=sys.stderr)
        return 1

    audit_date = args.date or date.today().isoformat()
    out = args.output
    if out is None:
        out = args.input.parent / f"{slugify(args.title)}-audit-{audit_date}.pdf"

    run(args.input, out, args.title, args.author, audit_date)
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
