from helloagents import PlanAndSolveAgent, ReActAgent, ReflectionAgent, SimpleAgent


def test_simple_agent_returns_answer():
    result = SimpleAgent("simple").run("Hello")
    assert result.answer
    assert len(result.messages) == 2


def test_react_agent_uses_calculator():
    result = ReActAgent(max_steps=3).run("What is (25 + 15) * 3 - 8?")
    assert result.answer == "112"
    assert any(step.type == "observation" for step in result.steps)


def test_plan_and_solve_agent_records_plan():
    result = PlanAndSolveAgent("planner").run("Plan a test")
    assert result.answer
    assert result.steps[0].type == "plan"


def test_reflection_agent_records_critique():
    result = ReflectionAgent("reflector").run("Explain agents")
    assert result.answer
    assert any(step.type == "critique" for step in result.steps)
