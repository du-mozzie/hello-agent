# 性能评估

模块：`helloagents.evaluation`

评估模块用于把智能体行为变成可度量的结果。它既支持简单问答评测，也支持函数调用和成对比较。

## 组件

- `TaskCase`：评测样例，包含输入、期望答案、指标名和元数据。
- `Evaluator`：运行评测样例并收集结果。
- `EvaluationReport`：评测报告，支持 Markdown 输出。
- `FunctionCallCase`：函数调用评测样例。
- `FunctionCallEvaluator`：检查 JSON 函数调用预测是否匹配。
- `PairwiseJudge`：确定性的成对比较评审器。
- `JudgeResult`：成对比较结果。

## 示例

```python
from helloagents import Evaluator, SimpleAgent, TaskCase

cases = [TaskCase("Hello", "deterministic", "contains")]
report = Evaluator().evaluate(SimpleAgent("demo"), cases)
print(report.to_markdown())
```

## 评估层次

- 单元层：测试工具和解析器。
- Agent 层：测试最终答案和执行步骤。
- 工具调用层：测试函数名和参数。
- 产品层：比较不同 Agent 的效果、成本和稳定性。

## 扩展建议

可以继续接入 BFCL、GAIA、自定义业务数据集、人类审核流、延迟/成本统计和错误分类。
