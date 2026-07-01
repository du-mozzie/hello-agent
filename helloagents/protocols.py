"""Communication protocol primitives: MCP-like tools, A2A, and ANP."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from uuid import uuid4

from .agents import SimpleAgent
from .schema import Message
from .tools import Tool


class MCPToolAdapter:
    """Expose a local Tool through a minimal MCP-like schema."""

    def __init__(self, tool: Tool) -> None:
        self.tool = tool

    def describe(self) -> dict[str, str]:
        return {"name": self.tool.name, "description": self.tool.description, "input_schema": "string"}

    def call(self, arguments: dict[str, str]) -> dict[str, str]:
        return {"content": self.tool.run(arguments.get("input", ""))}


@dataclass(slots=True)
class A2AMessage:
    sender: str
    receiver: str
    content: str
    message_id: str = field(default_factory=lambda: uuid4().hex)


class A2AAgent:
    """Agent wrapper that exchanges direct messages with peers."""

    def __init__(self, agent: SimpleAgent) -> None:
        self.agent = agent
        self.inbox: list[A2AMessage] = []

    @property
    def name(self) -> str:
        return self.agent.name

    def receive(self, message: A2AMessage) -> A2AMessage:
        self.inbox.append(message)
        result = self.agent.run(message.content)
        return A2AMessage(sender=self.name, receiver=message.sender, content=result.answer)

    def send(self, peer: "A2AAgent", content: str) -> A2AMessage:
        return peer.receive(A2AMessage(sender=self.name, receiver=peer.name, content=content))


class ANPRegistry:
    """Small service-discovery registry for agents and tools."""

    def __init__(self) -> None:
        self._services: dict[str, object] = {}

    def publish(self, name: str, service: object) -> None:
        self._services[name] = service

    def discover(self, keyword: str = "") -> list[str]:
        lowered = keyword.lower()
        return sorted(name for name in self._services if lowered in name.lower())

    def get(self, name: str) -> object:
        return self._services[name]


class TaskDistributor:
    """Assign tasks to named agents by capability keyword."""

    def __init__(self) -> None:
        self.capabilities: dict[str, set[str]] = defaultdict(set)

    def register(self, agent_name: str, capabilities: list[str]) -> None:
        self.capabilities[agent_name].update(capability.lower() for capability in capabilities)

    def assign(self, task: str) -> str | None:
        tokens = set(task.lower().split())
        best_agent = None
        best_score = 0
        for agent_name, capabilities in self.capabilities.items():
            score = len(tokens & capabilities)
            if score > best_score:
                best_agent = agent_name
                best_score = score
        return best_agent


class RoundRobinLoadBalancer:
    """Round-robin selection for a pool of equivalent agents."""

    def __init__(self, agents: list[str]) -> None:
        if not agents:
            raise ValueError("agents cannot be empty.")
        self.agents = agents
        self.index = 0

    def next(self) -> str:
        agent = self.agents[self.index % len(self.agents)]
        self.index += 1
        return agent


@dataclass(slots=True)
class NegotiationOffer:
    sender: str
    terms: dict[str, float]
    message: str = ""


class SimpleNegotiator:
    """Score offers and choose the one with the best weighted utility."""

    def __init__(self, weights: dict[str, float]) -> None:
        self.weights = weights

    def score(self, offer: NegotiationOffer) -> float:
        return sum(offer.terms.get(term, 0.0) * weight for term, weight in self.weights.items())

    def choose(self, offers: list[NegotiationOffer]) -> NegotiationOffer:
        if not offers:
            raise ValueError("offers cannot be empty.")
        return max(offers, key=self.score)
