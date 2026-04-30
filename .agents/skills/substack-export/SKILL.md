---
name: substack-export
description: Convert an MkDocs blog post in this repo to Substack-ready HTML. Strips frontmatter, pulls the H1 as the title, rewrites image paths to absolute URLs on hadijaveed.me, renders to HTML, and opens it in the browser so the user can select-all and paste into Substack's editor. Trigger on "/substack-export <post-path>" or when the user asks to publish a post from this blog to Substack.
---

# substack-export

Substack's editor is a WYSIWYG (ProseMirror) and does not accept markdown. It does accept rich text pasted from a rendered browser page, so the workflow is: render markdown to HTML, open in browser, select all, copy, paste into Substack.

## How to run

```bash
source .venv/bin/activate
python .Codex/skills/substack-export/export.py <path-to-post.md>
```

If the user gives just a slug or filename, resolve it to `docs/posts/<filename>.md`. If ambiguous, ask.

The script will:

1. Strip the YAML frontmatter and the `<!-- more -->` marker.
2. Extract the first H1 as the post title (printed separately so it can be pasted into Substack's title field, not the body).
3. Rewrite `(../assets/...)` and `(assets/...)` references to `https://hadijaveed.me/assets/...` so Substack's image-fetcher can grab them on paste.
4. Strip mkdocs `{:target="_blank"}` attribute-list syntax (Substack opens external links in new tabs by default).
5. Convert markdown to HTML with `extra` (tables, fenced code, footnotes), `sane_lists`, and `smarty` extensions.
6. Wrap in a clean serif-styled HTML page with a yellow banner showing the title and a canonical URL.
7. Write to `/tmp/substack-export-<slug>.html` and open it in the default browser via `open`.

After running, tell the user:

- The title (for Substack's title field).
- The canonical URL (for Substack's "Original source URL" field — good for SEO if the post already exists on hadijaveed.me).
- That they should select-all (Cmd+A) on the page (the yellow banner is `display:none` in print/copy contexts but will be included in a select-all — they can delete it after pasting, or skip it by clicking below the banner before select-all).
- That images on Substack are hosted by Substack: pasting absolute URLs usually triggers auto-fetch, but if any image fails to import they'll need to upload manually.

## Caveats to mention if relevant

- **Code highlighting**: Substack restyles code blocks with its own monospace formatting. Block structure transfers, syntax colors do not.
- **Mermaid / admonitions / pymdown-only syntax**: These won't render. If a post uses `!!! note` admonitions, mermaid fences, or other mkdocs-only extensions, warn the user that those sections will appear as raw text and need manual handling.
- **Footnotes**: Standard Python markdown's `extra` extension renders footnotes as a numbered list at the bottom with backlinks. Substack will preserve the structure but the backlink anchors may not work after paste.
