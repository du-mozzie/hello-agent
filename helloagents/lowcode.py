"""Low-code platform flow descriptions."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass(slots=True)
class LowCodeFlow:
    name: str
    description: str
    nodes: list[dict[str, object]] = field(default_factory=list)
    edges: list[tuple[str, str]] = field(default_factory=list)

    def add_node(self, node_id: str, kind: str, config: dict[str, object] | None = None) -> None:
        self.nodes.append({"id": node_id, "kind": kind, "config": config or {}})

    def connect(self, source: str, target: str) -> None:
        self.edges.append((source, target))


class PlatformAdapter:
    """Export a portable flow for different low-code agent platforms."""

    def __init__(self, platform: str) -> None:
        self.platform = platform.lower()

    def export(self, flow: LowCodeFlow, path: str | Path) -> None:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        payload = {"platform": self.platform, "flow": asdict(flow)}
        if self.platform in {"coze", "dify", "fastgpt", "n8n"}:
            target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        else:
            raise ValueError(f"Unsupported platform: {self.platform}")


def hello_agent_flow() -> LowCodeFlow:
    flow = LowCodeFlow("hello-agent", "A portable assistant flow with LLM, tool, and final answer nodes.")
    flow.add_node("input", "input")
    flow.add_node("llm", "llm", {"system_prompt": "You are a helpful agent."})
    flow.add_node("tool", "tool", {"name": "search"})
    flow.add_node("answer", "output")
    flow.connect("input", "llm")
    flow.connect("llm", "tool")
    flow.connect("tool", "answer")
    return flow
