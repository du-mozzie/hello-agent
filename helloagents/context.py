"""Context engineering helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .memory import WorkingMemory
from .schema import Message


class NoteStore:
    """Simple named note collection for long-running tasks."""

    def __init__(self) -> None:
        self._notes: dict[str, str] = {}

    def write(self, name: str, content: str) -> None:
        self._notes[name] = content

    def append(self, name: str, content: str) -> None:
        current = self._notes.get(name, "")
        self._notes[name] = f"{current}\n{content}".strip()

    def read(self, name: str) -> str:
        return self._notes[name]

    def render(self) -> str:
        return "\n\n".join(f"## {name}\n{content}" for name, content in self._notes.items())


@dataclass(slots=True)
class WorkspaceSnapshot:
    root: Path
    files: list[str] = field(default_factory=list)

    @classmethod
    def scan(cls, root: str | Path, patterns: tuple[str, ...] = ("*.py", "*.md")) -> "WorkspaceSnapshot":
        base = Path(root)
        files: list[str] = []
        for pattern in patterns:
            files.extend(str(path.relative_to(base)) for path in base.rglob(pattern) if path.is_file())
        return cls(root=base, files=sorted(files))

    def render(self, limit: int = 40) -> str:
        shown = self.files[:limit]
        suffix = "" if len(self.files) <= limit else f"\n... {len(self.files) - limit} more files"
        return "\n".join(shown) + suffix


class ContextBuilder:
    """Assemble bounded context from instructions, memory, notes, and files."""

    def __init__(self, max_chars: int = 6000) -> None:
        self.max_chars = max_chars
        self.sections: list[tuple[str, str]] = []

    def add_section(self, title: str, content: str) -> "ContextBuilder":
        if content.strip():
            self.sections.append((title, content.strip()))
        return self

    def add_messages(self, messages: list[Message]) -> "ContextBuilder":
        rendered = "\n".join(f"{message.role}: {message.content}" for message in messages)
        return self.add_section("Messages", rendered)

    def add_working_memory(self, memory: WorkingMemory) -> "ContextBuilder":
        return self.add_section("Working Memory", memory.render())

    def add_notes(self, notes: NoteStore) -> "ContextBuilder":
        return self.add_section("Notes", notes.render())

    def build(self) -> str:
        rendered = "\n\n".join(f"# {title}\n{content}" for title, content in self.sections)
        if len(rendered) <= self.max_chars:
            return rendered
        return rendered[-self.max_chars :]


@dataclass(slots=True)
class ContextItem:
    title: str
    content: str
    priority: int = 50


class PriorityContextBuilder:
    """Context builder that keeps high-priority sections first."""

    def __init__(self, max_chars: int = 6000) -> None:
        self.max_chars = max_chars
        self.items: list[ContextItem] = []

    def add(self, title: str, content: str, priority: int = 50) -> "PriorityContextBuilder":
        if content.strip():
            self.items.append(ContextItem(title=title, content=content.strip(), priority=priority))
        return self

    def build(self) -> str:
        selected: list[str] = []
        size = 0
        for item in sorted(self.items, key=lambda value: value.priority, reverse=True):
            block = f"# {item.title}\n{item.content}"
            if size + len(block) + 2 > self.max_chars:
                continue
            selected.append(block)
            size += len(block) + 2
        return "\n\n".join(selected)
