# 第 4 章：智能体经典范式构建

## 学习目标

掌握常见 Agent 控制流：单次调用、ReAct、Plan-and-Solve 和 Reflection。

## 对应实现

- `SimpleAgent`
- `ReActAgent`
- `PlanAndSolveAgent`
- `ReflectionAgent`
- `ToolRegistry`

## 运行示例

```powershell
python examples/chapter04_classic_paradigms.py
```

## 代码要点

`ReActAgent` 会产生 Thought、Action、Observation 步骤；`PlanAndSolveAgent` 先规划再回答；`ReflectionAgent` 先草稿、再反思、再修订。

## 扩展方向

为每类 Agent 增加结构化输出、失败重试、成本控制和更严格的评估指标。
