from helloagents.tools import ToolRegistry, calculator_tool, local_search_tool, safe_calculate


def test_safe_calculate_supports_arithmetic():
    assert safe_calculate("(25 + 15) * 3 - 8") == 112


def test_tool_registry_executes_registered_tool():
    registry = ToolRegistry()
    registry.register(calculator_tool())
    assert registry.execute("calculator", "2 + 3 * 4") == "14"


def test_local_search_returns_matching_document():
    tool = local_search_tool({"react": "ReAct uses reasoning and actions."})
    assert "ReAct" in tool.run("reasoning")
