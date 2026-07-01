# Training Module

Module: `helloagents.training`

The training module provides data and reward utilities for Agentic RL workflows.

## Components

- `TrainingExample`: prompt and response pair for SFT-style data.
- `PreferenceExample`: prompt with chosen/rejected responses for preference training.
- `DatasetBuilder`: collects SFT and preference examples and exports JSONL.
- `RewardFunction`: composable scoring utility.
- `LoRAConfig`: lightweight fine-tuning configuration.
- `GRPOConfig`: agentic RL configuration placeholder.
- `TrainingPipelinePlan`: command plan for validation, SFT, GRPO, and evaluation.
- `save_jsonl` and `load_jsonl`: portable dataset helpers.

## Example

```python
from helloagents import RewardFunction

reward = RewardFunction.format_reward([r"Thought:", r"Action:"])
print(reward("Thought: inspect\nAction: search[agent]", ""))
```

## Scope

This module does not run GPU training. It prepares data and rewards that can be handed to external SFT, LoRA, GRPO, or distributed training stacks.

## Data Quality Checklist

- Prompts should include task, constraints, and available tools.
- Responses should include the expected reasoning/action format when training a ReAct-style agent.
- Preference examples should differ on correctness, grounding, format, or safety.
- Rewards should be deterministic before adding LLM-as-judge scoring.
