# 第 5 章：基于低代码平台的智能体搭建

## 学习目标

理解 Dify、Coze、FastGPT、n8n 等低代码平台中常见的节点、边、模型节点、工具节点和输出节点。

## 对应实现

- `LowCodeFlow`
- `PlatformAdapter`
- `hello_agent_flow`

## 运行示例

```powershell
python examples/chapter05_lowcode.py
```

## 代码要点

本项目用统一图结构表达低代码流程。这样可以对比不同平台的共同抽象，而不是绑定某一个平台的私有格式。

## 扩展方向

为具体平台实现更完整的导入/导出适配器，例如 Dify DSL、n8n workflow JSON 或 FastGPT 应用配置。
