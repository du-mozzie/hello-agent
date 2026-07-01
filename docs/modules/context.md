# 上下文工程

模块：`helloagents.context`

上下文工程模块负责选择哪些信息进入下一次模型调用。好的上下文工程可以减少噪声、控制成本，并提升任务完成率。

## 组件

- `NoteStore`：命名笔记，适合长期任务中保存目标、计划和结论。
- `WorkspaceSnapshot`：扫描工作区文件列表。
- `ContextBuilder`：按段落拼接上下文，并按字符预算截断。
- `PriorityContextBuilder`：按优先级选择上下文片段。
- `ContextItem`：带标题、内容和优先级的上下文项。

## 示例

```python
from helloagents import NoteStore, PriorityContextBuilder

notes = NoteStore()
notes.write("goal", "构建一个完整的 HelloAgents 项目")

context = (
    PriorityContextBuilder(max_chars=1000)
    .add("用户目标", "需要中文文档", priority=100)
    .add("笔记", notes.render(), priority=80)
    .build()
)
print(context)
```

## 优先级建议

- 最高优先级：系统约束、用户当前请求、必须遵守的格式。
- 中等优先级：最近对话、工具结果、工作记忆、检索片段。
- 较低优先级：完整文件列表、历史摘要、背景资料。

## 扩展建议

生产环境应增加 token 计数、模型上下文窗口配置、引用来源、去重和压缩策略。
