---
authors:
  - hjaveed
hide:
  - toc
date: 2026-05-28
readtime: 2
slug: claude-code-workflows
comments: true
---

# Claude Code Dynamic Workflows: A Fleet of Agents That Argue Before They Answer

Anthropic shipped Opus 4.8 today, and along with it Claude Code got dynamic workflows. I have been playing with it for a few hours and it is genuinely impressive.

<video autoplay muted loop playsinline controls style="width: 100%; max-width: 100%; border-radius: 8px; margin: 1.5rem 0;">
  <source src="https://github.com/user-attachments/assets/c9579cd8-54ef-4824-970f-29427278fddd" type="video/mp4">
  Your browser does not support the video tag.
</video>

<!-- more -->

You type "create a workflow," or you flip on "ultracode" in the effort menu, and Claude Code spins up hundreds of parallel agents that check each other's work. The unit of work you can hand off jumps from a single file to an entire codebase. Migrations, audits, rewrites, framework swaps, the stuff you used to plan in sprints, now finishes overnight.

The part that got me is that the agents argue with each other before they show you anything. Independent attempts at the same problem, then adversarial agents trying to break the answer, iterating until they converge. That is how a good senior team works. Except this team runs at 3am and never gets tired.

It also resumes. If a workflow gets interrupted, it picks up where it left off, so you can kick off work that runs for days, not sessions.

I went and read the Workflow tool definition inside Claude Code to see how it actually works. It is simpler than I expected. A workflow is just a JavaScript script. You write the control flow, the loops and the fan-out, in plain JS, and the agents do the model work. Three primitives carry most of it: `agent()` spawns one subagent, `parallel()` runs a batch and waits for all of them, and `pipeline()` pushes each item through every stage independently so the slow ones never block the fast ones. That is basically the whole thing.

Fair warning, this burns tokens fast. Anthropic says so themselves. But if the task is a migration that would have taken a team three months, spending a few hundred dollars to finish it in a week is the best trade in software.

None of the core idea is brand new, by the way. The recursive "a model spawns sub-model calls over a big problem" shape shows up in the [Recursive Language Models work](https://alexzhang13.github.io/blog/2025/rlm/){:target="\_blank"} out of MIT (Alex Zhang and Omar Khattab, late 2025). What is new is that it is now a button in the tool I already live in.

The ceiling on what one person can build just moved again. Going to be playing with this all week.
