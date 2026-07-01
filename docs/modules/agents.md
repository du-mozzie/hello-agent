# 智能体范式

模块：`helloagents.agents`

该模块实现教程中的经典智能体控制循环，从简单 LLM 调用到 ReAct、Plan-and-Solve 和 Reflection。

## 组件

- `BaseAgent`：所有智能体的基础类，保存名称、系统提示词、LLM 和消息历史。
- `SimpleAgent`：单轮模型调用，适合理解最小智能体结构。
- `ReActAgent`：交替执行 `Thought`、`Action`、`Observation`。
- `PlanAndSolveAgent`：先规划，再基于计划回答。
- `ReflectionAgent`：先生成草稿，再反思并修订。

## ReAct 示例

```python
from helloagents import ReActAgent

agent = ReActAgent(max_steps=3)
result = agent.run("What is (25 + 15) * 3 - 8?")
print(result.answer)

for step in result.steps:
    print(step.type, step.content)
```

## 执行轨迹

所有 Agent 都返回 `AgentResult`。其中 `steps` 记录中间过程，可用于：

- 调试智能体行为。
- 展示 UI 执行轨迹。
- 生成训练数据。
- 做评估和回归测试。

## 扩展建议

生产场景建议增加结构化输出解析、工具调用重试、异常恢复、最大成本限制和执行日志持久化。
