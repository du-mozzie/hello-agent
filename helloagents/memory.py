"""Memory and retrieval primitives."""

from __future__ import annotations

import math
import re
from collections import Counter, deque
from dataclasses import dataclass, field
from time import time


@dataclass(slots=True)
class MemoryRecord:
    content: str
    kind: str = "semantic"
    metadata: dict[str, object] = field(default_factory=dict)
    created_at: float = field(default_factory=time)


class WorkingMemory:
    """Bounded short-term memory."""

    def __init__(self, max_items: int = 8) -> None:
        self._items: deque[MemoryRecord] = deque(maxlen=max_items)

    def add(self, content: str, **metadata: object) -> MemoryRecord:
        record = MemoryRecord(content, kind="working", metadata=metadata)
        self._items.append(record)
        return record

    def list(self) -> list[MemoryRecord]:
        return list(self._items)

    def render(self) -> str:
        return "\n".join(record.content for record in self._items)


class ConversationMemory:
    """Conversation memory split into a rolling window and a summary."""

    def __init__(self, window_size: int = 6) -> None:
        self.window = WorkingMemory(max_items=window_size)
        self.summary = ""

    def add_turn(self, user: str, assistant: str) -> None:
        self.window.add(f"user: {user}\nassistant: {assistant}")

    def consolidate(self) -> str:
        turns = self.window.list()
        if not turns:
            return self.summary
        compact = " | ".join(record.content.replace("\n", " ") for record in turns)
        self.summary = f"{self.summary} {compact}".strip()
        return self.summary

    def render(self) -> str:
        parts = []
        if self.summary:
            parts.append(f"Summary: {self.summary}")
        if self.window.list():
            parts.append("Recent turns:\n" + self.window.render())
        return "\n\n".join(parts)


class EpisodicMemory:
    """Append-only event memory."""

    def __init__(self) -> None:
        self._records: list[MemoryRecord] = []

    def add(self, content: str, kind: str = "episode", **metadata: object) -> MemoryRecord:
        record = MemoryRecord(content=content, kind=kind, metadata=metadata)
        self._records.append(record)
        return record

    def recent(self, limit: int = 5) -> list[MemoryRecord]:
        return self._records[-limit:]

    def all(self) -> list[MemoryRecord]:
        return list(self._records)


class VectorMemory:
    """Tiny bag-of-words vector store suitable for local demos."""

    def __init__(self) -> None:
        self._records: list[MemoryRecord] = []

    def add(self, content: str, **metadata: object) -> MemoryRecord:
        record = MemoryRecord(content=content, kind="vector", metadata=metadata)
        self._records.append(record)
        return record

    def search(self, query: str, top_k: int = 3) -> list[MemoryRecord]:
        query_vec = _vectorize(query)
        scored = []
        for record in self._records:
            score = _cosine(query_vec, _vectorize(record.content))
            if score > 0:
                scored.append((score, record))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [record for _, record in scored[:top_k]]


class RAGPipeline:
    """Retrieve memories and build an answer prompt."""

    def __init__(self, memory: VectorMemory) -> None:
        self.memory = memory

    def ingest(self, documents: dict[str, str]) -> None:
        for title, content in documents.items():
            self.memory.add(content, title=title)

    def retrieve_context(self, query: str, top_k: int = 3) -> str:
        records = self.memory.search(query, top_k=top_k)
        return "\n".join(f"[{record.metadata.get('title', 'doc')}] {record.content}" for record in records)

    def build_prompt(self, query: str, top_k: int = 3) -> str:
        context = self.retrieve_context(query, top_k)
        return f"Use the context to answer.\nContext:\n{context}\n\nQuestion: {query}"


class MemoryConsolidator:
    """Move short-term observations into longer-term retrievable memory."""

    def __init__(self, working: WorkingMemory, vector: VectorMemory) -> None:
        self.working = working
        self.vector = vector

    def consolidate(self, label: str = "consolidated") -> MemoryRecord | None:
        items = self.working.list()
        if not items:
            return None
        content = "\n".join(record.content for record in items)
        return self.vector.add(content, label=label, item_count=len(items))


class RAGQAAssistant:
    """Small retrieval QA facade for demos."""

    def __init__(self, pipeline: RAGPipeline) -> None:
        self.pipeline = pipeline

    def answer(self, question: str) -> str:
        context = self.pipeline.retrieve_context(question)
        if not context:
            return "I do not have enough local context to answer."
        return f"Based on the retrieved context:\n{context}"


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9_]+", text.lower())


def _vectorize(text: str) -> Counter[str]:
    return Counter(_tokens(text))


def _cosine(left: Counter[str], right: Counter[str]) -> float:
    if not left or not right:
        return 0.0
    numerator = sum(left[key] * right[key] for key in left.keys() & right.keys())
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    return numerator / (left_norm * right_norm) if left_norm and right_norm else 0.0
