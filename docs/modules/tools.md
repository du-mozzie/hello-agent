# Tools Module

Module: `helloagents.tools`

Tools turn external capabilities into callable functions that agents can plan around.

## Components

- `Tool`: named function with a description.
- `ToolRegistry`: registration, discovery, and execution facade.
- `calculator_tool()`: safe arithmetic tool implemented with Python AST traversal.
- `local_search_tool()`: small in-memory document search tool.
- `terminal_tool()`: allow-listed shell command tool for controlled local automation.

## Example

```python
from helloagents.tools import ToolRegistry, calculator_tool

registry = ToolRegistry()
registry.register(calculator_tool())
print(registry.execute("calculator", "(25 + 15) * 3 - 8"))
```

## Safety

`safe_calculate` does not call `eval`. `terminal_tool` only executes commands in an allow list and should be configured narrowly for production workflows.

## Tool Design Rules

Keep tool names stable, descriptions short, inputs explicit, and outputs easy to parse. For complex tools, wrap structured arguments as JSON strings or add a typed schema layer before exposing the tool to a model.
