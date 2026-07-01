# HelloAgents

这是一个按 Datawhale「Hello-Agents」教程主线实现的模块化智能体项目。项目不是只放章节脚本，而是把教程里的核心概念整理成一个可安装、可测试、可复用的 Python 包。

默认实现只依赖 Python 标准库，可以离线运行；如果需要接入真实大模型，可以使用 OpenAI-compatible API 客户端。

## 快速开始

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .[dev]
python -m pytest -q
```

运行示例：

```powershell
helloagents react "What is (25 + 15) * 3 - 8?"
helloagents travel "Shanghai" "museums, coffee, river walk"
helloagents research "agent memory systems"
helloagents town
python examples/chapter16_capstone.py
```

## 中文文档

- 中文文档入口：[docs/README.md](docs/README.md)
- 中文模块文档：[docs/modules](docs/modules)
- 中文章节指南：[docs/chapters](docs/chapters)

## 模块总览

| 模块 | 说明 | 中文文档 |
| --- | --- | --- |
| `helloagents.schema` | 消息、步骤、工具调用、Agent 结果等共享数据结构 | [核心模型](docs/zh/modules/core.md) |
| `helloagents.fundamentals` | ELIZA、N-gram、BPE、简单 embedding、attention 演示 | [基础算法](docs/zh/modules/fundamentals.md) |
| `helloagents.llms` | 离线规则模型和 OpenAI-compatible LLM 客户端 | [模型接口](docs/zh/modules/llms.md) |
| `helloagents.tools` | 工具抽象、工具注册表、计算器、搜索、终端工具 | [工具系统](docs/zh/modules/tools.md) |
| `helloagents.agents` | Simple、ReAct、Plan-and-Solve、Reflection Agent | [智能体范式](docs/zh/modules/agents.md) |
| `helloagents.memory` | 工作记忆、会话记忆、向量检索、RAG | [记忆与检索](docs/zh/modules/memory.md) |
| `helloagents.context` | 笔记、工作区快照、优先级上下文构建 | [上下文工程](docs/zh/modules/context.md) |
| `helloagents.protocols` | MCP-like 工具、A2A 通信、ANP 注册、任务分发 | [通信协议](docs/zh/modules/protocols.md) |
| `helloagents.evaluation` | 任务评测、函数调用评测、成对评审 | [性能评估](docs/zh/modules/evaluation.md) |
| `helloagents.training` | SFT/偏好数据、奖励函数、LoRA/GRPO 配置计划 | [训练与 Agentic RL](docs/zh/modules/training.md) |
| `helloagents.lowcode` | Dify、Coze、FastGPT、n8n 风格流程描述与导出 | [低代码平台](docs/zh/modules/lowcode.md) |
| `helloagents.applications` | 旅行助手、深度研究、赛博小镇等综合应用 | [综合应用](docs/zh/modules/applications.md) |

## 章节覆盖

`examples/` 目录中提供了 16 个章节示例，对应教程完整主线：

| 章节 | 主题 | 示例 |
| --- | --- | --- |
| 第 1 章 | 初识智能体 | `examples/chapter01_first_agent.py` |
| 第 2 章 | 智能体发展史与 ELIZA | `examples/chapter02_eliza.py` |
| 第 3 章 | 大语言模型基础 | `examples/chapter03_llm_fundamentals.py` |
| 第 4 章 | 智能体经典范式 | `examples/chapter04_classic_paradigms.py` |
| 第 5 章 | 低代码平台搭建 | `examples/chapter05_lowcode.py` |
| 第 6 章 | 框架开发实践 | `examples/chapter06_framework_practice.py` |
| 第 7 章 | 构建自己的 Agent 框架 | `examples/chapter07_build_framework.py` |
| 第 8 章 | 记忆与检索 | `examples/chapter08_memory_rag.py` |
| 第 9 章 | 上下文工程 | `examples/chapter09_context_engineering.py` |
| 第 10 章 | 智能体通信协议 | `examples/chapter10_protocols.py` |
| 第 11 章 | Agentic RL | `examples/chapter11_agentic_rl.py` |
| 第 12 章 | 智能体性能评估 | `examples/chapter12_evaluation.py` |
| 第 13 章 | 智能旅行助手 | `examples/chapter13_trip_planner.py` |
| 第 14 章 | 自动化深度研究智能体 | `examples/chapter14_deep_research.py` |
| 第 15 章 | 构建赛博小镇 | `examples/chapter15_cyber_town.py` |
| 第 16 章 | 毕业设计 | `examples/chapter16_capstone.py` |

## 接入真实大模型

默认使用 `RuleBasedLLM`，方便测试和离线演示。接入 OpenAI-compatible 服务：

```powershell
pip install -e .[openai]
$env:OPENAI_API_KEY="..."
$env:OPENAI_BASE_URL="https://api.openai.com/v1"
$env:OPENAI_MODEL="gpt-4o-mini"
```

然后在代码中使用：

```python
from helloagents import OpenAICompatibleLLM, SimpleAgent

llm = OpenAICompatibleLLM()
agent = SimpleAgent("demo", llm=llm)
print(agent.run("解释 ReAct 智能体").answer)
```

## 项目结构

```text
helloagents/          # Python 包源码
examples/             # 章节示例与基础示例
tests/                # 单元测试
docs/modules/         # 英文模块文档
docs/chapters/        # 英文章节指南
docs/zh/modules/      # 中文模块文档
docs/zh/chapters/     # 中文章节指南
```
