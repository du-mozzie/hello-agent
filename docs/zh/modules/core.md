# 核心模型

模块：`helloagents.schema`

核心模型模块定义了整个项目共享的数据结构。其他模块不直接传递松散的字典，而是尽量通过这些结构表达消息、工具调用、执行步骤和最终结果。

## 核心类型

- `Message`：聊天消息，包含 `role`、`content`、可选 `name`、元数据和创建时间。
- `ToolCall`：结构化工具调用请求，包含工具名、输入和可选调用 ID。
- `StepEvent`：智能体执行过程中的可观察事件，例如 thought、action、observation、plan、critique。
- `AgentResult`：智能体运行结果，包含最终答案、步骤列表、消息历史和元数据。

## 示例

```python
from helloagents import AgentResult, Message

messages = [Message("user", "你好")]
result = AgentResult(answer="你好，我是一个智能体。", messages=messages)
result.add_step("note", "完成了一次简单回复")
```

## 设计原则

核心模型不依赖 LLM、工具、记忆或协议模块。这样可以保证：

- 单元测试更简单。
- Agent、评估器、应用层可以复用同一套结果结构。
- 后续接入 UI、API 或日志系统时不需要重写数据协议。
