---
authors:
    - hjaveed
hide:
    - toc
date: 2024-11-17
readtime: 5
slug: cognitive-architecture-patterns-in-health-care
comments: true
---

# Cognitive Architecture Patterns in Health Care for LLMs

We're inspired by the ideas from this [Cognitive Architecture paper](https://arxiv.org/pdf/2309.02427){target=_blank} and an insightful [Langchain Blog](https://blog.langchain.dev/what-is-a-cognitive-architecture/){target=_blank} by Harrison Chase. 

At [RevelAI Health](https://revelaihealth.com/){target=_blank}, we're exploring how to create closed-loop, safe agents in healthcare — systems that can reason and execute on patient needs in a secure and reliable way. The key is understanding how these agentic systems should think, the flow of execution in response to patient intent, and ensuring safety through structured, observable loops.

<!-- more -->

## Building Safe and Reliable Healthcare Agents

We've experimented with different architectures and patterns to develop effective healthcare agents, and here, I want to share our progress and ongoing work. This is a continuous journey; we're committed to evolving and learning as we go.

### Level 1: Single LLM Call (QnA Chatbot)

At the simplest level, we start with a tailored prompt-based LLM, designed for specific personas like an orthopedic care assistant or primary care assistant. Success here depends heavily on precise prompt engineering, including improving retrieval with a hybrid approach — for instance, combining semantic search and sparse vector search (e.g., BM25), along with metadata-based filtering that considers the patient phase of care, specific patient contexts like summarized notes from system records, patient history, and other contextual fields.

!!! note
    We're not diving into the technical details of our retrieval system here, as that deserves its own dedicated post. The retrieval process is arguably the most critical component, as it's the primary driver of accuracy alongside prompt engineering. Getting this right is essential for safe and reliable healthcare agents.


Grounding the LLM in evidence-based content curated by providers and subject matter experts is key to ensuring quality. It's not just about retrieval but also providing contextual awareness: patient phase of care, whether they're pre-op or post-op, current prescribed pathways, and other relevant information. The LLM must be firmly anchored in a patient's specific context to be effective.

Our retrieval process relies on a hybrid approach that uses system records like EMRs, combined with databases such as social needs referrals, to build a complete picture and provide accurate responses.

<img src="/assets/single-chatbot-retrieval.png" alt="LLM Retrieval" id="llm-retrieval" style="display: block; margin-left: auto; margin-right: auto; width: 100%; height: 500px; object-fit: cover;">
<style>
@media (max-width: 767px) {
  #llm-retrieval {
    height: auto !important;
  }
}
</style>

### Level 2: Chaining Multiple LLM Calls

When simple QnA isn’t sufficient, we use multiple specialized LLMs, each designed for a specific task such as rewriting questions, translating based on language preferences, or adjusting responses based on literacy levels gathered through tools like the Single Item Literacy Screener (SILS-2).

In healthcare, questions often require multiple interactions for a complete answer. Our agents proactively engage in dialogue, asking follow-up questions based on different intents to gather the necessary context before providing a final response. We have developed several intent-specific dialogues to ensure the model collects all relevant information prior to giving an answer. Depending on the scenario, multiple specialized LLMs may collaborate in a sequence, working as an ensemble to deliver a final answer that is both accurate and personalized.

We also utilize an LLM as a judge, evaluating final responses against strict criteria to ensure compliance, such as avoiding unauthorized medication advice, and determining when the LLM should either refrain from answering or respond in a specific, predefined way.

<img src="/assets/chain-of-llms.png" alt="Chain of LLMs" id="chain-of-llms" style="display: block; margin-left: auto; margin-right: auto; width: 100%; height: 150px; object-fit: cover;">
<style>
@media (max-width: 767px) {
  #chain-of-llms {
    height: auto !important;
  }
}
</style>

### Level 3: The Intent Router and the Orchestrator

We've developed multiple sub-specialized agents, each one focusing on a specific area — like orthopedics, diabetes, or social care. These agents include an LLM, specialized retrieval content, and specific tools. They allow us to work in silos with healthcare professionals to refine accuracy before integrating them into broader orchestration systems. Every specialized agent follows it's own evaluation criteria and the testing

