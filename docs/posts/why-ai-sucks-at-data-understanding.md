---
authors:
  - hjaveed
hide:
  - toc
date: 2025-11-01
readtime: 5
slug: why-ai-sucks-at-data-analysis
comments: true
---

# AI Sucks at Analyzing Data

User asks an AI data analysis tool: "Pull all patient communication encounters from last month."

The AI confidently writes a SQL query, hits the `encounters` table directly, and returns 1,247 records. AI confidently answers that. Three days later, you discover the actual number should have been 3,891, because the real path is `patients → patient_queue → queue_encounters → encounters`. The AI missed two-thirds of your data.

<!-- more -->

This isn't a hypothetical. I've seen this exact scenario play out at [RevelAI Health](https://www.revelaihealth.com/){:target="\_blank"}, where we work with health communication data. And it's not unique to us, across healthcare, finance, and any domain with messy legacy systems, AI data tools are confidently wrong in ways that are hard to detect.

## The Real Problem Isn't the Model

Data, business rules, and relationships are messy. Table names are often misleading. Developers structure databases in ways that made sense five years ago but don't reflect current business logic. Relationships between tables encode tribal knowledge that exists only in the heads of a few engineers.

And we can't expect LLMs to magically infer these relationships from schema alone. They won't. They can't.

There are dozens of companies building tools that promise: "Connect your database, ask questions in plain language, get insights." Tools like [Julius](https://julius.ai){:target="\_blank"}, [Hex](https://hex.tech){:target="\_blank"}, ChatGPT's Advanced Data Analysis, and Claude's analysis features all offer variations on this theme.

In my experience, they work fine for:

- Simple CSV uploads with self-explanatory column names
- Basic SQL databases with well-defined foreign keys
- Schemas designed by data teams with semantic modeling in mind

But the moment data relationships become messy, which is what real-world data actually looks like, these tools don't just fail. They fail _confidently_. They return plausible-looking results that are subtly (or catastrophically) wrong.

## What Would Actually Work

I see this problem being approached in a fundamentally different way. Instead of rushing to the data-analysis part, we should focus on **building domain knowledge first**.

Here's what I envision:

### 1. Interview-Style Schema Discovery

When you connect a database, the tool doesn't immediately start answering questions. Instead, it:

1. Analyzes the schema and presents its _understanding_ of how tables relate
2. Asks clarifying questions: "I see `encounters` and `patient_queue`. Which table should I use to find all patient communications?"
3. Learns from the expert's corrections and stores that as long-term memory

Think of it like onboarding a junior data analyst. You wouldn't expect them to write perfect queries on day one. You'd walk them through the schema, explain the business logic, and correct their mistakes. Over time, they'd build an internal model of how your data works.

Why don't we do this with AI tools?

### 2. Long-Term Memory Bank

Every correction, every clarification, every "actually, use this path instead" should be stored as structured knowledge—not just dumped into a vector database, but organized as business rules:

```json
{
  "rule_id": "patient_encounters_path",
  "domain": "behavioral_health_comms",
  "learned_from": "john@example.com",
  "learned_at": "2025-10-15",
  "context": "When querying patient communication encounters",
  "incorrect_approach": "SELECT * FROM encounters WHERE...",
  "correct_approach": "JOIN patients → patient_queue → queue_encounters → encounters",
  "confidence": 0.95,
  "validated_by": ["jane@example.com", "mike@example.com"]
}
```

This isn't just context for the next query. It's a knowledge base that persists across sessions, gets validated by multiple team members, and improves over time.

### 3. Reinforcement Learning from Analyst Behavior

Imagine a tool that watches how senior data analysts write queries, sees when they correct the AI's suggestions, and learns from those signals. Not in a creepy surveillance way—but as an opt-in "training mode" where the tool explicitly asks: "I see you changed my query. Can you help me understand why?"

Recent research in [LLM reflection processes](https://arxiv.org/pdf/2509.03990){:target="\_blank"} (Meta-Policy Reflexion) shows that language models can learn from past experiences through structured reflection, although it's easier said that done in real-world setting.

### 4. Transparent "Here's What I've Learned" UI

Users should be able to see:

- What relationships the tool has learned
- Which team members validated each rule
- Where the tool is still uncertain
- What questions it has about the schema

This builds trust. When the tool says "Based on corrections from Sarah and Mike, I now route patient encounter queries through the queue table," you know it's not hallucinating—it's using actual domain knowledge.

## Here's the Architecture Diagram

Current approach vs. what I'm proposing (following is generated by Claude):

```
┌─────────────────────────────────────────────────────────────┐
│ CURRENT APPROACH (Stateless)                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  User Question → Schema Inference → SQL Generation →       │
│  Execute → Return Results                                   │
│                                                             │
│  (Each query starts from scratch, no learning)              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ PROPOSED APPROACH (Stateful Learning)                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐         ┌─────────────────┐              │
│  │   Initial    │         │  Domain         │              │
│  │   Setup      │────────→│  Knowledge      │              │
│  │   Interview  │         │  Bank           │              │
│  └──────────────┘         └────────┬────────┘              │
│                                    │                        │
│  ┌──────────────┐                  │                        │
│  │ User         │                  │                        │
│  │ Question     │──────────────────┤                        │
│  └──────────────┘                  │                        │
│                                    ↓                        │
│                          ┌─────────────────┐                │
│                          │  Query          │                │
│                          │  Generation     │                │
│                          │  (Context-Aware)│                │
│                          └────────┬────────┘                │
│                                   │                         │
│                          ┌────────↓────────┐                │
│                          │   Execution     │                │
│                          └────────┬────────┘                │
│                                   │                         │
│  ┌──────────────┐        ┌────────↓────────┐               │
│  │  Analyst     │───────→│  Correction &   │               │
│  │  Correction  │        │  Learning Loop  │───┐           │
│  └──────────────┘        └─────────────────┘   │           │
│                                   │             │           │
│                                   └─────────────┘           │
│                          (Updates domain knowledge)         │
└─────────────────────────────────────────────────────────────┘
```

## Why This Is Hard

Let's face it: this is easier said than done.

As [Andrej Karpathy observed on the Dwarkesh podcast](https://www.dwarkesh.com/p/andrej-karpathy){:target="\_blank"}, we're trying to make bigger leaps without solving the underlying problem—and I'm seeing the same pattern with AI data analysis tools. There's a lot of optimism around them, but some fundamental challenges remain unaddressed.

The memory architecture isn't there yet. Deciding what becomes a long-term memory, when to retrieve it, and how to balance learned rules with schema changes—these are tough challenges we haven't solved elegantly.

**Key open questions:**

1. Memory decay: How do you handle schema migrations that invalidate learned rules?
2. Conflicting corrections: What happens when two analysts give contradictory guidance?
3. Confidence calibration: How does the tool know when to trust its learned knowledge vs. ask for clarification?

There might be a stopgap UX solution: a dashboard showing "Here's what the tool has learned about your business rules from different stakeholders," with validation workflows before rules become permanent.

But we're not there yet.

## Conclusion

I should note—I haven't done exhaustive research on every tool in the market. There are a few that come close:

**Existing Tools**: Vanna AI (RAG-based text-to-SQL with manual training), AskYourDatabase (custom question/SQL pair training), and Tableau Pulse & Power BI Copilot (enterprise BI with semantic layers) all represent progress, but require either manual training or pre-built data models—none combine interview-style discovery, long-term memory, and transparent learning from corrections.

I'm keeping an eye on:

- Memory architecture research and more implementations (like the Meta-Policy Reflexion paper)
- Tools that add interview-style schema discovery
- Reinforcement learning approaches in data tools
- Transparent "here's what I learned" UX patterns

This is one of those problems where I have strong intuitions but limited visibility into what's being built behind closed doors. If I've missed tools that are actually doing this well, please let me know in the comments.
