---
authors:
  - hjaveed
hide:
  - toc
date: 2026-07-14
readtime: 5
slug: fable-5-without-the-token-anxiety
comments: true
---

# Fable 5 Without the Token Anxiety

Episode 3 of Build with Agents. Two things this time: the delegation setup that keeps my Fable 5 limits sane even when I am coding all day, and why I stopped using plan mode in favor of a living artifact.

> 🎥 **Watch the episode.** This is part of my Build with Agents video series. [Watch Episode 3 on Substack](https://hjaveed.substack.com/p/3-fable-5-without-the-token-anxiety){:target="\_blank"}.

<!-- more -->

## The best model, and the hungriest

We all felt it last December when Opus 4.5 launched. Everything you threw at it just felt right. It got your intent, it debugged well, it figured things out. And then no model gave me that feeling again, until Fable 5. This is a great time to be building.

The problem is Fable 5 consumes tokens aggressively. You live in constant token anxiety: "I am running out, I need more, this model is too good to stop using." And I think Anthropic will eventually move it to API-based pricing. Who knows when, but it is coming.

So the question becomes: how do you keep this level of intelligence available without burning through tokens?

## Plan big, execute small

The answer came from an Anthropic cookbook notebook: [Plan big, execute small](https://github.com/anthropics/claude-cookbooks/blob/main/managed_agents/CMA_plan_big_execute_small.ipynb){:target="\_blank"}. Plan with the big model, execute with smaller ones.

Most of an agent's token consumption is not deep reasoning. It is search and reading code. You do not need Fable-level intelligence for that. In this pattern, Fable stays the coordinator and spins up Sonnet 5 or Opus subagents that do the reading and report back. Anthropic's own measurements show you barely lose anything on benchmarks, because Fable is still the one in the loop making the calls.

And here is the part that makes it work: Fable 5 is the first model I have used that is genuinely good at delegating. I can tell it to hand backend tasks to Codex gpt-5.6 and frontend tasks to Opus 4.8, and it just does it well. It makes the plan, waits for the subagents to implement, reviews what came back, decides whether the loop is closed or needs another verification pass, then runs an adversarial review. GPT 5.6 is particularly good at that adversarial review step.

I have been running this for a week. I am coding a lot, and my limits are pretty sane: sitting at 40% usage where I would have run out in a couple of hours without the skill.

I wrote the full thesis, the router-era argument and the economics, in [The LLM Router Era Starts with Fable 5](https://hjaveed.substack.com/p/the-llm-router-era-starts-with-fable){:target="\_blank"}. This episode is the practice.

## Steal the skill

I fed the notebook to Fable 5 itself and had it craft a delegation skill, then kept using it over and over to hone it. To install it globally:

```bash
mkdir -p ~/.claude/skills/plan-big-execute-small
```

Then save the markdown below as `~/.claude/skills/plan-big-execute-small/SKILL.md`. For a single repo, put it in `.claude/skills/plan-big-execute-small/SKILL.md` at the project root. If you do not want a skill at all, paste the body into your `CLAUDE.md` and it works as standing instructions.

Two notes. If you do not have Codex CLI set up, remove the Codex section, although Fable is smart enough to skip it even if you leave it in. And the rules are mine: tune the model tiers to whatever plans you actually pay for.

````markdown
---
name: plan-big-execute-small
description: Cost-saving delegation harness based on Anthropic's "plan big, execute small" cookbook. Keep planning, judgment, and synthesis on the expensive main model (Fable); fan out mechanical token-heavy work (bulk file reads, code searches, web research, log trawls, per-item transforms, doc summarization) to Opus 4.8 subagents (default worker tier; Sonnet 5 allowed for rote volume, NEVER Haiku — quality floor set by Hadi). Also treat OpenAI Codex (gpt-5.6-sol, xhigh reasoning, via `codex exec`) as a peer work-agent for backend implementation, deep debugging, web research, and cross-vendor second opinions — it bills to the OpenAI plan, not Claude tokens. NO worktrees ever: all work happens in the main checkout, one writer at a time. Trigger when the user says "/pbes", "do this cheaply", "save tokens", "frugal mode", "delegate to codex", or when a task involves pulling large volumes of content (many files, many web pages, long logs) through the model.
---

# Plan Big, Execute Small

You (the main loop, running an expensive frontier model) are the **coordinator**. Your tokens cost 3–10x more than a subagent's. The single biggest cost driver in agentic work is _mechanical reading_ — files, web pages, logs, search results pulled into context. Move that reading onto cheaper workers; keep only planning, judgment, and synthesis here.

**Key insight from the cookbook:** the savings come from **rate arbitrage, not reading less**. Both approaches read roughly the same volume — the split team was 2.5x cheaper and 3x faster because 84–98% of input tokens were billed at the worker rate, and workers ran in parallel. Do NOT respond to cost pressure by skimping on rigor; respond by changing _who_ reads.

## Standing rules (Hadi's preferences)

- **NO worktrees, ever.** Not for you, not for Codex, not for subagents. All work happens in the main checkout, main thread. Worktrees are confusing — never call EnterWorktree, never pass `isolation: 'worktree'`, never `-C` Codex into a worktree.
- **One writer at a time** (this replaces worktree isolation): never let two things edit files simultaneously. When Codex implements, you don't touch files until it's done. When you implement, Codex runs read-only (`-s read-only`). Investigation subagents are read-only by nature — always safe in parallel.
- **Quality floor: never Haiku workers.** Opus 4.8 is the default worker tier; Sonnet 5 is allowed for truly rote high-volume reading.
- Hadi commits himself — don't commit unless he asks.

## Rate table (why this works)

| Model                   | Input $/M            | Output $/M        | Role                                                                                        |
| ----------------------- | -------------------- | ----------------- | ------------------------------------------------------------------------------------------- |
| Fable 5                 | $10                  | $50               | Coordinator: plan, decompose, verify, synthesize, review every diff                         |
| Opus 4.8                | $5                   | $25               | **Default worker**: reading, searching, web research, transforms, debugging                 |
| Sonnet 5                | $3 ($2 intro)        | $15 ($10 intro)   | Optional tier for truly rote volume reading                                                 |
| Codex gpt-5.6-sol xhigh | bills to OpenAI plan | ~$0 Claude tokens | **Peer work-agent**: backend implementation, deep debugging, web research, second opinions  |

Every token a worker reads instead of you is a 2–5x saving on that token (or ~free, for Codex). It also keeps your own transcript small, which compounds: your context is re-sent (cache-read billed) on every subsequent turn.

## Step 1 — Classify the work

Before acting, split the task into:

- **Judgment work** (stays here): understanding the ask, decomposing into sub-questions, deciding the approach, resolving conflicts between worker reports, verifying suspicious findings, reviewing diffs, writing the final deliverable.
- **Mechanical volume** (→ Opus subagents): anything where the _procedure_ is clear and the cost is in volume — read N files and report X, search the web for Y and return evidence, trawl logs for pattern Z, apply the same transform to each item, summarize each document.
- **Deep self-contained units** (→ Codex): one gnarly, well-specifiable problem — implement a backend module/endpoint/migration, root-cause a hard bug, a meaty research question, a design second opinion. Quality work, not volume work.

If the whole task is mechanical and small (one grep, one file read), just do it — delegation has a floor (see anti-patterns).

## Step 2 — Fan out with the Agent tool

Spawn workers with an explicit `model`, in parallel (one message, multiple Agent calls), in the background:

- `subagent_type: "Explore"` + `model: "opus"` — codebase searches and file-location sweeps.
- `subagent_type: "general-purpose"` + `model: "opus"` — web research, multi-file reading, per-item transforms, debugging.
- **Opus 4.8 is the default worker tier.** Drop to `model: "sonnet"` only for truly rote high-volume reading where reasoning doesn't matter. Never `model: "haiku"` (quality floor); never spawn `fable` workers (no arbitrage).

For large structured fan-outs (10+ items, multi-stage, verify passes) — and only when the user has opted into multi-agent orchestration — use the Workflow tool instead, with per-agent overrides: `agent(prompt, {model: 'opus'})` for worker stages; leave `model` unset (inherit) only for the final judge/synthesis stage. Never pass `isolation: 'worktree'`.

## Step 2b — Collaborate with Codex (peer work-agent)

OpenAI Codex CLI is installed and authenticated (`codex` on PATH, default model gpt-5.6-sol at xhigh reasoning). It's a **peer, not a subordinate**: strong at backend implementation, deep debugging, web research, and algorithmic work. It bills to Hadi's OpenAI plan — a Codex delegation costs ~zero Claude tokens (just your brief and its report).

**Invocation** (always via Bash, always `run_in_background: true` — xhigh takes minutes):

```bash
codex exec --skip-git-repo-check \
  -o /path/to/tmp/codex-report.md \   # final report → file; read ONLY that file
  -s read-only \                       # include whenever it must not edit files
  "<self-contained brief>" </dev/null
```

- `-o` / `--output-last-message` keeps its report out of your context until you choose to read it.
- `--output-schema schema.json` when you need structured JSON back.
- `-s read-only` for review/research/consult briefs; omit (workspace-write) only when Codex is the designated writer.
- It works in the **main checkout** (no worktrees) — which is why the one-writer rule above is load-bearing.
- Briefs follow the same discipline as Step 3: Codex sees nothing of your conversation, so the brief must carry the full spec, constraints, file paths, and acceptance criteria.

**Collaboration patterns:**

1. **Backend implementer** — you write the spec + acceptance criteria into the brief; Codex implements in the main checkout (you hands-off files meanwhile); you review with `git diff` and run verification. Hadi commits.
2. **Cross-vendor reviewer** — you implement, Codex reviews read-only (`codex exec review` inside a repo, or a "try to refute this diff" brief). Different model families catch different bugs.
3. **Research peer** — for meaty questions, fire Codex AND an Opus subagent on the same question in parallel, then triangulate. Two independent takes beat one.
4. **xhigh consultant** — gnarly bug or design decision: pack the evidence into a brief, let it reason deeply, judge its answer against your own read.

## Step 3 — Write worker briefs correctly

Workers know NOTHING you don't put in the prompt — not the conversation, not your plan, not the other workers' briefs. From the cookbook: "Everything the coordinator believes about its workers comes from its own system prompt." (This applies doubly to Codex, which is a different vendor entirely.)

Each brief must contain:

1. **One focused sub-question** — self-contained, no references to "the task above".
2. **Rigor instructions** — "try multiple query phrasings / search patterns, follow promising leads, cross-check across sources." Workers default to shallow; the brief supplies the rigor.
3. **An evidence-bearing report format** — require `file:line` references, URLs, verbatim quotes, exact values. You will verify from evidence, not by re-reading the sources yourself. Ask for structured findings (a list of facts + evidence), NOT polished prose.
4. **A size cap** — "report at most N findings / keep the report under ~500 words" so worker output doesn't flood your context.

## Step 4 — Synthesize and verify here

- Read only the reports. Do not re-read what workers already read — that pays the expensive rate twice and defeats the pattern.
- Review every diff (yours or Codex's) at the expensive rate — but only the diff, not the whole tree.
- Spot-check: if a finding is load-bearing and the evidence looks thin, send ONE targeted verification (a single file read, a cheap verify-subagent with a refute-this brief, or a read-only Codex cross-check) rather than redoing the sweep.
- Conflicting reports → resolve with judgment here, or spawn one tie-breaker worker with both claims and their evidence.

## Anti-patterns (from the cookbook's measurements)

- **Over-sharding.** Delegation has a floor: each worker pays a bootstrap cost (system prompt + brief + report). Narrowly-scoped micro-briefs _increased_ total cost in the cookbook's tests. A brief should represent at least several tool calls' worth of mechanical work. 3–6 meaty workers beat 20 tiny ones.
- **Delegating judgment.** Final synthesis, architecture decisions, security-sensitive conclusions, diff review, and anything needing the full conversation context stay on the main model. That's what the expensive tokens are _for_.
- **Two writers at once.** You and Codex (or any two writers) editing the same checkout simultaneously — there is no worktree isolation, so sequence it or make one side read-only.
- **Using Codex for volume.** Codex xhigh is slow and deep — wrong tool for "read these 40 files" (that's an Opus subagent's job); right tool for one hard, self-contained problem.
- **Prose reports.** Workers returning essays waste their output tokens and your input tokens. Demand structured findings + evidence.
- **Cutting rigor to cut cost.** A solo agent that "reads less" is a lower-rigor product, not a cheaper equivalent. Keep the rigor; move it to the cheap rate.
- **Doing the sweep yourself first "to understand it".** Scout minimally (list files, scope the diff — cheap), then delegate the heavy reading. Don't pull 50 files into your own context and then also spawn workers.

## Cheap-by-default habits (apply even without fan-out)

- Noisy investigation (grep sweeps, log trawls, broad search) → always a subagent; keep only the conclusion in the main transcript.
- Long web pages / docs → an `opus` worker fetches and distills; you read the distillation.
- A meaty self-contained question with no urgency → consider firing a background Codex run in parallel with your own work; its answer costs no Claude tokens.
- When the user asks for a quick answer, answer directly — this skill is for volume, not for adding ceremony to small tasks.
````

[Theo](https://x.com/theo){:target="\_blank"} runs a similar setup. He scores every model on cost, intelligence, and taste, and lets Fable 5 decide when to delegate what. Worth stealing ideas from both.

![Theo's model routing CLAUDE.md](../assets/theo-model-routing-claude-md.png)

## Stop using plan mode

Second thing from the video. I truly believe plan mode was created because models were not good enough. Sitting in a loop of planning, planning, planning, reading long documents before anything happens, is counterintuitive now. At least it was for me.

[Peter Steinberger](https://steipete.me/posts/just-talk-to-it){:target="\_blank"} made this argument way ahead of time in "Just Talk To It": do not ceremonialize planning, talk to the agent like you would talk to a pair programmer and iterate with it. So I start in auto mode and just chat.

The iteration is fun, but sometimes you want to see things visually: the plan, the design decisions, the architecture. This is where Claude artifacts changed my workflow. Instead of downloading HTML files and reopening them over and over, I ask Claude to maintain a single artifact of everything it is doing: every design decision, every architectural call, all the implementation details. I keep it open in a browser tab, refresh it, and iterate on top of it.

It matters most at review time. Agents write code really fast, and I do not want to be the bottleneck, developer ego and all. The best way to review is end to end: queue it up, ask the agent to help you review, have it generate component diagrams in the artifact, and move through the code quickly instead of pretending you will read every line.

That is the episode. Fable 5 plans big, cheaper models execute small, and the plan lives in an artifact instead of plan mode. More videos coming. Thank you.
