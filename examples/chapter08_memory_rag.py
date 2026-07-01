from helloagents import MemoryConsolidator, RAGPipeline, RAGQAAssistant, VectorMemory, WorkingMemory


if __name__ == "__main__":
    vector = VectorMemory()
    rag = RAGPipeline(vector)
    rag.ingest(
        {
            "memory": "Working memory keeps recent state. Vector memory retrieves relevant knowledge.",
            "rag": "RAG retrieves documents before generating an answer.",
        }
    )
    print(RAGQAAssistant(rag).answer("How does memory retrieval help agents?"))

    working = WorkingMemory()
    working.add("User prefers concise examples.")
    consolidated = MemoryConsolidator(working, vector).consolidate()
    print("Consolidated:", consolidated.content if consolidated else "none")
