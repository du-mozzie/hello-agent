# Chapter 06 - Framework Development Practice

## Goal

Show how multi-agent framework ideas map to local abstractions before using LangGraph, AutoGen, CAMEL, or AgentScope.

## Implemented Code

- `A2AAgent`
- `SimpleAgent`
- shared `Message` and `AgentResult`

## Run

```powershell
python examples/chapter06_framework_practice.py
```

## Extension

Wrap external frameworks behind the same agent result interface so the rest of the project can evaluate and orchestrate them consistently.
