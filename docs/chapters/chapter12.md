# 第 12 章：智能体性能评估

## 学习目标

理解如何用任务样例、函数调用检查和成对评审来度量智能体效果。

## 对应实现

- `TaskCase`
- `Evaluator`
- `EvaluationReport`
- `FunctionCallCase`
- `FunctionCallEvaluator`
- `PairwiseJudge`

## 运行示例

```powershell
python examples/chapter12_evaluation.py
```

## 代码要点

评估不应只看最终文本，还应检查工具调用、结构化输出、步骤轨迹和稳定性。

## 扩展方向

接入 BFCL、GAIA、业务数据集、人类审核和成本/延迟统计。
