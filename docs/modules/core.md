# Core Module

Module: `helloagents.schema`

The core module defines the shared data structures used by the rest of the project.

## Main Types

- `Message`: chat-style message with `role`, `content`, optional `name`, metadata, and timestamp.
- `ToolCall`: structured request to execute a named tool.
- `StepEvent`: observable intermediate event such as a thought, action, observation, plan, or critique.
- `AgentResult`: final answer plus steps, messages, and metadata.

## Usage

```python
from helloagents import AgentResult, Message

messages = [Message("user", "hello")]
result = AgentResult(answer="hi", messages=messages)
result.add_step("note", "The request was handled.")
```

## Design Notes

The schema layer has no dependency on LLM providers, tools, or frameworks. This keeps every higher-level module testable and easy to serialize.
