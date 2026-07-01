# 第 6 章：框架开发实践

## 学习目标

理解多智能体框架的基本协作方式，并把外部框架思想映射到本地统一接口。

## 对应实现

- `A2AAgent`
- `SimpleAgent`
- `Message`
- `AgentResult`

## 运行示例

```powershell
python examples/chapter06_framework_practice.py
```

## 代码要点

`A2AAgent` 展示了两个 Agent 之间如何发送消息和接收回复。它是理解 AutoGen、LangGraph、CAMEL 等框架的最小抽象。

## 扩展方向

可以把外部框架包装成相同的 `AgentResult` 输出，统一接入评估和日志系统。
