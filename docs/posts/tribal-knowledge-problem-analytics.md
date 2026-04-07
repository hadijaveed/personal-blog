---
authors:
  - hjaveed
hide:
  - toc
date: 2026-04-07
readtime: 10
slug: tribal-knowledge-problem-analytics
comments: true
---

# The Tribal Knowledge Problem Nobody Is Solving for Analytics

Your AI can write SQL. It just has no idea what the data means.

I have spent the last four years building AI products in healthcare. Our databases have columns like `amt_1`, `stat_cd`, `eff_dt`. A model looking at raw schema has no way to know that `amt_1` is patient copay in one table and coinsurance in another. That `stat_cd` means enrollment status, not statistical code. That `eff_dt` is the date a policy became active, not when something happened.

This is tribal knowledge. It lives in the heads of the three people who built the database. It is not documented anywhere. And it is the reason text-to-SQL fails in production.

<!-- more -->

## The numbers tell the story

The Spider benchmark, the industry standard for evaluating text-to-SQL, reports 86% accuracy. Sounds great until you look at Spider 2.0, which uses real enterprise schemas instead of clean academic ones. The accuracy drops to 6%.

That gap is not about the model being dumb. It is about context.

Here is how accuracy scales with context:

- Raw schema alone: 10-20%
- With relationship mapping: 20-40%
- With a catalog or data dictionary: 40-70%
- With a semantic layer: 70-90%
- With tribal knowledge encoded: 90-99%

GPT-4 on raw schemas achieves 16.7% accuracy. Add a semantic layer and it triples to 54.2%. The model is not the bottleneck. Context is.

## The "plausible but wrong" problem

This is what makes tribal knowledge dangerous to ignore. The AI does not fail loudly. It fails confidently.

A logistics retailer ran into this: their BI dashboard showed 98% on-time delivery. An AI agent querying the same raw tables reported 92%. Both were running correct SQL. The difference was that the BI tool excluded "customer-waived delays," a filter that existed only in the dashboard logic, not in the database. The AI had no way to know that filter existed.

The SQL was syntactically perfect. Semantically, it was wrong. And the person reading the result had no way to tell.

An ex-Amazon engineer put it bluntly: "At Amazon we had a text-to-SQL homegrown to understand our table schema, and most of the time it would break as old tables got sunsetted for new ones. AI SQL is useless without a comprehensive understanding of the data."

## The math that kills self-service analytics

Even if you solve the tribal knowledge problem for a single query, there is a compounding problem nobody talks about enough.

90% accuracy per query sounds great. But run 10 queries in an analytical session and the probability that all 10 are correct drops to 35%. Run 20 queries and you are at 12%.

For a data engineer reviewing output, this is manageable. For a PM running self-service analytics with no SQL knowledge, this is a trust problem that makes the tool useless within a few sessions.

Confidence scoring matters more than raw accuracy. The tool needs to tell you when it is uncertain. "I am 95% confident this is right" is useful. "Here is your answer" with no qualification is dangerous.

## Why the standard fix does not work

The industry answer is: build a semantic layer. Define every metric, every column, every relationship upfront. Then point your AI at the semantic layer instead of raw tables.

Hex is doing this well with Semantic Authoring. Teams define measures, dimensions, and joins directly inside Hex. The semantic context becomes "instructions for use" for the data, and the AI generates queries against those curated definitions instead of raw tables. Snowflake has Semantic Views. dbt has its Semantic Layer via MetricFlow. Cube does it too.

These work. Semantic layers improve query accuracy by up to 300%.

But there is a catch. Building a semantic layer is expensive. It takes a dedicated data team, often months of work, and constant maintenance. For a company with 10 data engineers and a mature data stack, this is feasible. For everyone else, the cost of building the semantic layer negates the benefit of having AI analytics in the first place.

One BI practitioner described it well: tools that require a semantic layer are "not that much better or faster than asking someone for a new dashboard." You have replaced one bottleneck with another.