The most significant challenge is routing patient intent to the right agent based on the context and data available. This goes beyond typical function-based OpenAI routing; we build datasets of different intents (e.g., orthopedic care, medication refill, social care, appointment requests) to guide the routing accurately. Our intent prediction is done through in-context-learning ICL or other mechanism to ensure the accuracy. We have developed multiple accuracy benchmarks on creating evaluation and predicting the correct intent across like 20 categories.Additionally, we have developed a dataset for acuity prediction, categorizing patient inquiries based on urgency, specificity, and need. Each inquiry is classified into one of three acuity levels: high, medium, or low.

We provide a dashboard for care team members to manage incoming inquiries, whether they come via text, call, or other communication channels. The system suggests actions based on the acuity level and determines when human intervention is necessary, coordinating between agents to fulfill patient intents either automatically or manually.


<img src="/assets/triage-dashboard.png" alt="RevelAI Triage" id="revel-ai-triage" style="display: block; margin-left: auto; margin-right: auto; width: 100%; height: 500px; object-fit: cover;">
<style>
@media (max-width: 767px) {
  #revel-ai-triage {
    height: auto !important;
  }
}
</style>

Once intents are identified, orchestrators manage the specialized agents, coordinating them either sequentially or in parallel based on the context. Some agents complete tasks autonomously, such as drafting medication refill requests or forwarding notes to system records, effectively closing the loop.
<img src="/assets/llm-orchesttration.png" alt="LLM Orchestration" id="llm-orchestration" style="display: block; margin-left: auto; margin-right: auto; width: 100%; height: 600px; object-fit: cover; margin-top: 20px;">
<style>
@media (max-width: 767px) {
  #llm-orchestration {
    height: auto !important;
  }
}
</style>

### Level 4: Looping Agents and State Machines

Based on the predicted intents, our system can loop through agents and create a state machine to orchestrate workflows effectively. This means different agents work together seamlessly, adapting to changes in the patient’s condition or needs as they move through the healthcare journey.

### Level 5: Towards Full Autonomy with Agent Loops

We're not fully autonomous yet, and we believe in keeping humans in the loop for high-stakes decisions. For example, an agent can collect patient preferences for an appointment, but the final booking action still requires human oversight.

We’ve built agents capable of predicting the acuity level of patient requests (high, medium, or low). For high-acuity needs, we loop in healthcare professionals. For medium ones, we may involve a nurse, and for low-risk tasks, we can close the loop automatically. But we are cautious, recognizing the importance of human validation, especially in critical scenarios.

Proactive outreach is another complex area — moving beyond hard-coded pathways (e.g., sending a message X days after discharge). We envision a dynamic state machine that adapts to patient data and engagement patterns, reaching out proactively and intelligently. However, this requires rigorous testing to ensure safety and effectiveness, and we're committed to learning and iterating. We believe that an autonomous state machine capable of proactively reaching out to patients based on engagement patterns or temporal relationships could significantly improve our scalability, eliminating the need to build rigid pathways for every possible scenario. It has the potential to transform population health management at scale, fundamentally changing how care is delivered. This is why we continue to experiment and refine our approach.

## Final Thoughts

LLMs are still evolving, and the stakes in healthcare are high — getting things wrong can have severe consequences. We must balance the need for experimentation with the need for caution. By involving healthcare professionals in our iterative processes, maintaining a human-in-the-loop approach, and building strong feedback mechanisms, we aim to de-risk our systems while maximizing the value they bring.

Our work is just beginning. We believe in learning every day and evolving our approach to bring safe, effective, and scalable AI-driven healthcare solutions to life. Tracing response paths, annotation-based evaluation, and leveraging LLMs as judges are just some of the methods we're using to ensure accuracy, minimize bias, and automate the testing process.

We're off to a promising start, and we’re eager to keep pushing forward, mindful of the responsibility that comes with innovation in healthcare.

