# 第 1 章：初识智能体

## 学习目标

理解智能体的最小结构：接收用户输入、结合系统提示词、调用推理组件、返回结果，并保存必要的消息历史。

## 对应实现

- `helloagents.schema.Message`
- `helloagents.schema.AgentResult`
- `helloagents.agents.BaseAgent`
- `helloagents.agents.SimpleAgent`

## 运行示例

```powershell
python examples/chapter01_first_agent.py
```

## 代码要点

`SimpleAgent` 是最小可用 Agent。它只做一次 LLM 调用，但已经具备 Agent 的基本边界：输入、模型、历史、输出结构。

## 扩展方向

替换 `RuleBasedLLM` 为 `OpenAICompatibleLLM`，就可以把离线演示切换成真实模型调用。