Gartner estimates 40% of agentic AI projects will be abandoned by 2027 due to poor integration. The semantic layer tax is a big part of why.

## What the solution actually looks like

The missing piece is not smarter models or bigger semantic layers. It is a system for capturing, validating, and evolving tribal knowledge as a living artifact.

Andrej Karpathy pointed the way recently with his LLM knowledge base approach. The idea: instead of training models, build structured knowledge in markdown files that any AI agent can read. Raw material goes in, the LLM writes encyclopedia-style articles for each concept, creates backlinks, and maintains an index. The human's role is not writing the knowledge but writing and refining the schema that instructs the AI on how to interpret it.

Apply this pattern to analytics and you get something powerful: org-level data skills.

Think of a data skill as a markdown file that encodes what a column means, what a metric definition is, what filters should always be applied, what relationships exist between tables. Not a full semantic layer built by engineers over months, but a living document that grows from actual usage.

DataRecce captured this idea precisely: "The fix is not waiting for a smarter model. AI skills are markdown files that encode domain knowledge into coding tools. No framework, just files."

## The codebase already knows what the schema does not

Here is what every approach so far gets wrong: they treat the database in isolation. But the application code already encodes tribal knowledge. Your controllers validate which fields are required. Your models define relationships between tables. Your API layer names things in human-readable terms that the schema never bothered to.

A column called `stat_cd` is meaningless in a schema. But if the codebase has an enum mapping `stat_cd` to `ACTIVE`, `SUSPENDED`, `TERMINATED` with validation logic around each state, that is the tribal knowledge you need. Existing dashboards and notebooks encode it too. Every Metabase query, every Jupyter notebook, every dbt model is a record of how humans actually interpret the data.

The agent should read all of this. Not just the schema. The codebase, the dashboards, the notebooks, the API contracts. This is the real context source.

## Solving the cold start problem

Progressive learning is the right long-term approach, but it has a cold start problem. Session 1 is terrible if the agent starts from zero.

The fix is an init process, similar to how Claude Code indexes a codebase on first run. Point the agent at your repo, your existing dashboards, your notebooks. It crawls them, extracts column usage patterns, metric definitions, relationship mappings, and filter logic. It proposes an initial set of org-level data skills based on what it found. A human reviews and approves.

Day one accuracy jumps from 10% to 60-70% before a single user query. That is the difference between a tool people abandon after one session and a tool they keep using.

## From individual memory to organizational knowledge

The real unlock is making tribal knowledge collaborative and governed.

When a senior analyst knows that "revenue" means net-of-returns for the finance team but gross for the sales team, that knowledge lives only in their head. When they leave, it leaves with them.

What should happen instead:

1. The AI encounters an ambiguous column or metric
2. It flags the ambiguity and asks the user to clarify
3. The user provides the correct interpretation
4. That fact gets proposed as a knowledge contribution, not immediately committed
5. A data steward reviews and approves it
6. Once approved, it becomes part of the org-level knowledge base that every future query benefits from

This is not session memory. This is a governed knowledge layer with a review process. Like a pull request for data definitions.

The system should also auto-research. When a new table appears, a column gets renamed, or a migration changes relationships, the agent should detect the drift, cross-reference existing skills, and propose updates. Not silently break. Not wait for someone to notice three weeks later.

## What this means

The companies that figure out tribal knowledge will win the AI analytics market. Not because their models are smarter, but because their context is richer.

The current landscape: enterprise incumbents are bolting AI onto pre-generative architectures. Cloud startups are building real semantic layers but requiring cloud access to your data. Open-source tools are getting the architecture right but lack the knowledge layer.

The gap is a tool that bootstraps from your codebase and dashboards, accumulates knowledge progressively through usage, governs that knowledge with an approval process, auto-researches schema drift, and keeps data local.

The pieces exist. Karpathy showed the knowledge architecture. Hex showed how semantic layers power AI queries. The MCP ecosystem showed how agents connect to databases locally. What is missing is the system that ties them together.
