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

# Open Sourcing Byaan, Your Company's AI Data Analyst

Today I am open sourcing [Byaan](https://github.com/byaan-ai/byaan){:target="\_blank"}, a small AI data analyst that runs close to your database and answers the long tail of "can you pull this real quick?" questions that pile up at every startup.

About ten startups are already using it day to day. I quietly shared it with founder friends over the last few months, and the same pattern kept showing up: their customer success and ops teams stopped pinging engineering for one-off data questions, and engineering got hours back every week.

<video autoplay muted loop playsinline controls style="width: 100%; max-width: 100%; border-radius: 8px; margin: 1.5rem 0;">
  <source src="https://github.com/user-attachments/assets/ccaea2b4-ed92-4bb7-b5df-0218bac5b63c" type="video/mp4">
  Your browser does not support the video tag.
</video>

<!-- more -->

At [RevelAI](https://www.revelaihealth.com/){:target="\_blank"}, where this started, our customer success team now answers most of their own questions through Byaan. Client health, patient engagement, satisfaction trends, contract usage, the weird one-off "why did this account drop last week" stuff. All of it used to land in an engineer's lap. Now it does not.

That is the whole pitch. The rest of this post is how it works and why I think the open source version is worth your time.

## The Problem Every Startup Hits

You do not need a data platform on day one. You need an engineer who can write SQL.

That works until it does not. The schema grows. Metrics get company-specific meanings. Customer success needs an answer before the call at 3pm. Engineers slowly become the query interface for the whole company.

BI dashboards solve part of this, but only part. Dashboards are great for stable metrics people look at every day. They are terrible for the long tail. Someone asks about one client, one cohort, one contract, one odd edge case. You do not want to build a dashboard for every question, and you do not want every non-technical teammate waiting on an engineer for a one-off query.

## Why Text-to-SQL Alone Falls Over

A model can generate decent SQL when the schema is small and table names are obvious. Real databases are messier. Tables have history. Columns are named after old product decisions. Metrics have meanings that only exist in code, Slack, and people's heads.

At RevelAI, an "active customer" is not just a row in a customers table. Some clients are pilots. Some are churned but still have data. Some get excluded from internal metrics for billing reasons. Raw text-to-SQL does not know any of that. It sees tables and guesses.

The model was rarely the bottleneck. The harness around the model was.

## What I Tried First

The obvious moves did not fit:

- **[Julius](https://julius.ai){:target="\_blank"}, [Hex](https://hex.tech){:target="\_blank"}, and the warehouse-native data agents.** Good products. Jason Cui at a16z had a [good post on X](https://x.com/JasonSCui/status/2031371431129526446){:target="\_blank"} mapping the data agent landscape if you want the full picture. For us, most of them felt too heavy for a 20-50 person company, and they introduce more cloud surface area than I wanted. I did not want to hand a third party broad access to production if I could avoid it.
- **Point Claude Code at the database.** Two problems. First, security. Prompting an agent to "please do not DROP TABLE" is not a real safety layer. Second, transparency. A CLI is fine for engineers. It is not the right surface for a customer success teammate asking five questions before a renewal call.

So I built the thing in the middle.

## What Byaan Actually Does

Byaan sits between a CLI and a SaaS:

- A small agent harness built on the OpenAI Agents SDK
- A read-only wrapper that blocks DDL and DML at the execution layer, so the agent is physically incapable of mutating your database, no matter what the model decides to do
- A UI that shows the generated SQL, the result, the chart, and lets you correct the agent inline
- A memory layer that learns your schema, your joins, your metric definitions, and the mistakes it made yesterday
- A Mac app for individual use, Docker for teams, and an MCP server so developers can use it directly from Claude Code or any MCP-aware client

Your database connection stays on your infrastructure. Only query results and relevant schema context go to whatever model provider you configure.

The loop is the thing that matters. When the agent gets something wrong, the correction becomes part of the system. Tribal knowledge slowly stops being tribal.

## Why I Open Sourced It

Honestly, I wanted to solve my own problem at Revel first. Running tens of ad-hoc queries every day is no fun, and watching our team wait on engineering for answers was less fun. I teamed up with two engineers who shared the same itch, Usama and Soha, and we started building it on the side.

Once it was working for us, founder friends kept asking for it. Shipping a private build to ten different companies is not a thing I want to maintain. And honestly, this should not be a SaaS. The whole point is that your database connection and your schema context stay yours. Open source is the honest version of that promise. If you do not trust the harness, read the code. If something is missing, send a PR.

The startups using it now are running the same code that is on GitHub. No special build, no hidden features.

## Try It

- Founders and ops teams: grab the [Mac app](https://www.byaan.ai){:target="\_blank"} and point it at a read replica.
- Developers: run it with Docker, or wire up the MCP server and use it from Claude Code.
- Either way, the repo is [github.com/byaan-ai/byaan](https://github.com/byaan-ai/byaan){:target="\_blank"}. Stars help, issues help more.

I would especially appreciate blunt feedback from people who have tried agents against real databases. Where it feels useful, where it feels fragile, what would make you trust it more. [Open an issue](https://github.com/byaan-ai/byaan/issues){:target="\_blank"} or message me directly.
