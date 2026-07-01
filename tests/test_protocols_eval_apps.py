from pathlib import Path

from helloagents import A2AAgent, Evaluator, SimpleAgent, TaskCase, TravelPlanner
from helloagents.lowcode import PlatformAdapter, hello_agent_flow
from helloagents.protocols import ANPRegistry, MCPToolAdapter
from helloagents.tools import calculator_tool


def test_mcp_tool_adapter_calls_tool():
    adapter = MCPToolAdapter(calculator_tool())
    assert adapter.call({"input": "2 + 2"})["content"] == "4"


def test_a2a_agent_round_trip():
    alice = A2AAgent(SimpleAgent("alice"))
    bob = A2AAgent(SimpleAgent("bob"))
    reply = alice.send(bob, "Hello")
    assert reply.sender == "bob"
    assert reply.receiver == "alice"


def test_anp_registry_discovers_service():
    registry = ANPRegistry()
    registry.publish("math-agent", object())
    assert registry.discover("math") == ["math-agent"]


def test_evaluator_scores_cases():
    report = Evaluator().evaluate(SimpleAgent("demo"), [TaskCase("Hello", "deterministic", "contains")])
    assert report.score == 1.0


def test_travel_planner_outputs_days():
    itinerary = TravelPlanner().plan("Shanghai", "museums, coffee", days=2)
    assert "Day 1" in itinerary
    assert "Day 2" in itinerary


def test_lowcode_export(tmp_path: Path):
    target = tmp_path / "flow.json"
    PlatformAdapter("dify").export(hello_agent_flow(), target)
    assert target.exists()
