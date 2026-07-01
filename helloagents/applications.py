"""End-to-end demo applications."""

from __future__ import annotations

from dataclasses import dataclass, field

from .agents import ReActAgent, SimpleAgent
from .llms import BaseLLM, RuleBasedLLM
from .memory import EpisodicMemory, VectorMemory
from .tools import ToolRegistry, calculator_tool, local_search_tool


@dataclass(slots=True)
class TripDay:
    day: int
    theme: str
    morning: str
    afternoon: str
    evening: str


@dataclass(slots=True)
class TripPlan:
    destination: str
    days: list[TripDay]

    def to_markdown(self) -> str:
        lines = [f"# {self.destination} {len(self.days)}-day itinerary"]
        for day in self.days:
            lines.extend(
                [
                    f"## Day {day.day}: {day.theme}",
                    f"- Morning: {day.morning}",
                    f"- Afternoon: {day.afternoon}",
                    f"- Evening: {day.evening}",
                ]
            )
        return "\n".join(lines)


class TravelPlanner:
    """Small itinerary planner showing planning plus tool grounding."""

    def __init__(self, llm: BaseLLM | None = None) -> None:
        self.llm = llm or RuleBasedLLM()

    def build_plan(self, destination: str, interests: str, days: int = 3) -> TripPlan:
        interests_list = [item.strip() for item in interests.split(",") if item.strip()] or ["local highlights"]
        trip_days = []
        for day in range(1, days + 1):
            theme = interests_list[(day - 1) % len(interests_list)]
            trip_days.append(
                TripDay(
                    day=day,
                    theme=theme,
                    morning=f"Visit a {theme} anchor spot in {destination}.",
                    afternoon=f"Add a nearby walk or backup indoor stop around {theme}.",
                    evening=f"Choose dinner near transit and leave buffer time.",
                )
            )
        return TripPlan(destination=destination, days=trip_days)

    def plan(self, destination: str, interests: str, days: int = 3) -> str:
        return self.build_plan(destination, interests, days).to_markdown()


@dataclass(slots=True)
class ResearchReport:
    topic: str
    plan: list[str]
    evidence: list[str]
    synthesis: str

    def to_markdown(self) -> str:
        lines = [f"# Research Brief: {self.topic}", "## Plan"]
        lines.extend(f"- {item}" for item in self.plan)
        lines.append("## Evidence")
        lines.extend(f"- {item}" for item in self.evidence)
        lines.extend(["## Synthesis", self.synthesis])
        return "\n".join(lines)


class DeepResearchAgent:
    """Offline deep-research workflow: plan, retrieve, synthesize."""

    def __init__(self, corpus: dict[str, str] | None = None, llm: BaseLLM | None = None) -> None:
        self.memory = VectorMemory()
        for title, body in (corpus or {}).items():
            self.memory.add(body, title=title)
        self.llm = llm or RuleBasedLLM()

    def build_report(self, topic: str) -> ResearchReport:
        records = self.memory.search(topic, top_k=5)
        evidence = [record.content for record in records]
        if not evidence:
            evidence = ["No local corpus was provided; rely on known project patterns."]
        plan = ["Define scope", "Gather evidence", "Compare tradeoffs", "Synthesize findings"]
        synthesis = self.llm.invoke(f"Summarize this research context for {topic}:\n" + "\n".join(evidence))
        return ResearchReport(topic=topic, plan=plan, evidence=evidence, synthesis=synthesis)

    def research(self, topic: str) -> str:
        return self.build_report(topic).to_markdown()


@dataclass(slots=True)
class TownPerson:
    name: str
    role: str
    memory: EpisodicMemory = field(default_factory=EpisodicMemory)
    affinity: dict[str, int] = field(default_factory=dict)


class CyberTown:
    """Minimal multi-agent town simulator."""

    def __init__(self) -> None:
        self.people = [
            TownPerson("Alex", "planner"),
            TownPerson("Blair", "researcher"),
            TownPerson("Casey", "builder"),
        ]

    def tick(self, event: str = "daily standup") -> list[str]:
        updates = []
        for person in self.people:
            update = f"{person.name} the {person.role} responds to {event}."
            person.memory.add(update)
            updates.append(update)
        return updates

    def interact(self, source: str, target: str, topic: str) -> str:
        source_person = self._person(source)
        self._person(target)
        source_person.affinity[target] = source_person.affinity.get(target, 0) + 1
        event = f"{source} discusses {topic} with {target}."
        source_person.memory.add(event, kind="interaction", target=target, topic=topic)
        return event

    def summary(self) -> str:
        return "\n".join(record.content for person in self.people for record in person.memory.recent(3))

    def _person(self, name: str) -> TownPerson:
        for person in self.people:
            if person.name == name:
                return person
        raise KeyError(name)


def demo_react_agent() -> ReActAgent:
    registry = ToolRegistry()
    registry.register(calculator_tool())
    registry.register(local_search_tool())
    return ReActAgent(tools=registry)
