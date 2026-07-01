from helloagents import ContextBuilder, NoteStore, RAGPipeline, VectorMemory, WorkingMemory


def test_vector_memory_retrieves_relevant_record():
    memory = VectorMemory()
    memory.add("ReAct combines reasoning and tool actions.", title="react")
    memory.add("Transformers use attention.", title="llm")
    results = memory.search("reasoning actions")
    assert results[0].metadata["title"] == "react"


def test_rag_pipeline_builds_prompt():
    rag = RAGPipeline(VectorMemory())
    rag.ingest({"memory": "Agents can retrieve memory."})
    prompt = rag.build_prompt("retrieve memory")
    assert "Agents can retrieve memory" in prompt


def test_context_builder_includes_notes_and_memory():
    notes = NoteStore()
    notes.write("goal", "build docs")
    memory = WorkingMemory()
    memory.add("recent task")
    context = ContextBuilder().add_notes(notes).add_working_memory(memory).build()
    assert "build docs" in context
    assert "recent task" in context
