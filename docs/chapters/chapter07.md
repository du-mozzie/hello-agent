# 第 7 章：构建你的 Agent 框架

## 学习目标

从零理解 Agent 框架需要哪些基础模块：LLM 接口、工具抽象、工具注册表、消息结构和 Agent 循环。

## 对应实现

- `BaseLLM`
- `Tool`
- `ToolRegistry`
- `ReActAgent`
- `default_registry`

## 运行示例

```powershell
python examples/chapter07_build_framework.py
```

## 代码要点

自定义工具只需要实现一个函数，然后注册到 `ToolRegistry`。Agent 只依赖工具描述和执行接口，不关心工具内部实现。

## 扩展方向

增加工具 schema、运行追踪、流式输出、并发执行和持久化 run 记录。
