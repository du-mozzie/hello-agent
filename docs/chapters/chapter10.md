# 第 10 章：智能体通信协议

## 学习目标

理解 MCP-like 工具调用、A2A 智能体通信、ANP 服务发现、任务分发、负载均衡和协商机制。

## 对应实现

- `MCPToolAdapter`
- `A2AAgent`
- `ANPRegistry`
- `TaskDistributor`
- `RoundRobinLoadBalancer`
- `SimpleNegotiator`

## 运行示例

```powershell
python examples/chapter10_protocols.py
```

## 代码要点

本章代码提供本地版本的协议抽象，便于先理解边界，再替换成真实网络协议。

## 扩展方向

加入 HTTP transport、鉴权、schema 校验、重试、队列和服务健康检查。
