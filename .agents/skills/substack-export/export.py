#!/usr/bin/env python3
"""Convert an MkDocs blog post to Substack-ready HTML.

Usage: export.py <path-to-post.md>

Strips frontmatter and the <!-- more --> marker, pulls out the H1 as the
post title, rewrites relative asset paths to absolute URLs on the live
blog, renders to HTML, and opens the result in the default browser so it
can be selected and pasted into Substack's editor.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import markdown
import yaml

SITE_URL = "https://hadijaveed.me"


def split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    fm_block = text[4:end]
    body = text[end + 5 :]
    try:
        meta = yaml.safe_load(fm_block) or {}
    except yaml.YAMLError:
        meta = {}
    return meta, body


def extract_title(body: str) -> tuple[str, str]:
    lines = body.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("# "):
            title = line[2:].strip()
            del lines[i]
            while lines and lines[0].strip() == "":
                lines.pop(0)
            return title, "\n".join(lines)
    return "", body


def rewrite_assets(body: str) -> str:
    return re.sub(r"\((?:\.\./)?assets/", f"({SITE_URL}/assets/", body)


def strip_attr_lists(body: str) -> str:
    return re.sub(r"(\]\([^)]+\))\s*\{[^}]*\}", r"\1", body)


def to_html(md_body: str) -> str:
    return markdown.markdown(
        md_body,
        extensions=["extra", "sane_lists", "smarty"],
        output_format="html",
    )


HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title} - Substack export</title>
<style>
  body {{
    font-family: Georgia, "Times New Roman", serif;
    max-width: 680px;
    margin: 60px auto;
    padding: 0 20px;
    line-height: 1.6;
    color: #1a1a1a;
    font-size: 18px;
  }}
  h1, h2, h3, h4 {{
    font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", sans-serif;
    line-height: 1.25;
  }}
  h1 {{ font-size: 32px; margin-bottom: 8px; }}
  h2 {{ font-size: 24px; margin-top: 36px; }}
  h3 {{ font-size: 20px; margin-top: 28px; }}
  pre, code {{ font-family: "SF Mono", Monaco, Consolas, monospace; }}
  pre {{
    background: #f5f5f5; padding: 16px; border-radius: 6px;
    overflow-x: auto; font-size: 14px; line-height: 1.45;
  }}
  code {{ background: #f0f0f0; padding: 2px 5px; border-radius: 3px; font-size: 0.9em; }}
  pre code {{ background: none; padding: 0; }}
  blockquote {{
    border-left: 4px solid #ccc; margin: 0; padding: 4px 16px; color: #555;
  }}
  img {{ max-width: 100%; height: auto; display: block; margin: 24px auto; }}
  a {{ color: #0066cc; }}
  hr {{ border: none; border-top: 1px solid #ddd; margin: 32px 0; }}
  table {{ border-collapse: collapse; width: 100%; margin: 16px 0; }}
  th, td {{ border: 1px solid #ddd; padding: 8px 12px; text-align: left; }}
  th {{ background: #f5f5f5; }}

  .banner {{
    background: #fff7d6; border: 1px solid #e5d294; padding: 14px 18px;
    border-radius: 6px; font-family: -apple-system, sans-serif; font-size: 14px;
    margin-bottom: 36px; line-height: 1.5;
  }}
  .banner code {{ background: #fff; }}
  .banner strong {{ display: block; margin-bottom: 4px; }}
  @media print {{ .banner {{ display: none; }} }}
</style>
</head>
<body>
<div class="banner">
  <strong>Substack export ready.</strong>
  Title: <code>{title}</code><br>
  Select all (&#8984;A) then copy (&#8984;C) and paste the body into Substack.
  Title goes in Substack's title field separately.{canonical}
</div>
{html}
</body>
</html>
"""


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: export.py <post.md>", file=sys.stderr)
        return 1

    path = Path(sys.argv[1]).expanduser().resolve()
    if not path.exists():
        print(f"file not found: {path}", file=sys.stderr)
        return 1

    raw = path.read_text()
    meta, body = split_frontmatter(raw)
    body = body.replace("<!-- more -->", "")
    title, body = extract_title(body)
    body = rewrite_assets(body)
    body = strip_attr_lists(body)
    html_body = to_html(body)

    canonical_block = ""
    canonical_url = ""
    slug = meta.get("slug")
    date = meta.get("date")
    if slug and date:
        date_str = str(date).replace("-", "/")
        canonical_url = f"{SITE_URL}/{date_str}/{slug}/"
        canonical_block = (
            f'<br>Canonical: <a href="{canonical_url}">{canonical_url}</a> '
            "(paste into Substack's <em>Original source URL</em> field for SEO)."
        )

    out_html = HTML_TEMPLATE.format(
        title=title or path.stem,
        html=html_body,
        canonical=canonical_block,
    )

    out_path = Path("/tmp") / f"substack-export-{slug or path.stem}.html"
    out_path.write_text(out_html)

    print(f"Title:     {title or '(no H1 found)'}")
    if canonical_url:
        print(f"Canonical: {canonical_url}")
    print(f"Output:    {out_path}")
    print("Opening in browser...")
    subprocess.run(["open", str(out_path)], check=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
