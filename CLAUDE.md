# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Local development server with live reload
mkdocs serve

# Build static site
mkdocs build
```

## Project Structure

This is an MkDocs Material blog. Key locations:

- `docs/posts/` - Blog posts (markdown files)
- `docs/assets/` - Images and media files
- `docs/index.md` - Homepage
- `docs/about.md` - About page
- `mkdocs.yml` - Site configuration
- `overrides/` - Custom HTML templates

## Writing New Blog Posts

### File Location

Create new posts in `docs/posts/` with a descriptive filename using hyphens: `my-new-post-title.md`

### Required Frontmatter

Every post must start with this YAML frontmatter:

```yaml
---
authors:
  - hjaveed
hide:
  - toc
date: YYYY-MM-DD
readtime: X
slug: your-post-slug
comments: true
---
```

- `date`: Publication date in YYYY-MM-DD format
- `readtime`: Estimated minutes to read
- `slug`: URL-friendly identifier (used in post URL)

### Post Structure

```markdown
---
authors:
  - hjaveed
hide:
  - toc
date: 2025-01-15
readtime: 5
slug: my-post-slug
comments: true
---

# Post Title

Opening paragraph that hooks the reader.

<!-- more -->

Rest of the content goes here after the fold marker.

## Section Heading

Content...
```

The `<!-- more -->` marker separates the excerpt (shown on blog index) from the full content.

### Adding Images

1. Place images in `docs/assets/`
2. Reference them with relative paths from the post:

```markdown
![Alt text](../assets/your-image.png)
```

### External Links

Open external links in new tabs using this syntax:

```markdown
[Link text](https://example.com){:target="\_blank"}
```

## Writing Style Rules

**CRITICAL: Never use typographic dashes.** Do not use:

- En dash (–)
- Em dash (—)
- Any Unicode dash variants

Always use the standard ASCII hyphen-minus (-) for all dashes in content.

### Tone

- Concise and direct
- First person, conversational
- Avoid unnecessary verbosity
- Use short paragraphs
- Include practical examples and code snippets where relevant
