---
authors:
  - hjaveed
hide:
  - toc
date: 2026-05-18
readtime: 5
slug: byaan-agent-harness-for-data-queries
comments: true
---

# Byaan: An Agent Harness for Data Questions

2026 is the year of customized agent harnesses. Not generic chat. Not another SaaS with an AI button. Thin, opinionated agents wrapped around a specific job.

I just open-sourced [Byaan](https://github.com/byaan-ai/byaan){:target="\_blank"}, a local data agent harness I have been using daily for a few months and building all along. Site is at [byaan.ai](https://www.byaan.ai){:target="\_blank"}.

<!-- more -->

## Why Not Julius or Hex or purpose build tools for this

The honest answer is they are great products. Jason Cui at a16z had a [great post on X](https://x.com/JasonSCui/status/2031371431129526446){:target="\_blank"} mapping the data agent landscape, and there are good options out there.

But at [RevelAI](https://www.revelaihealth.com/){:target="\_blank"}, none of them fit. They felt too heavy for a 20-50-person company. There is a lot going on inside those tools, a lot of promise around semantic context and governance, and a lot of cloud surface area. I did not want to give a third party access to our production database if I could avoid it. Nothing against these tools, they are amazing and solve a specific need, but that need did not exist for us.

Meanwhile, Claude was already doing the hard parts for us. It could read the codebase. It could understand a Slack thread about which clients were churning. It could write the SQL. The model was not the bottleneck. The harness around it was.

## Why Not Warehouse Native Tools Like Snowflake

This is the other obvious question. If your data already lives in Snowflake, why not just use Snowflake Cortex or whatever warehouse-native AI ships next to it?

From what I have seen, the agent that lives inside the warehouse only knows the warehouse. It does not read your application code. It does not see the Slack thread where the team decided that "active customer" excludes free trials and any account flagged by billing. It does not learn over the months that "MRR" at our company is calculated a specific weird way for historical reasons.

That whole context layer is missing, unless something has changed very recently. And without it, you are back to text-to-SQL on raw schemas, which is the part AI is already worst at.

## Why Not Just Claude Code

The obvious next step is: skip the product layer, point Claude Code at the database, done.

Two problems with that.

One, security. There is no built-in guardrail stopping an agent from running `DROP TABLE` or a stray `UPDATE`. We have all seen the story about [Claude in Cursor wiping a production database](https://www.theregister.com/2025/07/22/replit_saastr_vibe_coding_incident/){:target="\_blank"}. Agents are confident. Production databases do not forgive confidence.

Two, transparency. Even when the SQL is technically correct, AI is not yet accurate enough to trust on the first try. You need a UI that shows the query, lets you inspect the result, and makes it easy to say "that is not what I meant" before that answer ends up in a board deck. A CLI is the wrong surface for that.

## So I Built the Middle

[Byaan](https://github.com/byaan-ai/byaan){:target="\_blank"} is what sits between a CLI and a SaaS.

- A thin harness built on the Agents SDK
- A read-only wrapper that blocks DDL and DML at the execution layer, so the agent is incapable of mutating your database
- A UI that shows the generated SQL, the result, the chart, and lets you correct the agent inline
- A basic semantic learning loop that picks up business context from the codebase and from how the team uses it, especially through Slack

It will not solve every tribal knowledge problem on day one. But it learns, and that compounds.

You can run it as a [native Mac app](https://www.byaan.ai){:target="\_blank"} for personal use, or as a single Docker container for your team. Database connections stay on your infrastructure. Only the query results and relevant schema context go to whichever model provider you configure.

## What Actually Happened

Byaan started as a hobby project with two engineer friends who wanted to build something real together. We had RevelAI problems to solve, so we used ourselves as the first customer.

Today most of our customer success team answers questions through Byaan: client health, patient engagement, satisfaction trends, contract usage. The agent has learned our schema, our metrics, and the weird tribal things that only the three people who built the database used to know.

Along the way I quietly gave access to a handful of fellow startup founders. About ten startups are now running Byaan daily.

## What Is Next

We will keep solving our own problems with it. That is the whole point.

If you want to try it, grab the Mac app or run it with Docker. If something feels off, [open an issue](https://github.com/byaan-ai/byaan/issues){:target="\_blank"} or message me directly. This is a hobby project built out of joy, and feedback is the most useful thing you can give us back.

Also, I am always hiring at [RevelAI Health](https://www.revelaihealth.com/){:target="\_blank"}. If you are looking, reach out.
