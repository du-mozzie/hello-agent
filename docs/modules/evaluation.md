# Evaluation Module

Module: `helloagents.evaluation`

Evaluation makes agent behavior measurable.

## Components

- `TaskCase`: input, expected answer, metric name, and metadata.
- `Evaluator`: runs task cases against an agent.
- `EvaluationReport`: score, details, and Markdown export.
- `FunctionCallCase`: BFCL-style function-call expectation.
- `FunctionCallEvaluator`: checks JSON function-call predictions.
- `PairwiseJudge`: deterministic win-rate style comparison.
- `JudgeResult`: winner, reason, and scores.

## Built-in Metrics

- `exact`
- `contains`
- `non_empty`

## Example

```python
from helloagents import Evaluator, SimpleAgent, TaskCase

cases = [TaskCase("Say hello", "deterministic", "contains")]
report = Evaluator().evaluate(SimpleAgent("demo"), cases)
print(report.to_markdown())
```

Register stricter metrics for tool calls, structured outputs, latency, cost, or domain-specific correctness.

## Evaluation Levels

- Unit level: verify tools and output parsers.
- Agent level: verify task cases and final answers.
- Tool-use level: verify function-call names and arguments.
- Product level: compare two agents with `PairwiseJudge` or a human review workflow.
