---
authors:
    - hjaveed

date: 2024-03-05
readtime: 10
slug: tracing-and-observability-in-llm-applications
---

**From Concept to Production with Observability in LLM Applications**

Understanding observability in AI applications, particularly in Large Language Models (LLMs), is crucial. It's all about tracking how your model performs over time, which is especially challenging with text generation outputs. Unlike categorical outputs, text generation can vary widely, making it essential to monitor the behavior and performance of your model closely.

<!-- more -->

Imagine you're developing an application tailored to a specific use case. Perhaps you're enhancing an LLM with an external corpus through techniques like [RAG (Retrieval-Augmented Generation) ](https://arxiv.org/pdf/2005.11401.pdf){:target="_blank"} or interfacing with a database API to process unstructured text. By leveraging relevant snippets retrieved in this way, you aim for your model to generate useful outputs. With the advent of tools like [LangChain](https://www.langchain.com/){:target="_blank"} and [LLamaIndex](https://www.llamaindex.ai/){:target="_blank"}, alongside embedding models, building such systems has become more straightforward. Your development team's initial reaction might be overwhelmingly positive, but the real challenge emerges when transitioning from a development to a production environment. How do you ensure the accuracy and reliability of your system in real-world scenarios?

**The Evolution of Chatbots and Classification Applications with LLMs**

As LLMs grow increasingly accessible, many teams are venturing into creating innovative applications. An approach might involve using a document corpus to develop a RAG pipeline tailored to your domain-specific data. Thanks to open-source libraries, assembling these applications has become significantly easier.

You might employ a prompt to enhance the retrieval workflow, utilizing content from a vector store. Given the impressive reasoning capabilities of LLMs, such applications can provide substantial value depending on the use case, earning you accolades from your team for swift development.

**Navigating the Challenges of Production Readiness**

When your application is in staging, and your team begins to use it extensively, you're on the cusp of deploying it in a production environment. This stage brings about a critical question: How do you measure the accuracy and performance of your application? LLM-generated responses introduce a high degree of subjectivity, rendering traditional unit tests inadequate. Developing robust test cases becomes imperative, ensuring they're revisited with every modification to the application, be it in the prompts or any other component.

**Investing in LLM Operations: A Necessity, Not a Choice**

Collecting comprehensive and well-rounded feedback can seem daunting. Human annotation and labeling, while valuable, are often costly. A practical first step involves identifying 50-100 common queries and patterns. Collaborate with your team or subject matter experts to craft ideal responses for these scenarios.

### LLM Response Evaluation

An effective strategy is to conduct automated evaluations based on these ideal responses. The more diverse and case-specific your questions are, the better. Even a small subset of questions reviewed by human labelers can provide invaluable insights.

Consider implementing an evaluation pipeline similar to [RAGAS](https://github.com/explodinggradients/ragas){:target="_blank"}, focusing on metrics like faithfulness and answer relevancy:

- **Faithfulness**: Assess whether the LLM creates outputs based solely on the provided content, avoiding hallucinations.
- **Relevancy**: Evaluate how the LLM's responses align with the user's questions.

Beyond these metrics, you might explore additional measures tailored to your specific use case. Regularly running these automated tests, especially after updates to your RAG strategy or prompts, can significantly enhance your application's reliability. Incorporating these tests into your continuous deployment process can further streamline operations.

### Tracing and Collecting Spans: Insights into Execution

Drawing inspiration from [OpenTelemetry](https://opentelemetry.io/docs/concepts/signals/traces/){:target="_blank"}, Traces give us the big picture of what happens when a request is made to an LLM application. Traces are essential to understanding the full “path” a request takes in your application, e.g, prompt, query-expansion, RAG retrieved top-k document, functional call and other mechanisms incorporated into your LLM application are represented as [SPAN](https://opentelemetry.io/docs/concepts/signals/traces/#spans){:target="_blank"} under one trace. Spans represent individual unit of work or operation e.g, vector store call, functional call or others.

Understanding the intricacies of your LLM's performance is vital. Perhaps the issue isn't with the LLM itself but with the RAG component or a lack of relevant data in your corpus. Identifying the root cause of errors or hallucinations requires comprehensive traceability of your application's execution paths.

**Example: Leveraging Langsmith SDK for Enhanced Observability**

Selecting the right tools for tracing can dramatically affect your operational efficiency. While custom solutions are possible, they often require substantial effort to implement correctly. Tools like Langchain provide abstractions that facilitate tracking multiple execution units, types, and attributes without overcomplicating your codebase, allowing you to focus more on product development and less on operational infrastructure. 

```python
class LLMTracer:
    def __init__(self, inputs: dict, meta: dict = {}):
        self.pipeline = RunTree(
            run_type="chain",
            name="<your-application>",
            inputs=inputs,
            extra=meta,
        )

    def add_log(self, name: str, inputs: dict = {}, outputs: dict = {}, run_type: str = "llm"):
        log = self.pipeline.create_child(
            name=name,
            run_type=run_type,
            inputs=inputs,
        )
        log.end(outputs=outputs)
        log.post()

    def final(self, outputs: dict = {}):
        self.pipeline.end(outputs=outputs)
        self.pipeline.post()


## example usage in the code
tracer = LLMTracer(inputs=messages, meta={"model": "xyz", **other })

## add logs to the execution trace
tracer.add_log("functional_call", inputs={**function_inputs}, outputs={**function_outputs)})


## RAG call results or something
tracer.add_log("rag", inputs={**rag_query}, outputs={**rag_docs_etc})


## towards the end of execution, usually before sending the reply back or final output
tracer.final(output={**your final message or the output})
```

Leveraging either their [UI](https://docs.smith.langchain.com/user_guide){:target="_blank"} or SDK, you have the flexibility to meticulously select and integrate traces into your testing pipeline or direct them towards an annotation queue, especially if your process incorporates human labelers.

The essence of this approach underscores the necessity of a robust tracing infrastructure within your LLM application, enabling the tracking of key metrics. It's imperative to monitor metadata associated with inputs, such as chunk-size, model, prompt, and the number of documents. The more comprehensive your tracking, the more accurately you can assess what aspects are performing optimally and which areas require refinement.

The choice of tracing application remains a matter of personal preference. Options range from DataDog and OpenTrace to custom-built solutions using Clickhouse or Postgres. However, managed services like Langsmith or Arize offer distinct advantages, particularly in streamlining test case automation and facilitating the collection of annotations via human labelers.

> Also the traces and spans let you monitor your number of token usage, latency and pricing.

### SQL Database for tracing:

Although tools such as Arize and Langsmith offer impressive features, they are not indispensable. You can adopt a strategy to monitor events using a tabular format as shown below as long as your infrastructure can support it

| query_id | question      | response     | source_documents | chunks               | mean_cosine_scores | re_ranker_score | metadata        |
| -------- | ------------- | ------------ | ---------------- | -------------------- | ------------------ | --------------- | --------------- |
| 1        | user-question | llm-response | [docid1, docid2] | [chunkid1, chunkid2] | 0.855              | 0.8             | {***json-based} |
| 2        | ...           | ...          | []               | []                   |                    |                 | {****}          |

Additionally, you can track user feedback in a separate table, linked by query IDs. This feedback on whether responses were helpful or not can be instrumental in fine-tuning your model or overall understanding how model could be improved later

| query_id | user_id | helpful | response_suggestion | response_critique |
| -------- | ------- | ------- | ------------------- | ----------------- |
| 1        | user-id | yes/no  | re-written response | user-feedback     |
| 2        | ...     | ...     | ...                 | ...               |

### Prompt Management (Versioning):

Implementing an effective version control system for your prompts can significantly enhance your testing processes. Consider the scenario where you're conducting A/B tests between two different sets of prompts to determine which yields better performance. The ability to trace the evolution of your prompts—reviewing every change to understand whether these modifications have led to improvements or declines in production performance—can be incredibly valuable.

The method you choose for managing version control of your prompts is entirely up to you. Langsmith offers a private hub that allows you to track versions of your prompts along with their input variables, although this might not significantly enhance your prompt management strategy. Personally, I prefer to maintain prompts within a code editor, typically in .txt or .py files, with a designated variable for version control, and organize them within a specific directory.

```shell
prompts/
    system_prompt/
            2023-12-28.txt
            2024-01-12.txt

    other_prompts/
```

However, managing prompts in this manner presents challenges, particularly within a production-grade system where updates necessitate a code deployment. An alternative approach involves utilizing the Langsmith hub. Regardless of the method, it's imperative to exercise extreme caution when updating prompts in production, ensuring thorough testing in a lower environment beforehand.

```python
SYSTEM_PROMPT = hub.pull(f"system_prompt:{prompt_versopm}").template
```

Now, the version of the prompt must be retrieved from the configuration or your database at the time of inference. Alternatively, you can configure your system to always use the most recent version of the prompt.

### RAG Evaluation:

When working with proprietary and domain-specific data in your LLM application, it's crucial to implement robust measures for evaluating your Retrieval-Augmented Generation (RAG) pipeline. A comprehensive RAG pipeline typically encompasses the following components:

- An embedding model, which can be either proprietary or open-source. For benchmarking, consider the [MTEB benchmark](https://huggingface.co/spaces/mteb/leaderboard){:target="_blank"}.

- A vector store, such as PgVector, Pinecone, or similar.

- A chunking strategy detailing how data is segmented and whether chunks overlap.

- Document ingestion processes to ensure clean data extraction from PDFs, HTML, or other formats.

- Metadata filtering to refine the embedding search space through specific criteria.

- A combination of hybrid search techniques or [Reciprocal Rank Fusion](https://www.elastic.co/guide/en/elasticsearch/reference/current/rrf.html){:target="_blank"}, utilizing both dense and sparse vectors, possibly integrating a BM25 filter for enhanced keyword search.

- A [re-ranker or cross-encoder](https://txt.cohere.com/rerank/){:target="_blank"} to improve result relevance.

- Query expansion techniques for optimizing the search experience through query rewriting or extraction.

Initiating a RAG pipeline might seem straightforward, but constructing a production-grade, accurate system introduces numerous complexities. For instance, replacing an embedding model with one of a different dimensionality necessitates regenerating all embeddings, a task manageable within a new database or index. Similarly, modifications to chunking strategies, document parsing, or the implementation of Reciprocal Rank Fusion or metadata-based filtering raise questions about the efficacy of these changes.

To address these challenges, it's essential to develop specialized, robust test cases focused on retrieval. Unlike end-to-end LLM evaluations, testing individual components of the RAG pipeline can provide insightful feedback. Recommended test cases include:

- Precision@K
- Recall
- Mean Cosine Scores and Re-ranker scores

Tracking these metrics requires a collection of 100-200 diverse test cases tailored to your specific use case. Regular analysis of RAG results upon any modification or content addition is vital.

Enhance your RAG pipeline evaluation by meticulously documenting metadata, such as top-k results, the size of the last chunk used, and the embedding model employed. The more metadata you track, the more nuanced your understanding of the pipeline's performance, facilitating targeted improvements.

**Embedding based cluster analysis**:

Utilizing [HDBSCAN](https://umap-learn.readthedocs.io/en/latest/clustering.html){:target="_blank"} to segment embeddings into distinct inference groups can be instrumental in pinpointing segments of your embeddings that are underperforming or deviating from expected patterns. Similarly, [UMAP](https://umap-learn.readthedocs.io/en/latest/clustering.html){:target="_blank"} can facilitate a deeper comprehension of how your embeddings capture semantic meanings in a format that's easy to visualize. ArizeAI offers an impressive 3D visualization tool that's worth exploring, although I haven't personally experimented with it yet.

For those with access to production data, initiating a notebook to visualize and dissect embeddings can be enlightening. In this context, tools like [Arize](https://arize.com/llm/){:target="_blank"} prove to be invaluable resources for such analytical endeavors.

## Fine-Tuning:

Details on fine-tuning metrics and their significance will be provided in the future. As of now, I have not systematically tracked these metrics. However, I am currently in the process of doing so and plan to share insights on the necessity and impact of fine-tuning a model based on my experiences. This section will be updated accordingly.

## Conclusion:

In the rapidly evolving domain of production-grade LLM applications, there exists no one-size-fits-all strategy. The current GPU shortage raises questions about the capability of mid to smaller sized companies to support workloads exceeding 1M+ QPS. However, it's anticipated that these capacity constraints will diminish over time. Nonetheless, for LLM operations of any scale, it's crucial to have robust operational components in place. These include diligent response monitoring and establishing benchmarks for accuracy, relevancy, and RAG metrics. Such measures empower developers to make informed modifications with confidence, supported by data, and to pinpoint precise areas where adjustments are necessary.

## References

- [RAG (Retrieval-Augmented Generation) ](https://arxiv.org/pdf/2005.11401.pdf){:target="_blank"}
- [RAGAS](https://github.com/explodinggradients/ragas){:target="_blank"}
- [Langsmith](https://docs.smith.langchain.com/user_guide){:target="_blank"}
- [UMAP & HDBSCAN](https://umap-learn.readthedocs.io/en/latest/clustering.html){:target="_blank"}
- [MTEB benchmark](https://huggingface.co/spaces/mteb/leaderboard){:target="_blank"}
- [OpenTelemetry](https://opentelemetry.io/docs/concepts/signals/traces/){:target="_blank"}
- [Cohere Rerank](https://txt.cohere.com/rerank/){:target="_blank"}