# Memory Module

Module: `helloagents.memory`

Memory gives agents persistent and retrievable state.

## Components

- `WorkingMemory`: bounded short-term queue for active context.
- `ConversationMemory`: rolling conversation window plus consolidated summary.
- `EpisodicMemory`: append-only event log.
- `VectorMemory`: local bag-of-words retrieval store.
- `MemoryConsolidator`: moves short-term observations into vector memory.
- `RAGPipeline`: ingest documents, retrieve context, and build answer prompts.
- `RAGQAAssistant`: simple QA facade over retrieved context.

## Example

```python
from helloagents import RAGPipeline, VectorMemory

rag = RAGPipeline(VectorMemory())
rag.ingest({"react": "ReAct combines reasoning and tool use."})
print(rag.retrieve_context("tool reasoning"))
```

## Notes

`VectorMemory` is intentionally simple and dependency-free. Replace it with FAISS, SQLite vector extensions, Elasticsearch, or a hosted vector database when scaling.

## Recommended Workflow

1. Store the latest turns in `WorkingMemory` or `ConversationMemory`.
2. Periodically call `MemoryConsolidator` to preserve useful observations.
3. Ingest reference documents into `VectorMemory`.
4. Use `RAGPipeline.build_prompt()` before the LLM call.
5. Evaluate retrieval quality with task cases from `helloagents.evaluation`.
