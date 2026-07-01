# 第 9 章：上下文工程

## 学习目标

理解如何从用户目标、对话、笔记、记忆、工具结果和工作区信息中选择合适内容进入模型上下文。

## 对应实现

- `NoteStore`
- `WorkspaceSnapshot`
- `ContextBuilder`
- `PriorityContextBuilder`

## 运行示例

```powershell
python examples/chapter09_context_engineering.py
```

## 代码要点

`PriorityContextBuilder` 会优先保留高优先级内容。当上下文预算不足时，低优先级内容会被跳过。

## 扩展方向

增加 token 计数、上下文压缩、去重、引用来源和不同模型的上下文窗口配置。
