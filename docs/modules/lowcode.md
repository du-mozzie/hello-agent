# 低代码平台

模块：`helloagents.lowcode`

该模块把低代码智能体平台中的工作流抽象成可移植图结构，用于对比 Dify、Coze、FastGPT 和 n8n 等平台的核心概念。

## 组件

- `LowCodeFlow`：流程图，包含节点和边。
- `PlatformAdapter`：按平台名导出流程 JSON。
- `hello_agent_flow()`：示例工作流，包含输入、LLM、工具和输出节点。

## 示例

```python
from helloagents.lowcode import PlatformAdapter, hello_agent_flow

flow = hello_agent_flow()
PlatformAdapter("dify").export(flow, "exports/dify-flow.json")
```

## 说明

导出的 JSON 是教学用的统一格式，不保证可以直接导入所有平台。真实平台通常需要额外字段，例如应用 ID、凭据、节点位置、变量声明和知识库配置。

## 扩展建议

可以为每个平台新增更具体的 adapter，把统一流程转换为该平台真实的导入格式。
