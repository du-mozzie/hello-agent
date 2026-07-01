# Low Code Module

Module: `helloagents.lowcode`

This module represents low-code agent workflows in a portable format.

## Components

- `LowCodeFlow`: nodes and edges for an agent workflow.
- `PlatformAdapter`: exports flow JSON for `coze`, `dify`, `fastgpt`, or `n8n`.
- `hello_agent_flow()`: starter flow with input, LLM, tool, and output nodes.

## Example

```python
from helloagents.lowcode import PlatformAdapter, hello_agent_flow

flow = hello_agent_flow()
PlatformAdapter("dify").export(flow, "exports/dify-flow.json")
```

The exported JSON is a normalized teaching artifact. Real platform imports may require extra platform-specific fields.
