# 工具系统

模块：`helloagents.tools`

工具系统负责把外部能力封装成可注册、可描述、可执行的函数。ReAct Agent、MCP-like 适配器和应用层都依赖该模块。

## 组件

- `Tool`：工具对象，包含名称、描述和执行函数。
- `ToolRegistry`：工具注册表，负责注册、查找、描述和执行工具。
- `calculator_tool()`：安全数学表达式计算工具，基于 AST 遍历，不使用 `eval`。
- `local_search_tool()`：内存文档搜索工具。
- `terminal_tool()`：带命令白名单的本地终端工具。

## 示例

```python
from helloagents.tools import ToolRegistry, calculator_tool

registry = ToolRegistry()
registry.register(calculator_tool())
print(registry.execute("calculator", "(25 + 15) * 3 - 8"))
```

## 工具设计建议

- 工具名要稳定、短小、可读。
- 描述要告诉模型什么时候使用该工具。
- 输入输出尽量结构化，复杂参数可以用 JSON 字符串承载。
- 对有副作用的工具增加白名单、权限和审计。

## 安全说明

`terminal_tool` 默认只允许少数命令。生产环境中应进一步限制工作目录、超时时间、网络访问和文件写入权限。
