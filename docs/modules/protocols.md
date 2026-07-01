# 通信协议

模块：`helloagents.protocols`

该模块把教程中的 MCP、A2A、ANP、任务分发、负载均衡和协商思想抽象成可运行的本地实现。

## 组件

- `MCPToolAdapter`：把本地 `Tool` 暴露成 MCP-like 调用结构。
- `A2AAgent`：智能体之间直接发送消息。
- `ANPRegistry`：发布和发现命名服务。
- `TaskDistributor`：根据能力关键词分配任务。
- `RoundRobinLoadBalancer`：在多个等价 worker 之间轮询。
- `NegotiationOffer`：协商报价。
- `SimpleNegotiator`：按权重计算效用并选择最优报价。

## 示例

```python
from helloagents import TaskDistributor

distributor = TaskDistributor()
distributor.register("coding-agent", ["code", "debug", "test"])
print(distributor.assign("debug test failure"))
```

## 分层理解

本地原型可以直接调用 Python 对象。生产系统通常还需要：

- HTTP、WebSocket 或消息队列传输。
- 鉴权和权限控制。
- Schema 校验。
- 重试和幂等。
- 调用日志和审计。

本模块保留这些边界，方便以后替换成真实协议服务。
