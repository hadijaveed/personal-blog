---
authors:
  - hjaveed
hide:
  - toc
date: 2025-08-13
readtime: 4
slug: recursive-summary-is-all-you-need-healthcare-llm
comments: true
---

# Recursive Summarization Unlocks Effective LLM Integration in Healthcare

Your patient has 247 pages of medical records spanning 8 years. Two ER visits, three specialists, ongoing knee osteoarthritis, recent ACL reconstruction. How do you create a coherent summary that preserves critical information while making it digestible for both clinicians and AI systems?

The answer isn't just summarization, it's **recursive summarization**. And the secret isn't just what you summarize, but what you choose to preserve at each level of abstraction.

<!-- more -->

## What Is Recursive Summarization?

Recursive summarization creates a hierarchical tree of information by repeatedly clustering and summarizing content at increasing levels of abstraction. Think of it as building a pyramid where each level captures essential information from the layer below, but with progressively broader context.

This technique builds on established methods like [hierarchical clustering for document organization](https://arxiv.org/html/2506.19992){target=_blank} and [map-reduce approaches for long document processing](https://stephencollins.tech/newsletters/improving-summarization-tasks-graphrag-raptorrag){target=_blank}.

Here's how it works for healthcare:

1. **Level 0**: Individual clinical notes, lab results, prescription records
2. **Level 1**: Daily/visit summaries combining related notes from the same encounter
3. **Level 2**: Episode summaries (e.g., "ACL reconstruction recovery Q2 2024" or "chronic pain management")  
4. **Level 3**: Longitudinal condition summaries spanning multiple episodes
5. **Level 4**: Complete patient timeline with major orthopedic events and functional outcomes

This approach, inspired by systems like [RAPTOR (Recursive Abstractive Processing for Tree-Organized Retrieval)](https://arxiv.org/abs/2401.18059){target=_blank}, enables LLMs to access both granular details and high-level patient narratives depending on the clinical context needed.

## The Challenge: Encounters Beyond the EHR

Healthcare happens everywhere, not just in structured EHR fields. Consider these real scenarios:

**Nurse triage call**: "Patient reports 8/10 knee pain, started after PT session yesterday. Swelling increased, can't bear weight. Taking prescribed oxycodone 5mg q6h. Post-op week 3 from ACL reconstruction."

**Patient text**: "Hey doc, my knee is really stiff in the mornings and the exercises are getting harder. Should I push through the pain? Also, when can I start jogging again?"

**Post-discharge follow-up**: "Incision healing well, no signs of infection. Pain is down to 4/10 with ibuprofen. ROM improving but still can't fully extend. When can I return to work?"

Each interaction contains critical information that traditional EHRs often lose in free-text fields or don't capture at all. Recursive summarization can preserve both the immediate clinical details and the broader patterns these communications reveal.

## The Salient Features Problem

Here's the catch: building upon past summaries alone isn't enough. **What you choose to keep or abstract at each level determines everything.**

This is where subject matter expertise becomes critical. Clinical insights from orthopedic surgeons, physical therapists, and care coordinators are essential for defining what information matters at each abstraction level. Developers working in isolation will inevitably miss nuanced clinical relationships that experienced clinicians intuitively understand.

Let's examine what matters:

### Keep These Details:
- **Dosages and frequencies**: "Oxycodone 5mg q6h PRN" not "taking pain medication"
- **Timing relationships**: "Knee pain increased 24 hours after PT session" 
- **Quantified symptoms**: "8/10 pain scale, ROM 0-90 degrees" vs "significant pain"
- **Functional outcomes**: Weight-bearing status, return-to-activity timelines
- **PT progress markers**: Specific exercises, resistance levels, functional milestones

### Abstract These Patterns:
- **Recurring themes**: Multiple PT compliance issues → "Adherence challenges with rehabilitation protocol"
- **Stable recovery**: "Post-op healing progressing as expected" vs daily wound checks
- **Resolution of complications**: "Post-surgical swelling resolved" vs daily measurements

The distinction between what to preserve and what to abstract often requires clinical judgment that only comes from years of patient care experience. For example, knowing that "terminal extension deficit" in ACL recovery requires different monitoring than general ROM limitations is insight that developers simply cannot infer from data patterns alone.

## Example: Patient Encounter Hierarchy

**Level 0 (Raw Data)**:

- 3/15/2024 - Orthopedic follow-up note (847 words)
- 3/15/2024 - MRI report (312 words)  
- 3/15/2024 - PT evaluation (ROM measurements, strength testing)
- 3/20/2024 - Patient portal message about PT difficulties
- 3/22/2024 - Nurse callback about increased swelling

**Level 1 (Visit Summary)**:

"3/15/2024 Orthopedic follow-up: Patient reports improved weight-bearing tolerance, able to walk without crutches. ROM 0-110 degrees (target 0-130). MRI shows good graft healing, no complications. PT progressing but patient struggling with terminal extension exercises. Cleared for stationary bike. Follow-up in 6 weeks. Subsequent messages indicate increased swelling after PT - activity modification needed."

**Level 2 (Episode Summary)**:

"Q1 2024 ACL reconstruction recovery: Post-operative rehabilitation progressing appropriately. Achieved weight-bearing independence ahead of schedule. Graft healing well on imaging. PT compliance good but terminal extension remains challenging. Minor setback with activity-related swelling managed conservatively. Overall trajectory positive toward return-to-sport goals."

## The Delta-Based Approach: Reasoning About Change

Traditional summaries lose temporal context. Delta-based recursive summarization tracks **what changed** between encounters, enabling sophisticated clinical reasoning. This approach leverages [temporal reasoning techniques for medical data](https://www.sciencedirect.com/science/article/pii/S1532046407000032){target=_blank} and [longitudinal medical record analysis](https://arxiv.org/abs/2410.12860){target=_blank}:

```
Previous Summary (12/2023):
- "Chronic knee pain, conservative management"
- "ROM limited to 0-100 degrees, functional limitations"

Current Summary (3/2024):  
- "Post-ACL reconstruction, early recovery phase" 
- "ROM improved to 0-110 degrees, weight-bearing as tolerated"

Delta Analysis:
+ IMPROVING: Range of motion (0-100° → 0-110°)
+ IMPROVING: Functional status (non-weight bearing → WBAT)
+ NEW INTERVENTION: Surgical reconstruction completed
+ EMERGING CONCERN: PT compliance challenges with terminal extension
+ CONTEXT: Return-to-sport timeline driving aggressive rehabilitation
```

This delta awareness enables LLMs to reason about recovery trajectories, rehabilitation responses, and emerging functional patterns that pure summarization misses.

## Architecture: The Recursive Healthcare Summary System

<img src="/assets/recursive-summary.png" alt="Recursive Healthcare Summary Architecture" id="recursive-summary" style="display: block; margin-left: auto; margin-right: auto; width: 100%; height: auto; object-fit: contain;">
<style>
@media (max-width: 767px) {
  #recursive-summary {
    width: 100% !important;
  }
}
</style>

The key innovation is the **delta analysis layer** that maintains change awareness throughout the hierarchy, enabling both detailed clinical decision-making and population-level insights.

## Implementation Reality Check

The research shows promising results: [LLMs often outperform human experts in clinical text summarization](https://www.nature.com/articles/s41746-022-00742-2){target=_blank} across completeness, correctness, and conciseness. Systems processing [82+ billion medical words from millions of encounters](https://pmc.ncbi.nlm.nih.gov/articles/PMC10635391/){target=_blank} demonstrate this approach's feasibility at scale.

But challenges remain:

- **Information loss**: Summarization inherently discards details, choosing wisely is critical
- **Context windows**: Even with larger models, [100+ page patient histories require intelligent chunking](https://www.width.ai/post/patient-record-summarization){target=_blank}
- **Clinical validation**: Automated summaries need human oversight for high-stakes decisions

## Closing Thoughts

Healthcare generates massive amounts of unstructured data daily. [Clinicians spend enormous time synthesizing information](https://www.jmir.org/2025/1/e68998){target=_blank} instead of caring for patients. Recursive summarization with delta-based reasoning offers a path forward, preserving essential clinical details while making complex patient histories navigable.

The magic isn't in the AI doing the summarizing. It's in designing systems that know what clinical information to preserve, what to abstract, and how to maintain the temporal relationships that enable real medical reasoning.

As healthcare moves toward AI-augmented workflows, recursive summarization isn't just a nice-to-have feature, it's the foundation that makes everything else possible.
