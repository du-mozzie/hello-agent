"""Evaluation helpers for agent behavior."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Callable

from .agents import BaseAgent


@dataclass(slots=True)
class TaskCase:
    input: str
    expected: str
    metric: str = "contains"
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass(slots=True)
class EvaluationReport:
    total: int
    passed: int
    details: list[dict[str, object]]

    @property
    def score(self) -> float:
        return self.passed / self.total if self.total else 0.0

    def to_markdown(self) -> str:
        lines = [f"# Evaluation Report", "", f"Score: {self.passed}/{self.total} ({self.score:.1%})", ""]
        for index, detail in enumerate(self.details, start=1):
            status = "PASS" if detail["passed"] else "FAIL"
            lines.append(f"{index}. {status} - {detail['input']}")
        return "\n".join(lines)


Metric = Callable[[str, str], bool]


class Evaluator:
    """Run task cases against an agent."""

    def __init__(self) -> None:
        self.metrics: dict[str, Metric] = {
            "exact": lambda actual, expected: actual.strip() == expected.strip(),
            "contains": lambda actual, expected: expected.lower() in actual.lower(),
            "non_empty": lambda actual, expected: bool(actual.strip()),
        }

    def register_metric(self, name: str, metric: Metric) -> None:
        self.metrics[name] = metric

    def evaluate(self, agent: BaseAgent, cases: list[TaskCase]) -> EvaluationReport:
        details: list[dict[str, object]] = []
        passed = 0
        for case in cases:
            result = agent.run(case.input)
            metric = self.metrics[case.metric]
            ok = metric(result.answer, case.expected)
            passed += int(ok)
            details.append(
                {
                    "input": case.input,
                    "expected": case.expected,
                    "actual": result.answer,
                    "metric": case.metric,
                    "passed": ok,
                }
            )
        return EvaluationReport(total=len(cases), passed=passed, details=details)


@dataclass(slots=True)
class FunctionCallCase:
    """BFCL-style function-call evaluation case."""

    input: str
    expected_name: str
    expected_arguments: dict[str, object]


class FunctionCallEvaluator:
    """Evaluate JSON function-call predictions."""

    def evaluate_prediction(self, prediction: str, case: FunctionCallCase) -> dict[str, object]:
        try:
            payload = json.loads(prediction)
        except json.JSONDecodeError:
            return {"passed": False, "reason": "prediction is not valid JSON"}
        name_ok = payload.get("name") == case.expected_name
        args_ok = payload.get("arguments") == case.expected_arguments
        return {"passed": name_ok and args_ok, "name_ok": name_ok, "arguments_ok": args_ok}


@dataclass(slots=True)
class JudgeResult:
    winner: str
    reason: str
    score_a: float
    score_b: float


class PairwiseJudge:
    """Deterministic pairwise judge based on keyword coverage and brevity."""

    def judge(self, prompt: str, answer_a: str, answer_b: str, keywords: list[str] | None = None) -> JudgeResult:
        keywords = keywords or [word for word in prompt.lower().split() if len(word) > 3]
        score_a = self._score(answer_a, keywords)
        score_b = self._score(answer_b, keywords)
        winner = "A" if score_a >= score_b else "B"
        reason = "higher keyword coverage with shorter or equal answer" if winner == "A" else "higher keyword coverage"
        return JudgeResult(winner=winner, reason=reason, score_a=score_a, score_b=score_b)

    @staticmethod
    def _score(answer: str, keywords: list[str]) -> float:
        lowered = answer.lower()
        coverage = sum(1 for keyword in keywords if keyword in lowered)
        length_penalty = min(len(answer) / 1000, 1.0)
        return coverage - 0.1 * length_penalty
