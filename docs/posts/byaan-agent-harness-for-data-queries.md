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

# Does Your Startup Need an AI Data Analyst?

Most startups do not need a full data platform on day one. But at some point, the same questions start showing up every week.

How many active customers do we have? Which accounts are slipping? Did patient engagement improve after the last release? Why did usage drop for this client?

For a while, the answer is simple: ask an engineer to write SQL.

<!-- more -->

That works until it does not. The schema gets bigger. Metrics get weird. Customer success needs answers now. Engineers become the query interface for the company.

I built [Byaan](https://github.com/byaan-ai/byaan){:target="\_blank"} because we kept running into this problem at [RevelAI](https://www.revelaihealth.com/){:target="\_blank"}. It is a small data agent harness that runs close to your database, learns your schema, shows its SQL, and stays read-only by default. The site is at [byaan.ai](https://www.byaan.ai){:target="\_blank"}.

## Why Not Just Use a BI Tool

BI tools are useful, and I am not arguing against them. Dashboards are still the right answer for stable metrics people look at every day.

The problem is the long tail of questions.

Someone asks about one client, one cohort, one workflow, one contract, or one odd edge case. You do not want to build a dashboard for every question. You also do not want every non-technical teammate waiting on an engineer for a one-off query.

This is where a data agent starts to make sense. Not as a replacement for BI, but as a better interface for questions that are too specific for a dashboard.

## Why Text-to-SQL Still Fails

The SQL is not the only hard part.

A model can generate decent SQL when the schema is small and the table names are obvious. Real databases are messier. Tables have history. Columns are named after old product decisions. Metrics have company-specific meanings. The right join is often not obvious from the schema alone.

At RevelAI, an "active customer" is not just a row in a customers table. Some clients are pilots. Some are churned but still have data. Some should be excluded from internal metrics for billing or contract reasons. That context usually lives in code, Slack, docs, and people's heads.

Raw text-to-SQL does not know that. It sees tables and guesses.

## Why Not Julius, Hex, or Purpose-Built Tools

There are good products in this space. Jason Cui at a16z had a [good post on X](https://x.com/JasonSCui/status/2031371431129526446){:target="\_blank"} mapping the data agent landscape.

For us, many of those tools felt too heavy for a 20-50 person company. They also introduced more cloud surface area than I wanted. I did not want to hand a third party broad access to our production database if I could avoid it.

The other issue was context. A warehouse-native or SaaS data tool may understand your warehouse. It usually does not understand your application code, your internal naming conventions, or the Slack thread where the team decided how a metric should work.

The model was not always the bottleneck. The harness around the model was.

## Why Not Just Claude Code

The obvious next step is to skip the product layer and point Claude Code at the database.

Two problems with that.

First, security. There should be a hard execution layer that prevents an agent from mutating the database. Relying on a prompt to stop `DROP TABLE`, `DELETE`, or a stray `UPDATE` is not enough. We have all seen stories about AI coding tools making destructive production changes.

Second, transparency. Even when the SQL runs, you still need to inspect it. You need to see the generated query, the result, the chart, and the assumptions before the answer ends up in a board deck or a customer conversation.

A CLI is great for engineers. It is not the right surface for a customer success or operations team asking data questions all day.

## What I Built

[Byaan](https://github.com/byaan-ai/byaan){:target="\_blank"} is what sits between a CLI and a SaaS.

- A small harness built on the OpenAI Agents SDK
- A read-only wrapper that blocks DDL and DML at the execution layer, so the agent is incapable of mutating your database
- A UI that shows the generated SQL, the result, the chart, and lets you correct the agent inline
- A lightweight memory layer that learns schema meaning, common joins, and mistakes over time
- A Mac app for individual use and a Docker setup for teams

It does not solve every tribal knowledge problem on day one. But the loop matters. When the agent gets something wrong, the correction should become part of the system instead of disappearing into chat history.

Database connections stay on your infrastructure. Only the query results and relevant schema context go to whichever model provider you configure.

## What Actually Happened

Byaan started as a hobby project with two engineer friends. We wanted to build something real, and we had our own data problem to solve.

Today, most of our customer success team answers questions through it: client health, patient engagement, satisfaction trends, contract usage, and odd one-off questions that used to go to engineering.

It is still early, but it has already learned a lot of our schema, our metrics, and the weird tribal details that only the people who built the database used to know.

Along the way, I quietly gave access to a few startup founder friends. About ten startups are now using it.

## What Is Next

I am going to keep solving our own problems with it. That is the main filter.

If you want to try it, grab the Mac app or run it with Docker. If something feels off, [open an issue](https://github.com/byaan-ai/byaan/issues){:target="\_blank"} or message me directly.

I would especially appreciate blunt feedback from people who have tried to use agents against real databases. I am most interested in where this feels useful, where it feels fragile, and what would make you trust it more.
