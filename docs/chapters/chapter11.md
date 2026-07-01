# 第 11 章：Agentic RL

## 学习目标

理解 Agent 训练前的数据准备、偏好样本、奖励函数、LoRA 配置和 GRPO 流程计划。

## 对应实现

- `TrainingExample`
- `PreferenceExample`
- `DatasetBuilder`
- `RewardFunction`
- `LoRAConfig`
- `GRPOConfig`
- `TrainingPipelinePlan`

## 运行示例

```powershell
python examples/chapter11_agentic_rl.py
```

## 代码要点

本项目不直接训练模型，而是提供训练数据和配置计划。这样可以与外部 SFT、LoRA、DPO、GRPO 框架对接。

## 扩展方向

接入真实训练框架，加入模型 checkpoint、数据版本管理和训练后评估。
