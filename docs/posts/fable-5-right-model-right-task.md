---
authors:
  - hjaveed
hide:
  - toc
date: 2026-07-06
readtime: 4
slug: fable-5-right-model-right-task
comments: true
---

# The LLM Router Era Starts with Fable 5

Fable 5 is the most incredible model I have used. Not a nicer version of the last one. Another level of increment in capability.

But that is not the part that stuck with me. After days of heavy use, the thing I keep noticing is not what Fable does. It is what Fable chooses not to do itself.

It delegates. And it is good at it. That is the first real glimpse of something I have been waiting for: the LLM router era.

<!-- more -->

## What actually makes Fable different

Benchmarks will not tell you this. What you feel in practice is judgment:

- It holds a long thread without drifting
- It knows when a task deserves its full attention and when a cheaper model can grind through it
- It verifies work instead of declaring victory

That last one is the unlock. A model you can trust to check other models' work is a model you can put in charge.

## Your subscription is a loss leader

Here is the uncomfortable math. Anthropic and OpenAI are subsidizing most of the model usage happening today. You are not paying what your tokens cost.

That does not last. I believe the next generation of best-in-class models will be metered by API usage. They will not live comfortably inside any subscription under $200. The frontier is getting too expensive to hand out flat-rate.

![The subsidy runs out: subsidized era vs metered era](../assets/diagrams/rmrt-01-metered-era.png)

When that happens, "use the right model for the right task" stops being a power-user trick. It becomes the only economics that make sense. Paying frontier prices for grunt work will feel like hiring a staff engineer to rename variables.

## Everyone claims routing. Nobody has it.

We are so early in this. One of these days there will be a router model capable enough to look at a task and send it where it belongs: frontier for judgment, mid-tier for implementation, cheap or open source for bulk mechanical work.

Plenty of software factory products claim they have this down already. I have not seen Devin, Droid, or any of the others truly nail it.

Fable gave me the first glimpse. Not because it routes across vendors out of the box, but because it finally has the judgment to know what to keep and what to hand off. The router was never going to be a traffic cop with a lookup table. It was always going to be the smartest model in the room.

## My setup right now

Fable is the orchestrator. It holds the plan, the context, and the taste. Everything else is a worker:

- Codex (gpt-5.5) for well spec'd execution, computer use, and UI/UX verification. It is still WAY better at driving a browser and checking visual work
- Opus 4.8 or Sonnet 5 for focused implementation forks and reviews
- Kimi 2.7 or GLM 5.2 if you are running an open source setup

![One brain, many hands: Fable orchestrates, cheaper models execute](../assets/diagrams/rmrt-02-delegation.png)

[Theo](https://x.com/theo){:target="\_blank"} has been minmaxing exactly this, and his CLAUDE.md is the best concrete version I have seen. He scores every model on cost, intelligence, and taste, then routes accordingly: bulk mechanical work to gpt-5.5 because it is effectively free on his plan, anything user-facing to models with taste, reviews to Fable or Opus.

![Theo's model routing CLAUDE.md](../assets/theo-model-routing-claude-md.png)

The result, in his words: he was throwing away about 50% of his end-to-end agent-driven PRs before this workflow. After it, he did not close a single one. Read his [strategy post](https://x.com/theo){:target="\_blank"}.

My favorite rule from his setup: the rankings are defaults, not limits. If a cheaper model's output misses the bar, escalate without asking. Judge the output, not the price tag. Escalating costs less than shipping mediocre work.

## Add loops and it compounds

Routing decides who does the work. Loops decide when it happens. I wrote about this in [Agent Workflows & Loops](agent-workflows-and-loops.md), and Anthropic just published a solid primer on [getting started with loops](https://x.com/ClaudeDevs/status/2074208949205881033){:target="\_blank"}.

Put the two together and you get the shape I think this job is settling into:

![Judgment stays expensive, execution gets cheap: orchestrator, routing, and loops](../assets/diagrams/rmrt-03-compounding.png)

The orchestrator keeps the context warm. Cheap models grind through the passes. Loops keep everything moving while you sleep. Your attention goes to product calls and the weird edge cases, not to being the cron job for your own codebase.

## The new shape of the job

Fable is the first model where delegation feels less like a workaround and more like the architecture. The frontier model becomes the staff engineer you pay a premium for, managing a team of cheaper, faster, good-enough models.

Judgment stays expensive and centralized. Execution gets cheap and distributed. That is the LLM router era, and we are just getting the first glimpse of it.

It is also the most fun I have had building in years.
