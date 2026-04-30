---
name: claude-design-diagram
description: Generate clean dev-blog flow diagrams (orchestrator/agent flows, architecture, sequences) as HTML, render to PNG via headless Chrome, embed into a markdown post. Uses a consistent warm-cream aesthetic with sharp typography and one accent color so all diagrams in the blog feel like a family. Trigger on "/claude-design-diagram", "create a diagram", "generate a flowchart", "make a flow diagram for blog", or when a markdown post has `<add-diagram>` style placeholders.
---

# claude-design-diagram

Use this skill when the user wants a polished diagram for a blog post, slide, or social share. The output is a static PNG (1600x900) generated from a hand-written HTML file. The HTML source is kept in the repo so the diagram can be edited and re-rendered later.

## When to use this

- The user asks to "generate a diagram", "create a flowchart", "make a flow diagram", "draw an architecture diagram", or anything similar for a blog post or content piece.
- A markdown post has placeholder text like `<add-diagram-here>`, `[diagram TODO]`, `.... add diagram later ...`.
- The user references this skill explicitly (`/claude-design-diagram`).

Do NOT use this skill for:
- Live mermaid diagrams (just write a fenced ```mermaid block).
- Animated/video output (use `claude-design-compose` + `claude-design-render`).
- Hand-drawn aesthetics like Excalidraw — this skill is intentionally clean/typeset, not sketchy.

## Output contract

Each diagram produces three artifacts:

1. **HTML source** at `docs/assets/diagrams/src/<slug>.html` — editable, diffable.
2. **PNG render** at `docs/assets/diagrams/<slug>.png` — 1600x900, used in markdown.
3. **Markdown reference** in the target post:
   `![alt text](../assets/diagrams/<slug>.png)`

If the diagrams live in a different repo, mirror the same structure under that repo's assets.

## Design system (do not improvise)

Consistency across diagrams matters more than novelty. Always use these values.

```css
--bg: #faf8f3;        /* warm cream page background */
--card: #ffffff;      /* default node fill */
--ink: #1a1916;       /* primary text */
--muted: #8a8580;     /* secondary text, meta lines */
--line: #d8d2c4;      /* default borders */
--accent: #c2410c;    /* burnt orange — primary, lines, arrows */
--accent-bg: #fef3e6; /* primary node fill */
--good: #15803d;      /* positive paths (yes branches, ship) */
--good-bg: #ecfdf5;
--bad: #b45309;       /* negative paths (no branches, alerts) */
```

Typography:

- Headings + node names: `Inter`, weights 400/500/600/700, `letter-spacing: -0.02em` on titles.
- Labels, meta, code: `JetBrains Mono`, weight 400/500/600, lowercase preferred for that handcrafted feel.
- Step indicator (top-left of every page): `STEP 0X / 0Y · NAME`, mono, uppercase, 12px, `letter-spacing: 0.18em`, accent color.

Layout:

- Page: exactly 1600x900 (matches Twitter card and renders crisp on mkdocs at 1x and 2x).
- Padding: `60px 80px`.
- Title: 44px, weight 600.
- Subtitle: 19px, muted, max-width 760px.
- Nodes: 14px border-radius, 1.5px border, 18-22px padding.
- Primary nodes: 2px accent border, accent-bg fill, accent-colored title.
- Arrows: SVG paths with `stroke-width: 1.5–1.8`, `marker-end` arrowheads. Use accent for primary flow, good/bad for branches.
- Tags/annotations: small mono pills with dashed borders for asides.
- Branding strip in bottom-right: `<series-name> · 0X` in mono, 11px, muted.

## Workflow

When the user asks for diagrams:

1. **Clarify scope** in one sentence if unclear: how many diagrams, what does each show, what post are they for. Skip if obvious.

2. **Pick slugs** — `01-breadth.html`, `02-depth.html`, etc. Use a numeric prefix when there's a sequence; use a descriptive slug otherwise (`auth-flow.html`).

3. **Write the HTML** — copy `template.html` as the starting scaffold. Replace the step indicator, title, subtitle, and the `<div class="canvas">` body. Use absolute positioning + inline SVG for arrows (it's the cleanest way to get pixel-precise layout at 1600x900).

4. **Render** with `render.sh`:
   ```bash
   .claude/skills/claude-design-diagram/render.sh <slug>
   # or render all:
   .claude/skills/claude-design-diagram/render.sh --all
   ```

5. **Verify** — Read the resulting PNG. Common issues:
   - Arrowheads landing inside boxes → shorten the SVG path by 8–10px.
   - Text overflowing nodes → either shorten the text or widen the node.
   - Lines crossing labels → reposition or curve the path.

6. **Embed** in the target markdown post with a descriptive alt:
   ```markdown
   ![Breadth first: orchestrator forks across 3 repos](../assets/diagrams/01-breadth.png)
   ```

## Composition principles

When designing the actual diagram:

- **One idea per diagram.** If you're tempted to add a second concept, that's a second diagram.
- **Lead with a sentence-style title.** "Plan once. Fork wide." is better than "Breadth First Phase".
- **Use the subtitle to name the takeaway**, not to summarize the diagram.
- **Annotate sparingly.** One or two pill tags per diagram is plenty; more becomes noise.
- **Prefer 3-5 nodes.** Reach for 6+ only when the structure (e.g. an MCP cluster) genuinely requires it.
- **Asymmetry > symmetry.** Symmetrical layouts feel auto-generated. Offset things slightly.
- **Direction matters.** Left→right for time/flow. Top→bottom for hierarchy/forking. Pick one and stick to it within the diagram.

## Cross-platform notes

PNGs work everywhere — MkDocs, Substack, Twitter, LinkedIn, GitHub. Mermaid does NOT render on Substack, which is why this skill outputs raster images. Keep the HTML source in the repo so you can edit and re-render rather than starting from scratch.

## Files in this skill

- `SKILL.md` — this file.
- `template.html` — starter scaffold with the design system baked in. Copy it for each new diagram.
- `render.sh` — headless Chrome screenshot helper. Pass a slug or `--all`.

## Reference examples

Finished diagrams from past posts live in the blog itself, not duplicated here:

- `docs/assets/diagrams/src/01-breadth.html` — orchestrator forks into 3 forks (top-down hierarchy)
- `docs/assets/diagrams/src/02-depth.html` — single-fork zoom with dimmed siblings + checklists (left-right with side panels)
- `docs/assets/diagrams/src/03-vet.html` — decision diamond with yes/no branches and dashed loop-back
- `docs/assets/diagrams/src/04-loop.html` — production → MCP cluster grid → orchestrator with curved feedback loop

Read these when picking a layout — most diagram requests will resemble one of these patterns. Copy the closest one as a starting point rather than the blank `template.html` when the structure overlaps.

## Quick start (typical session)

```bash
# 1. Copy the closest existing example or the template
cp docs/assets/diagrams/src/01-breadth.html docs/assets/diagrams/src/my-new-diagram.html

# 2. Edit the new file: title, subtitle, nodes, arrows
#    (Claude does this directly via Edit tool)

# 3. Render
.claude/skills/claude-design-diagram/render.sh my-new-diagram

# 4. Review docs/assets/diagrams/my-new-diagram.png
#    Iterate by re-editing the HTML and re-running render.sh

# 5. Embed in markdown
#    ![alt text](../assets/diagrams/my-new-diagram.png)
```
