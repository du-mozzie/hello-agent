# LLMs Module

Module: `helloagents.llms`

This module provides a small model interface used by every agent.

## Classes

- `BaseLLM`: abstract interface with `complete(messages)` and convenience `invoke(prompt)`.
- `RuleBasedLLM`: deterministic offline implementation for tests and examples.
- `OpenAICompatibleLLM`: optional client for OpenAI-compatible APIs.

## Offline Example

```python
from helloagents import RuleBasedLLM

llm = RuleBasedLLM()
print(llm.invoke("What is 1 + 2?"))
```

## OpenAI-Compatible Example

```python
from helloagents import OpenAICompatibleLLM

llm = OpenAICompatibleLLM(model="gpt-4o-mini")
print(llm.invoke("Explain ReAct in one paragraph."))
```

Install optional dependencies first:

```powershell
pip install -e .[openai]
```

Required environment variable: `OPENAI_API_KEY`.
