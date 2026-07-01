# 训练与 Agentic RL

模块：`helloagents.training`

该模块不直接训练大模型，而是提供训练数据、偏好数据、奖励函数和训练计划配置，便于接入外部 SFT、LoRA、DPO 或 GRPO 框架。

## 组件

- `TrainingExample`：SFT 样例，包含 prompt 和 response。
- `PreferenceExample`：偏好样例，包含 chosen 和 rejected。
- `DatasetBuilder`：收集并导出 SFT/偏好数据。
- `RewardFunction`：可组合的文本奖励函数。
- `LoRAConfig`：LoRA 参数配置。
- `GRPOConfig`：GRPO 参数配置。
- `TrainingPipelinePlan`：训练流水线命令计划。
- `save_jsonl` / `load_jsonl`：JSONL 数据读写。

## 示例

```python
from helloagents import DatasetBuilder, RewardFunction

builder = DatasetBuilder()
builder.add_sft("Solve with ReAct: 2+2", "Thought: calculate\nAction: calculator[2+2]")

reward = RewardFunction.format_reward([r"Thought:", r"Action:"])
print(reward("Thought: calculate\nAction: calculator[2+2]"))
```

## 数据质量建议

- Prompt 应包含任务、约束和可用工具。
- Response 应体现目标格式，例如 ReAct 的 Thought/Action。
- 偏好数据应在正确性、格式、引用、工具使用或安全性上形成明显差异。
- 奖励函数先保持确定性，再考虑引入 LLM-as-judge。
