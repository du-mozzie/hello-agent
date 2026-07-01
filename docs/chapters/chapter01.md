# Chapter 01 - Introduction to Agents

## Goal

Understand the minimal shape of an agent: receive input, hold instructions, call a reasoning component, and return an answer.

## Implemented Code

- `helloagents.schema.Message`
- `helloagents.schema.AgentResult`
- `helloagents.agents.BaseAgent`
- `helloagents.agents.SimpleAgent`

## Run

```powershell
python examples/chapter01_first_agent.py
```

## Extension

Replace `RuleBasedLLM` with `OpenAICompatibleLLM` when a real model endpoint is available. Keep the same `SimpleAgent` interface.
