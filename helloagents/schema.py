"""Shared data models used across HelloAgents modules."""

from __future__ import annotations

from dataclasses import dataclass, field
from time import time
from typing import Any, Literal

Role = Literal["system", "user", "assistant", "tool"]


@dataclass(slots=True)
class Message:
    """A chat message exchanged by users, agents, LLMs, and tools."""

    role: Role
    content: str
    name: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time)

    def to_dict(self) -> dict[str, Any]:
        data = {"role": self.role, "content": self.content}
        if self.name:
            data["name"] = self.name
        return data


@dataclass(slots=True)
class ToolCall:
    """A structured request to invoke a tool."""

    name: str
    input: str
    call_id: str | None = None


@dataclass(slots=True)
class StepEvent:
    """An observable agent step."""

    type: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AgentResult:
    """Final output of an agent run."""

    answer: str
    steps: list[StepEvent] = field(default_factory=list)
    messages: list[Message] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_step(self, type_: str, content: str, **metadata: Any) -> None:
        self.steps.append(StepEvent(type_, content, metadata))
