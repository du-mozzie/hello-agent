# Chapter 07 - Build Your Own Agent Framework

## Goal

Expose the framework primitives needed to build agents from scratch: LLM interface, tools, registry, messages, and agent loops.

## Implemented Code

- `BaseLLM`
- `Tool`
- `ToolRegistry`
- `ReActAgent`
- `default_registry`

## Run

```powershell
python examples/chapter07_build_framework.py
```

## Extension

Add typed tool schemas, streaming events, retry policy, and persistent run traces for production use.
