# 模型接口

模块：`helloagents.llms`

该模块提供智能体调用模型的统一接口。项目默认使用离线的 `RuleBasedLLM`，因此测试和示例不依赖网络。

## 组件

- `BaseLLM`：抽象基类，定义 `complete(messages)` 和便捷方法 `invoke(prompt)`。
- `RuleBasedLLM`：确定性的离线规则模型，用于测试、演示和示例。
- `OpenAICompatibleLLM`：OpenAI-compatible Chat Completions 客户端。

## 离线示例

```python
from helloagents import RuleBasedLLM

llm = RuleBasedLLM()
print(llm.invoke("What is 1 + 2?"))
```

## 接入真实模型

```powershell
pip install -e .[openai]
```

```python
from helloagents import OpenAICompatibleLLM

llm = OpenAICompatibleLLM()
print(llm.invoke("用一段话解释 ReAct 智能体。"))
```

## 扩展建议

如果要接入其他供应商，只需要继承 `BaseLLM` 并实现 `complete()`。Agent 层不需要知道底层供应商是 OpenAI、ModelScope、本地模型还是企业内部网关。
