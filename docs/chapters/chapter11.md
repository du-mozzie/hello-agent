# Chapter 11 - Agentic RL

## Goal

Prepare data and rewards for agent training workflows without requiring a GPU training stack.

## Implemented Code

- `TrainingExample`
- `PreferenceExample`
- `DatasetBuilder`
- `RewardFunction`
- `LoRAConfig`
- `GRPOConfig`
- `TrainingPipelinePlan`

## Run

```powershell
python examples/chapter11_agentic_rl.py
```

## Extension

Feed exported JSONL into external SFT, LoRA, DPO, or GRPO frameworks. Keep rewards deterministic before adding LLM judges.
