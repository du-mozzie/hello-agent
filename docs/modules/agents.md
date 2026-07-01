# Agents Module

Module: `helloagents.agents`

The agents module implements the tutorial's main agent paradigms.

## Agents

- `SimpleAgent`: sends one prompt to an LLM.
- `ReActAgent`: alternates `Thought`, `Action`, and `Observation` steps.
- `PlanAndSolveAgent`: creates a plan before generating the final answer.
- `ReflectionAgent`: drafts, critiques, and revises.

## ReAct Example

```python
from helloagents import ReActAgent

agent = ReActAgent()
result = agent.run("What is (25 + 15) * 3 - 8?")
print(result.answer)
```

## Extension Points

Pass a custom `BaseLLM` implementation or a custom `ToolRegistry` to connect external models, APIs, databases, or MCP servers.

## Agent Loop Details

`ReActAgent` emits `StepEvent` records for thoughts, actions, and observations. These records are suitable for debugging, UI traces, evaluation, and training data generation. `PlanAndSolveAgent` and `ReflectionAgent` use the same result schema, so downstream code can compare different paradigms without special casing each one.
