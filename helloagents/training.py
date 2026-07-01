"""Training-oriented helpers for Agentic RL examples.

This module does not train large models. It provides deterministic data and
reward utilities that mirror the tutorial workflow before plugging into SFT,
LoRA, GRPO, or external training frameworks.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable


@dataclass(slots=True)
class TrainingExample:
    prompt: str
    response: str
    metadata: dict[str, object] | None = None


@dataclass(slots=True)
class PreferenceExample:
    prompt: str
    chosen: str
    rejected: str
    metadata: dict[str, object] | None = None


class RewardFunction:
    """Composable text reward helpers."""

    def __init__(self, func: Callable[[str, str], float]) -> None:
        self.func = func

    def __call__(self, response: str, reference: str = "") -> float:
        return self.func(response, reference)

    @staticmethod
    def format_reward(required_patterns: list[str]) -> "RewardFunction":
        def score(response: str, reference: str = "") -> float:
            if not required_patterns:
                return 1.0
            hits = sum(1 for pattern in required_patterns if re.search(pattern, response, re.I))
            return hits / len(required_patterns)

        return RewardFunction(score)

    @staticmethod
    def exact_reward() -> "RewardFunction":
        return RewardFunction(lambda response, reference: 1.0 if response.strip() == reference.strip() else 0.0)


def save_jsonl(path: str | Path, examples: list[TrainingExample | PreferenceExample]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as handle:
        for example in examples:
            handle.write(json.dumps(asdict(example), ensure_ascii=False) + "\n")


def load_jsonl(path: str | Path) -> list[dict[str, object]]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


@dataclass(slots=True)
class LoRAConfig:
    rank: int = 8
    alpha: int = 16
    dropout: float = 0.05
    target_modules: list[str] = field(default_factory=lambda: ["q_proj", "v_proj"])


@dataclass(slots=True)
class GRPOConfig:
    group_size: int = 4
    kl_penalty: float = 0.02
    max_prompt_length: int = 2048
    max_completion_length: int = 512


@dataclass(slots=True)
class TrainingPipelinePlan:
    dataset_path: str
    output_dir: str
    lora: LoRAConfig = field(default_factory=LoRAConfig)
    grpo: GRPOConfig = field(default_factory=GRPOConfig)

    def commands(self) -> list[str]:
        return [
            f"validate-dataset --input {self.dataset_path}",
            f"sft-train --dataset {self.dataset_path} --output {self.output_dir} --lora-rank {self.lora.rank}",
            f"grpo-train --checkpoint {self.output_dir} --group-size {self.grpo.group_size}",
            f"evaluate-agent --checkpoint {self.output_dir}",
        ]


class DatasetBuilder:
    """Collect SFT and preference examples before exporting JSONL."""

    def __init__(self) -> None:
        self.sft: list[TrainingExample] = []
        self.preferences: list[PreferenceExample] = []

    def add_sft(self, prompt: str, response: str, **metadata: object) -> None:
        self.sft.append(TrainingExample(prompt=prompt, response=response, metadata=metadata or None))

    def add_preference(self, prompt: str, chosen: str, rejected: str, **metadata: object) -> None:
        self.preferences.append(
            PreferenceExample(prompt=prompt, chosen=chosen, rejected=rejected, metadata=metadata or None)
        )

    def export(self, directory: str | Path) -> dict[str, Path]:
        root = Path(directory)
        sft_path = root / "sft.jsonl"
        preference_path = root / "preferences.jsonl"
        save_jsonl(sft_path, self.sft)
        save_jsonl(preference_path, self.preferences)
        return {"sft": sft_path, "preferences": preference_path}
