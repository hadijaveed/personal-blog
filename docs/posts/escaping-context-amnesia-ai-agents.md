---
authors:
  - hjaveed
hide:
  - toc
date: 2025-11-26
readtime: 7
slug: escaping-context-amnesia-ai-agents
comments: true
---

# Escaping Context Amnesia: Practical Strategies for Long-Running AI Agents

The promise of autonomous AI agents is vast: give them a high-level goal, grant them access to tools, and watch them execute complex workflows. But reality often hits hard. Specifically, it hits the context window.

Models like [Claude Sonnet 4.5](https://www.anthropic.com/claude/sonnet){target=\_blank} now offer 200K tokens (up to 1M in beta), and [GPT-5.1](https://openai.com/gpt-5/){target=\_blank} supports 400K tokens with native compaction that claims to work across millions of tokens. Problem solved, right?

Not quite. **Bigger context windows don't solve the problem. They mask it.**

<!-- more -->

### The Real Problem: It's Not Just About Size

There are three reasons why simply "using more context" fails for long-running agents:

**1. Cost Scales Linearly (or Worse)**

Every token you send costs money. At scale, a 500K token context per request adds up fast. Anthropic even charges [premium rates (2x input, 1.5x output)](https://docs.anthropic.com/en/docs/build-with-claude/context-windows){target=\_blank} for requests exceeding 200K tokens.

**2. Latency Increases**

More tokens mean longer processing time. For interactive agents where users expect quick responses, stuffing the context window creates a sluggish experience.

**3. The "Lost in the Middle" Phenomenon**

This is the critical one. Research from Stanford and others ([Liu et al., 2023](https://arxiv.org/abs/2307.03172){target=\_blank}) demonstrated that LLM performance **degrades significantly** when relevant information is positioned in the middle of long contexts. Models perform best when key information is at the beginning or end, but struggle to access what's buried in between.

The cause? A combination of causal attention (where earlier tokens get processed more) and positional encoding effects that diminish attention to middle-positioned tokens. Even models explicitly designed for long contexts suffer from this.

So when your agent has 800K tokens of conversation history and the critical instruction from turn #3 is now buried in the middle, the model literally "forgets" it. Not because it ran out of space, but because attention doesn't reach it effectively.

### What This Post Covers

After analyzing the open-source strategies of leading developer agents, including [OpenAI's Codex](https://github.com/openai/codex){target=\_blank}, [SST's OpenCode](https://github.com/sst/opencode){target=\_blank}, and the VS Code agent [Cline](https://github.com/cline/cline){target=\_blank}, I've synthesized the state-of-the-art approaches to solving the context crunch.

While I'll focus on coding agents as examples, **these techniques apply to any long-running agent**: customer support bots, research assistants, data analysis pipelines, or workflow automation. Any agent that maintains state across many turns faces the same challenges.

Here's a deep dive into a tiered approach for building agents with effectively infinite context.

---

## The Problem: Death by a Thousand Tool Calls

Before diving into solutions, let's visualize the problem. Here's what happens during a typical multi-turn agent session:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│    ┌─────────────────────────┐                                              │
│    │ System Prompt (2k)      │                                              │
│    └─────────────────────────┘                                              │
│    ┌─────────────────────────┐                                              │
│    │ User: Refactor auth     │                                              │
│    └─────────────────────────┘                                              │
│         ■──────────────────────────────────────────────── Inference!        │
│    ┌─────────────────────────┐                                              │
│    │ Model: Ok, let me read  │                                              │
│    │ Tool Call: read_file    │                                              │
│    └─────────────────────────┘                                              │
│              *─────────────────────────────────────────── Run tool          │
│         ┌──────────────────────────┐                                        │
│         │ Tool Result: [8k tokens] │                                        │
│         └──────────────────────────┘                                        │
│         ■──────────────────────────────────────────────── Inference!        │
│    ┌─────────────────────────┐                                              │
│    │ Model: Now run tests    │                                              │
│    │ Tool Call: run_tests    │                                              │
│    └─────────────────────────┘                                              │
│              *─────────────────────────────────────────── Run tool          │
│         ┌───────────────────────────┐                                       │
│         │ Tool Result: [25k tokens] │  ← Verbose test output                │
│         └───────────────────────────┘                                       │
│         ■──────────────────────────────────────────────── Inference!        │
│    ┌─────────────────────────┐                                              │
│    │ Model: Tests pass, now  │                                              │
│    │ Tool Call: read_file    │                                              │
│    └─────────────────────────┘                                              │
│              *─────────────────────────────────────────── Run tool          │
│         ┌───────────────────────────┐                                       │
│         │ Tool Result: [12k tokens] │                                       │
│         └───────────────────────────┘                                       │
│                                                                             │
│    ════════════════════════════════════════════════════════════════════     │
│    Context: 47k / 128k tokens used... and we're just getting started        │
│    ════════════════════════════════════════════════════════════════════     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

If an agent runs a test suite and gets back 15,000 lines of successful "OK" messages followed by one failure at the end, 99% of that output is noise. Yet the model has to process all of it, and it consumes precious context space.

The solution isn't larger windows. It's smarter context engineering through a tiered compression strategy.

---

## The Tiered Approach to Infinite Context

The key insight from studying production agents is that context management isn't a single strategy. It's a cascade of increasingly aggressive techniques. Each tier activates only when the previous one proves insufficient.

```
                        ┌─────────────────────┐
                        │  New Turn Complete  │
                        └──────────┬──────────┘
                                   │
                                   ▼
                        ┌─────────────────────┐
                        │  Tokens > 60%?      │
                        └──────────┬──────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │ No                     Yes  │
                    ▼                              ▼
          ┌─────────────────┐           ┌─────────────────────┐
          │    Continue     │           │  TIER 1: Pruning    │
          │    Normally     │           │  Truncate old tool  │
          └─────────────────┘           │  outputs (head+tail)│
                    ▲                   └──────────┬──────────┘
                    │                              │
                    │                              ▼
                    │                   ┌─────────────────────┐
                    │                   │  Still > 70%?       │
                    │                   └──────────┬──────────┘
                    │                              │
                    │               ┌──────────────┴──────────────┐
                    │               │ No                     Yes  │
                    │◄──────────────┘                              ▼
                    │                             ┌─────────────────────┐
                    │                             │ TIER 1.5: Compress  │
                    │                             │ Replace with smart  │
                    │                             │ placeholders        │
                    │                             └──────────┬──────────┘
                    │                                        │
                    │                                        ▼
                    │                             ┌─────────────────────┐
                    │                             │  Still > 85%?       │
                    │                             └──────────┬──────────┘
                    │                                        │
                    │                          ┌─────────────┴─────────────┐
                    │                          │ No                   Yes  │
                    │◄─────────────────────────┘                           ▼
                    │                                       ┌─────────────────────┐
                    │                                       │  TIER 2: Handoff    │
                    │                                       │  Summarize → Clear  │
                    │                                       │  → Restart          │
                    │                                       └──────────┬──────────┘
                    │                                                  │
                    └──────────────────────────────────────────────────┘
```

---

## Tier 1: The Input Guard (Smart Pruning)

The most cost-effective strategy is to prevent "garbage" context from entering the window in the first place. Tool outputs are the primary culprit for context pollution.

### The Strategy: Token-Aware Truncation with Protection Zones

Both [Codex](https://github.com/openai/codex){target=\_blank} and [OpenCode](https://github.com/sst/opencode/blob/dev/packages/opencode/src/session/compaction.ts){target=\_blank} moved away from naive "line limits" (e.g., "keep first 100 lines") because 100 lines of dense JSON is very different from 100 lines of whitespace.

Instead, they implement a strict **Token Budget** for tool outputs. If an output exceeds the budget, the system keeps the critical "Head" (context) and "Tail" (results/errors), aggressively pruning the middle.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  BEFORE: Original Tool Output (20k tokens)                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ HEAD: Command executed, processing started...          (500 tokens) │    │
│  ├─────────────────────────────────────────────────────────────────────┤    │
│  │ MIDDLE: [OK] Test 1 passed                                          │    │
│  │         [OK] Test 2 passed                                          │    │
│  │         [OK] Test 3 passed                                          │    │
│  │         ... 14,997 more lines of verbose logs ...     (18k tokens)  │    │
│  │         [OK] Test 15000 passed                                      │    │
│  ├─────────────────────────────────────────────────────────────────────┤    │
│  │ TAIL: [FAIL] Test 15001 - AssertionError at line 42                 │    │
│  │       Summary: 15000 passed, 1 failed                 (1.5k tokens) │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     │ Tier 1 Pruning
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  AFTER: Pruned Output (2k tokens)                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ HEAD: Command executed, processing started...          (500 tokens) │    │
│  ├─────────────────────────────────────────────────────────────────────┤    │
│  │ [...truncated 18,000 tokens...]                                     │    │
│  ├─────────────────────────────────────────────────────────────────────┤    │
│  │ TAIL: [FAIL] Test 15001 - AssertionError at line 42                 │    │
│  │       Summary: 15000 passed, 1 failed                 (1.5k tokens) │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│  ✓ Model sees: what command ran + the actual error it needs to fix          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Key Implementation Details

OpenCode uses two critical thresholds in their [compaction logic](https://github.com/sst/opencode/blob/dev/packages/opencode/src/session/compaction.ts){target=\_blank}:

- **PRUNE_MINIMUM**: ~20,000 tokens. Don't bother pruning if potential savings are below this.
- **PRUNE_PROTECT**: ~40,000 tokens. Recent conversation window that's always protected.

The algorithm walks **backwards** through conversation history, identifying tool outputs that exceed a maximum length threshold, but only outside the protection zone:

```
def prune(conversation):
    protection_zone = find_last_N_user_turns(2)

    for each item in conversation (backwards):
        if item.index >= protection_zone.start:
            continue  // Protected recent context

        if item.role == "tool" AND item.tokens > MAX_OUTPUT_TOKENS:
            item.content = head(500) + "[...truncated...]" + tail(1500)

    return conversation
```

**Why it works**: It ensures that no single action can "brick" the session, while still allowing the model to see the command it ran and the final error message it needs to react to.

---

## Tier 1.5: Placeholder Compression

Pruning helps, but sometimes you need to be more aggressive without losing the _structure_ of the conversation. This is where placeholder compression shines.

### The Strategy: Actionable Hints, Not Silent Removal

The key insight from [OpenCode's summary.ts](https://github.com/sst/opencode/blob/dev/packages/opencode/src/session/summary.ts){target=\_blank} and [Cline's ContextManager](https://github.com/cline/cline/blob/main/src/core/context/context-management/ContextManager.ts){target=\_blank} is that replacing content with informative placeholders is better than silent removal.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  BEFORE: Full Conversation History                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│    ┌───────────────────────────────────┐                                    │
│    │ User: Query sales data            │                                    │
│    └───────────────────────────────────┘                                    │
│         ■──────────────────────────────────────────────── Inference!        │
│    ┌───────────────────────────────────┐                                    │
│    │ Model: Let me query that          │                                    │
│    │ Tool Call: execute_query          │                                    │
│    └───────────────────────────────────┘                                    │
│              *─────────────────────────────────────────── Run tool          │
│         ┌───────────────────────────────────────┐                           │
│         │ Tool Result:                          │                           │
│         │ {"rows": [                            │                           │
│         │   {"id": 1, "amount": 500, ...},      │  ← 15k tokens of JSON     │
│         │   {"id": 2, "amount": 750, ...},      │                           │
│         │   ... 4998 more rows ...              │                           │
│         │ ]}                                    │                           │
│         └───────────────────────────────────────┘                           │
│         ■──────────────────────────────────────────────── Inference!        │
│    ┌───────────────────────────────────┐                                    │
│    │ Model: Total sales are $2.3M      │                                    │
│    └───────────────────────────────────┘                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     │ Tier 1.5: Placeholder Compression
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  AFTER: Compressed with Actionable Placeholder                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│    ┌───────────────────────────────────┐                                    │
│    │ User: Query sales data            │                                    │
│    └───────────────────────────────────┘                                    │
│    ┌───────────────────────────────────┐                                    │
│    │ Model: Let me query that          │                                    │
│    │ Tool Call: execute_query          │  ← Tool call preserved (structure) │
│    └───────────────────────────────────┘                                    │
│         ┌─────────────────────────────────────────────────────────────┐     │
│         │ [Query executed. Use execute_query again for fresh results] │     │
│         └─────────────────────────────────────────────────────────────┘     │
│    ┌───────────────────────────────────┐    ↑                               │
│    │ Model: Total sales are $2.3M      │    │                               │
│    └───────────────────────────────────┘    │                               │
│                                             │                               │
│    ✓ Model knows: action succeeded + how to get data again if needed        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### The Critical Difference: Actionable vs. Generic Placeholders

A placeholder like `[removed]` or `[truncated]` leaves the model confused. But a placeholder like:

```
[Query executed successfully. Use execute_query again if you need fresh results]
```

...gives the model a clear path forward. It knows the action completed and how to recover the data if needed.

### Implementation Pattern

```
PLACEHOLDERS = {
    "query_execution":    "[Query executed. Re-run if you need fresh results]",
    "file_read":          "[File read previously. Read again if needed]",
    "search_results":     "[Search completed. Search again for current results]",
    "html_generation":    "[HTML generated. Use get_current_state for latest]",
}

def compact(conversation):
    essential_tools = {"schema_inspection", "database_structure"}
    keep_latest_only = {"saved_state", "current_config"}

    for each tool_result in conversation:
        tool_type = categorize(tool_result)

        if tool_type in essential_tools:
            continue  // Never compress these

        if tool_type in keep_latest_only:
            if not is_most_recent_of_type(tool_result):
                replace_with_placeholder(tool_result, PLACEHOLDERS[tool_type])
        else:
            replace_with_placeholder(tool_result, PLACEHOLDERS[tool_type])
```

### Cline's Duplicate Detection

[Cline](https://github.com/cline/cline/blob/main/src/core/context/context-management/ContextManager.ts){target=\_blank} adds another clever optimization: **duplicate file read detection**. If the same file is read multiple times in a conversation, subsequent reads are replaced with a notice pointing to the original. They target 30% character savings before moving to more aggressive truncation.

---

## Tier 2: Session Handoff (Total Recall)

Pruning and placeholders help, but for truly long-running tasks (e.g., a multi-hour refactoring mission), the history will eventually fill up with _necessary_ turns.

When the context window reaches a critical threshold (e.g., 85-90%), you need a "Reset Button." This is the strategy heavily utilized by [OpenAI's Codex](https://github.com/openai/codex){target=\_blank}.

### The Strategy: Compaction via Recursive Summarization

Rather than simply deleting old messages, the system triggers a "Handoff" event.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  SESSION HANDOFF FLOW                                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   1. DETECT: Context reaches 90% threshold                                  │
│   ─────────────────────────────────────────                                 │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │ Context Window: ████████████████████████████████████████░░░░ 92%   │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   2. PAUSE: Stop processing, gather full history                            │
│   ──────────────────────────────────────────────                            │
│                                                                             │
│   ┌────────────────────────────────────┐                                    │
│   │ Full Conversation History          │                                    │
│   │ ├─ System prompt                   │                                    │
│   │ ├─ User message #1                 │                                    │
│   │ ├─ Assistant + tools               │───────┐                            │
│   │ ├─ User message #2                 │       │                            │
│   │ ├─ Assistant + tools               │       │ Send to                    │
│   │ ├─ ... (50 more turns) ...         │       │ Fast Model                 │
│   │ └─ Last user message ◄─────────────│───┐   │                            │
│   └────────────────────────────────────┘   │   │                            │
│                                            │   ▼                            │
│   3. SUMMARIZE: Fast model generates handoff note                           │
│   ───────────────────────────────────────────────                           │
│                                            │   ┌────────────────────────┐   │
│                                            │   │ "Summarize this        │   │
│                                            │   │  conversation for      │   │
│                                            │   │  continuation..."      │   │
│                                            │   └───────────┬────────────┘   │
│                                            │               │                │
│                                            │               ▼                │
│   4. RESTART: New session with summary + last user message                  │
│   ────────────────────────────────────────────────────────                  │
│                                            │   ┌────────────────────────┐   │
│   ┌────────────────────────────────────┐   │   │ Handoff Note:          │   │
│   │ NEW Context Window                 │   │   │ - Goal: Refactor auth  │   │
│   │                                    │   │   │ - Done: Updated 3 files│   │
│   │ ┌────────────────────────────────┐ │   │   │ - Current: Fixing test │   │
│   │ │ System: PREVIOUS SESSION       │◄│───│───│ - Next: Run test suite │   │
│   │ │ [Handoff Note: ~500 tokens]    │ │   │   └────────────────────────┘   │
│   │ └────────────────────────────────┘ │   │                                │
│   │ ┌────────────────────────────────┐ │   │                                │
│   │ │ User: [Last message]           │◄│───┘                                │
│   │ └────────────────────────────────┘ │                                    │
│   │                                    │                                    │
│   │ Context: ██░░░░░░░░░░░░░░░░░░░ 5%  │  ← Fresh start!                    │
│   └────────────────────────────────────┘                                    │
│                                                                             │
│   ✓ 100k tokens of history → 500 tokens of pure signal                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### The Handoff Note Format

The summary isn't prose. It's a structured state definition. OpenCode's [compaction prompt](https://github.com/sst/opencode/blob/dev/packages/opencode/src/session/prompt/compaction.txt){target=\_blank} instructs the summarizer to capture:

1. **Current Goal**: What is the user ultimately trying to achieve?
2. **Progress Made**: What has been completed successfully?
3. **Files Modified**: Which files have been changed and how?
4. **Current State**: What was the agent doing when handoff triggered?
5. **Next Steps**: What should happen immediately after restart?

### Implementation

```
def handoff(conversation, threshold=0.90):
    if token_count(conversation) < context_limit * threshold:
        return conversation  // Not needed yet

    // Use a fast, cheap model for summarization
    summary = call_model(
        model = "fast-summarizer",  // e.g., GPT-4o-mini, Haiku
        prompt = HANDOFF_PROMPT,
        content = conversation
    )

    last_user_message = find_last_user_message(conversation)

    new_session = [
        {"role": "system", "content": "PREVIOUS SESSION CONTEXT:\n" + summary},
        last_user_message
    ]

    return new_session  // 100k tokens → ~500 tokens
```

**Why it works**: It converts 100k tokens of messy history into 500 tokens of pure signal, allowing the agent to continue working indefinitely by "passing the baton" to itself.

---

## Tier 2.5: Middle-Out Compression (Optional)

A common failure mode of naive summarization is the loss of critical details from the beginning of the task (the original goal) and the end (the current state). [Cline](https://github.com/cline/cline/blob/main/src/core/context/context-management/ContextManager.ts){target=\_blank} pioneered a "Middle-Out" strategy that addresses this.

### The Strategy: Preserve the Ends, Crush the Middle

When context pressure mounts, this strategy doesn't wipe the slate clean. Instead, it performs surgery on the conversation history.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  MIDDLE-OUT COMPRESSION                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   BEFORE                                       AFTER                        │
│   ──────                                       ─────                        │
│                                                                             │
│   ┌─────────────────────────┐                 ┌─────────────────────────┐   │
│   │ HEAD                    │                 │ HEAD                    │   │
│   │ ┌─────────────────────┐ │                 │ ┌─────────────────────┐ │   │
│   │ │ System Prompt       │ │  ═══════════▶   │ │ System Prompt       │ │   │
│   │ │ User: "Refactor     │ │   PRESERVED    │ │ User: "Refactor     │ │   │
│   │ │ the auth system"    │ │   VERBATIM     │ │ the auth system"    │ │   │
│   │ └─────────────────────┘ │                 │ └─────────────────────┘ │   │
│   │ (The original goal)     │                 │ (Goal intact)           │   │
│   └─────────────────────────┘                 └─────────────────────────┘   │
│                                                                             │
│   ┌─────────────────────────┐                 ┌─────────────────────────┐   │
│   │ MIDDLE                  │                 │ MIDDLE                  │   │
│   │ ┌─────────────────────┐ │                 │ ┌─────────────────────┐ │   │
│   │ │ Turn 2: Read files  │ │                 │ │ [Summary: Read 5    │ │   │
│   │ │ Turn 3: Analyze     │ │                 │ │  files, identified  │ │   │
│   │ │ Turn 4: First edit  │ │  ═══════════▶   │ │  auth patterns,     │ │   │
│   │ │ Turn 5: Run tests   │ │   SUMMARIZED   │ │  made 3 edits,      │ │   │
│   │ │ Turn 6: Fix bug     │ │                 │ │  tests passing]     │ │   │
│   │ │ ... 20 more turns   │ │                 │ └─────────────────────┘ │   │
│   │ └─────────────────────┘ │                 │ (Journey compressed)    │   │
│   │ (The noisy journey)     │                 └─────────────────────────┘   │
│   └─────────────────────────┘                                               │
│                                                                             │
│   ┌─────────────────────────┐                 ┌─────────────────────────┐   │
│   │ TAIL                    │                 │ TAIL                    │   │
│   │ ┌─────────────────────┐ │                 │ ┌─────────────────────┐ │   │
│   │ │ Turn N-4: Edit JWT  │ │  ═══════════▶   │ │ Turn N-4: Edit JWT  │ │   │
│   │ │ Turn N-3: Test fail │ │   PRESERVED    │ │ Turn N-3: Test fail │ │   │
│   │ │ Turn N-2: Debug     │ │   VERBATIM     │ │ Turn N-2: Debug     │ │   │
│   │ │ Turn N-1: Fix found │ │                 │ │ Turn N-1: Fix found │ │   │
│   │ │ Turn N: User input  │ │                 │ │ Turn N: User input  │ │   │
│   │ └─────────────────────┘ │                 │ └─────────────────────┘ │   │
│   │ (Current state)         │                 │ (State intact)          │   │
│   └─────────────────────────┘                 └─────────────────────────┘   │
│                                                                             │
│   ✓ Agent knows WHY it started + WHERE it is now                            │
│   ✗ Forgets the noisy journey in between (that's fine!)                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Cline's Implementation

In Cline's `getNextTruncationRange()` function, they explicitly protect indices 0-1 (the first user message and assistant response):

```
rangeStartIndex = 2  // Never touch the first exchange
```

They then calculate how much to remove based on pressure:

- **"half" mode**: Keep 75% of messages after deduplication
- **"quarter" mode**: Keep 50% of messages (more aggressive)

The truncation always removes from the middle, leaving both the "why we started" (head) and "where we are now" (tail) intact.

**Why it works**: The agent always knows why it started the task and where it is right now, without being distracted by the noisy journey in between.

---

## What Worked For Us

After studying these open-source implementations, we built our own tiered system. Here's the algorithm that's proven effective:

### Our Tiered Implementation

**Tier 1: Protection Zone Pruning**

```
def prune(conversation):
    // Protect last 2 user turns unconditionally
    protection_zone_start = find_nth_last_user_turn(2)
    tokens_before = count_tokens(conversation)

    for idx in reverse(range(len(conversation))):
        if idx >= protection_zone_start:
            continue  // In protection zone

        item = conversation[idx]
        if item.role == "tool" and len(item.content) > MAX_OUTPUT_LENGTH:
            preview = item.content[:1000]
            item.content = f"{preview}...\n[Output pruned. Original: {len(item.content)} chars]"

    tokens_after = count_tokens(conversation)
    log(f"Tier 1: {tokens_before} → {tokens_after} tokens")
    return conversation
```

**Tier 1.5: Smart Placeholder Replacement**

```
def compact(conversation):
    essential = {"schema_inspection", "structure_query"}  // Never touch
    latest_only = {"saved_state"}  // Keep only most recent

    tool_id_to_type = analyze_tool_calls(conversation)
    latest_of_type = {}

    // First pass: identify latest of each "keep latest" type
    for result in conversation where result.role == "tool":
        tool_type = tool_id_to_type[result.id]
        if tool_type in latest_only:
            latest_of_type[tool_type] = result.id

    // Second pass: replace with placeholders
    for result in conversation where result.role == "tool":
        tool_type = tool_id_to_type[result.id]

        if tool_type in essential:
            continue

        if tool_type in latest_only and result.id == latest_of_type[tool_type]:
            continue  // This is the latest, keep it

        result.content = PLACEHOLDERS[tool_type]

    return conversation
```

**Tier 2: Session Handoff**

```
def handoff(conversation, llm_connection):
    if token_ratio(conversation) < 0.85:
        return conversation

    summary = call_fast_model(
        prompt = HANDOFF_PROMPT,
        conversation = conversation,
        model = "fast-cheap-model"
    )

    last_user = find_last_user_message(conversation)

    return [
        {"role": "system", "content": f"SESSION CONTEXT:\n{summary}"},
        last_user
    ]
```

### Key Decisions That Made the Difference

1. **Protection zones by turn count, not tokens**: Last 2 user messages are always safe, regardless of their size
2. **Actionable placeholders**: Every placeholder tells the model how to recover the data
3. **Essential tools whitelist**: Schema and structure tools are never compressed. They're foundational.
4. **Keep-latest-only pattern**: For cumulative state (saved queries, current config), only the most recent matters

---

## The Future: From Reactive to Proactive

Today's strategies are primarily **reactive**: the agent hits a limit, then compresses. The next frontier is **proactive context management**:

- **Semantic RAG for conversation history**: Instead of keeping everything, index past turns and retrieve only what's relevant to the current task
- **Externalized state**: Maintain a persistent "scratchpad" file outside the context window that survives any amount of clearing
- **Predictive pruning**: Use a lightweight model to predict which tool outputs will be needed later, pruning aggressively on low-value results

The battle for AI reliability won't be won by larger context windows. It will be won by smarter context engineering. By implementing strategies like Input Pruning, Placeholder Compression, and Session Handoffs, we can build agents that don't just work for the first five minutes. They work for the entire project.

---

## References

- [OpenAI Codex](https://github.com/openai/codex){target=\_blank}: Session memory patterns, token counting
- [SST OpenCode](https://github.com/sst/opencode){target=\_blank}: Two-tier prune → compact strategy
  - [compaction.ts](https://github.com/sst/opencode/blob/dev/packages/opencode/src/session/compaction.ts){target=\_blank}
  - [summary.ts](https://github.com/sst/opencode/blob/dev/packages/opencode/src/session/summary.ts){target=\_blank}
- [Cline](https://github.com/cline/cline){target=\_blank}: Middle-out compression, duplicate detection
  - [ContextManager.ts](https://github.com/cline/cline/blob/main/src/core/context/context-management/ContextManager.ts){target=\_blank}
