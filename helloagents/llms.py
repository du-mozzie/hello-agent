"""LLM clients.

The default RuleBasedLLM keeps examples deterministic. OpenAICompatibleLLM is
loaded lazily so the base project has no hard network dependency.
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from typing import Iterable, Sequence

from .schema import Message

ALI_GATEWAY_ROOT = "https://ai-gw.huice.com/hjy-fi"
ALI_BASE_URL = f"{ALI_GATEWAY_ROOT.rstrip('/')}/compatible-mode/v1"
ALI_EMBEDDING_MODEL = "qwen3-vl-embedding"
ALI_MULTIMODAL_URL = (
    f"{ALI_GATEWAY_ROOT.rstrip('/')}/api/v1/services/embeddings/"
    "multimodal-embedding/multimodal-embedding"
)
ALI_API_KEY = "sk-837syyvh2wvjrypzfaph"
ALI_CHAT_BASE_URL = "https://ai-gw.huice.com/hjy-fi/compatible-mode/v1"
ALI_CHAT_MODEL = "qwen3.6-plus"


class BaseLLM(ABC):
    """Minimal LLM interface used by all agents."""

    @abstractmethod
    def complete(self, messages: Sequence[Message], **kwargs: object) -> str:
        """Return the assistant text for a list of messages."""

    def invoke(self, prompt: str | Sequence[Message], **kwargs: object) -> str:
        if isinstance(prompt, str):
            messages = [Message("user", prompt)]
        else:
            messages = list(prompt)
        return self.complete(messages, **kwargs)


class RuleBasedLLM(BaseLLM):
    """Deterministic LLM substitute for tests and offline demos."""

    def complete(self, messages: Sequence[Message], **kwargs: object) -> str:
        text = "\n".join(message.content for message in messages)
        lowered = text.lower()
        expression = _extract_math_expression(text)
        if "thought:" in lowered and "action:" in lowered:
            if "observation:" in lowered:
                observation = text.rsplit("Observation:", 1)[-1].strip().splitlines()[0]
                return f"Thought: I have enough information.\nAction: Finish[{observation}]"
            if expression:
                return f"Thought: I should calculate the expression.\nAction: calculator[{expression}]"
            return "Thought: I can answer directly.\nAction: Finish[I can help with that request.]"
        if expression:
            return f"The result is {_safe_eval_for_llm(expression)}."
        if "reflect" in lowered or "critique" in lowered:
            return "The answer is clear, grounded, and can be improved by citing tool observations."
        if "plan" in lowered:
            return "1. Understand the task\n2. Gather needed facts\n3. Produce the final answer"
        return "This is a deterministic offline response from RuleBasedLLM."


class OpenAICompatibleLLM(BaseLLM):
    """OpenAI-compatible chat completion client.

    Defaults to the configured Alibaba-compatible gateway.
    """

    def __init__(
        self,
        model: str | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
        temperature: float = 0.2,
        timeout: float = 60,
    ) -> None:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("Install the openai extra: pip install -e .[openai]") from exc
<<<<<<< HEAD
        self.model = model or ALI_CHAT_MODEL
        self.temperature = temperature
        self._client = OpenAI(
            api_key=api_key or ALI_API_KEY,
            base_url=base_url or ALI_CHAT_BASE_URL,
=======
        self.model = 'qwen3.6-plus'
        self.temperature = temperature
        self._client = OpenAI(
            api_key= 'sk-837syyvh2wvjrypzfaph',
            base_url= 'https://ai-gw.huice.com/hjy-fi/compatible-mode/v1',
>>>>>>> 1de80c0b5f561a73cf9bb6e1ace8bf668b2057be
            timeout=timeout,
        )

    def complete(self, messages: Sequence[Message], **kwargs: object) -> str:
        response = self._client.chat.completions.create(
            model=str(kwargs.get("model", self.model)),
            messages=[message.to_dict() for message in messages],
            temperature=float(kwargs.get("temperature", self.temperature)),
        )
        return response.choices[0].message.content or ""


def _extract_math_expression(text: str) -> str | None:
    candidates = re.findall(r"[-+*/().\d\s]{3,}", text)
    for candidate in sorted(candidates, key=len, reverse=True):
        stripped = candidate.strip()
        if any(operator in stripped for operator in "+-*/") and re.search(r"\d", stripped):
            return stripped
    return None


def _safe_eval_for_llm(expression: str) -> object:
    from .tools import safe_calculate

    try:
        return safe_calculate(expression)
    except Exception:
        return "unavailable"
