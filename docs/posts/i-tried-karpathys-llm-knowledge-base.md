---
authors:
  - hjaveed
hide:
  - toc
date: 2026-04-15
readtime: 4
slug: i-tried-karpathys-llm-knowledge-base
comments: true
---

# I Tried Karpathy's LLM Knowledge Base. Here Is What Actually Worked.

Like many of you, [this tweet from Andrej Karpathy](https://x.com/karpathy/status/2039805659525644595){target=\_blank} is what pushed me to actually try this. The whole post is worth reading, but the core idea:

<!-- more -->

> Raw data from a given number of sources is collected, then compiled by an LLM into a .md wiki, then operated on by various CLIs by the LLM to do Q&A and to incrementally enhance the wiki, and all of it viewable in Obsidian. You rarely ever write or edit the wiki manually, it's the domain of the LLM.

That last sentence is the key. The wiki is the domain of the LLM. You do not write it. You do not maintain it. The LLM compiles raw sources into structured knowledge, maintains backlinks, categorizes data into concepts, writes articles for them, and links them all together. Karpathy even runs LLM "health checks" over the wiki to find inconsistent data, impute missing information, and suggest new connections. His wiki grew to around 100 articles and 400K words, and he found that plain LLM grep over index files and summaries worked fine without reaching for fancy RAG.

He closed the post with: "I think there is room here for an incredible new product instead of a hacky collection of scripts." I agree, but I also think the hacky collection of scripts version is underrated. You do not need a product. You need a set of instructions and an LLM that follows them.

This resonated because I had just opened Apple Notes looking for something about a client project and ended up scrolling through pages of content from a company I left two years ago. Launch dates that already passed. Candidate notes for people I hired eight months ago. Project plans for features that shipped, got killed, or morphed into something unrecognizable. The notes were not wrong when I wrote them. They are wrong now because nobody updated them.

I have tried Notion and many other apps. Every system worked for about three weeks, then slowly became another graveyard of outdated context I could not trust. The common failure mode is always the same: these tools assume the human will maintain the notes. The human will not maintain the notes. You have better things to do.

The problem was never capture. Every app on the planet solves capture. The problem is maintenance. Notes rot the moment you write them, and the rot accelerates the more you have.

So I built something different. I built a system where an LLM maintains the notes and I just talk to it.

## Dreaming Creates Slop

Garry Tan built [gbrain](https://github.com/garrytan/gbrain){target=\_blank} on similar principles to Karpathy's approach which is a great attempt. A heavier implementation with more automation, more integrations, more always-on capture. The "dreaming" model: your system monitors all your signals (emails, Slack, meetings, documents) and auto-captures everything into structured knowledge.

I tried variants of the autonomous approach and it creates slop. The system generates pages you never asked for. It indexes things that do not matter. It captures the noise alongside the signal and you end up with a knowledge base that is technically comprehensive and practically useless. The context-free auto-generated page about a throwaway Slack thread is no better than the notes you already ignore.

Nobody has solved passive capture well yet. The models are getting smarter, but the fundamental problem remains: without human intent, the system does not know what matters. A meeting transcript is not knowledge. A Slack thread is not a learning. An email chain is not a project update. These things become knowledge only when a human decides they are worth remembering.

So I went the other direction. I talk to the agent like a personal EA. I say `/remember met with Christian about Q2 priorities` and the system figures out the rest. It classifies, stores, cross-links, and updates the index. The human provides focus. The LLM provides execution.

This is a deliberate design choice, not a limitation. I took the key insight from Karpathy (the LLM is the writer, the human is the curator) and stripped away everything else. No database. No application code. No always-on monitoring. Just markdown files, a 318-line instruction document called CLAUDE.md, and a set of Claude Code skills that operate on the files. I use Obsidian to look at my notes.

## Compiled Truth, Not Append-Only Notes

The core pattern that makes this work is something I call compiled truth. Traditional notes are append-only. You write something, time passes, you write something else, and now you have two entries that may or may not agree with each other. Multiply that by a hundred and you have a knowledge base where the truth about any topic is scattered across twelve different notes written at different times with different (often contradictory) context.

Compiled truth solves this by giving every entity page two zones, separated by a horizontal rule:

1. Compiled truth (above the line): the current best understanding. Rewritten entirely when new information arrives.
2. Timeline (below the line): append-only, reverse-chronological evidence trail. Never edited, only prepended.

Here is the template:

```markdown
---
title: Page Title
type: person | project | concept | learning
tags: [relevant, tags]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

Compiled truth goes here. Plain prose, not bullet soup. This is the
current best understanding of this entity. Rewrite completely when
significant new information arrives.

---

## Timeline

- YYYY-MM-DD: Most recent event or evidence. Source or context.
- YYYY-MM-DD: Earlier event.
```

The compiled truth paragraph is the synthesis. If I learn something new about knowledge management next week, the LLM rewrites that paragraph to incorporate the new information. It does not append a second paragraph. It does not create a "Knowledge Management (2)" page. It rewrites the truth.

The timeline below is the evidence trail. Append-only, reverse-chronological. You never edit past entries. This gives you an audit log of how your understanding evolved without cluttering the current synthesis.

Think of it like a Wikipedia article with a changelog. The article always reflects the latest understanding. The changelog tells you how it got there. Except the LLM is the editor and you are the one submitting evidence.

When new content comes in, the system classifies it using a decision tree I call the MECE resolver:

```
1. Is it a task/todo?                    -> Prepend to tasks.md
2. Is it a URL/article to save?          -> Prepend to bookmarks.md
3. Is it a blog idea?                    -> Prepend to blogs.md
4. Is it a fact or insight learned?      -> Create learnings/<slug>.md
5. Is it about a specific person?        -> Create/update people/<name>.md
6. Is it about a specific project?       -> Create/update projects/<slug>.md
7. Is it about a topic or technology?    -> Create/update concepts/<slug>.md
8. Is it a daily observation?            -> Append to today's entry in journal.md
```

If something spans multiple categories ("I learned X from person Y about project Z"), the system creates entries in all relevant places and cross-links them with Obsidian wiki-links. This creates a knowledge graph without a database. Every entity page links to related entities, and those links are maintained by the LLM every time it touches a page.

## The Instructions Are the Product

Here is the part that surprised me. The entire system is one instruction file and six skills. There is no application code. No API. No database. No build step. The "product" is a markdown document that tells the LLM how to behave.

The first three lines of my CLAUDE.md:

```
A markdown-based personal knowledge base maintained by Claude Code.
You (the LLM) are the primary writer and maintainer. The human
directs, curates, and reads.
```

That is the entire philosophy in three sentences. The rest of the 318 lines define the directory structure, entity page format, classification logic, cross-linking rules, and style rules. Here is the directory structure:

```
personal-os/
├── _index.md         # Master index, one-line summaries
├── tasks.md          # Single file, checkboxes, prepend at top
├── bookmarks.md      # Single file, read/unread checkboxes
├── learnings/        # One .md per learning
├── journal.md        # Single file, daily entries
├── blogs.md          # Single file, blog idea tracker
├── blogs/            # One .md per blog post being developed
├── people/           # One .md per person
├── projects/         # One .md per project
├── concepts/         # One .md per topic/technology
├── inbox/            # Drop zone for raw inputs
└── raw/              # Archived source material after processing
```

The skills layer sits on top. Six slash commands that trigger specialized operations:

- `/remember` - store new information
- `/recall` - query the knowledge base
- `/todo` - task management
- `/brain` - health check for stale pages, orphans, dead links
- `/ingest` - process raw files from the inbox
- `/brief` - daily status summary

Each skill is a focused instruction set. Here is the `/remember` skill in its entirety:

```
You are the memory engine for a personal knowledge base.

The user wants to remember something. Your job: classify it, store
it in the right place, cross-link it, and update the index.

Steps:
1. Read CLAUDE.md for format rules and classification logic.
2. Read _index.md to know what entities already exist.
3. Classify the user's input using the MECE resolver.
4. If the input spans multiple categories, create entries in all
   relevant places and cross-link them.
5. For entity pages: if existing, rewrite compiled truth with new
   info. If new, create with frontmatter + compiled truth + timeline.
6. Update _index.md if any entity pages were created.
7. Add [[wiki-links]] wherever you reference a known entity.
8. Confirm what you stored and where, in one short sentence.

Important:
- Never ask "what category?" Just figure it out from context.
- Use today's date for all entries.
- Keep it fast. Read index, classify, write, confirm.
```

That is the whole thing. No framework. No database. No Docker. Read the rules, read the current state, act, update the index. The same pattern for every operation.

If you have ever written a CLAUDE.md for a codebase, you already know how to build this. The same skill you use to instruct an LLM about your code applies to instructing it about your life. The instructions are the product.

## Bootstrapping in One Session

I bootstrapped the entire system from my existing Apple Notes in one session. I had one giant iPhone note where everything important was crammed. Six active consulting clients, a dozen ongoing projects at my primary job, personal finance items, blog ideas, people to keep track of. All in one note. When I needed to find something, I would Cmd+F through a wall of text.

I fed it to Claude Code and let the MECE classifier sort it. Out of that one messy note: 37 open tasks, 14 bookmarks, 8 learnings, 16 people pages, 12 project pages, 2 concept pages. All structured, cross-linked, and indexed.

The whole system lives in GitHub. Claude Code writes from any terminal. Obsidian auto-pulls from git on my laptop. Git is the sync layer, not Dropbox or iCloud. Full version history, works from any machine.

Does it scale? Plain markdown plus LLM grep handles up to roughly 400,000 words. That is the Harry Potter series. The `_index.md` master index acts as a routing table so the LLM rarely needs to read every file. If you somehow outgrow that, you need a database. You probably do not need a database.

## What I Would Tell You

This system is days old. The LLM makes classification mistakes sometimes. The compiled truth occasionally misses nuance. The real test is whether I am still using this in six months, not whether it works in the first week.

But here is what I know already. Most personal knowledge systems fail because the human stops maintaining them. This one might last longer because the human was never supposed to maintain it in the first place.

A knowledge base with 50 pages you trust is more useful than one with 5,000 pages you have never read. The LLM does the writing. You just have to keep talking to it.
