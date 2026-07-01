"""Foundational algorithms used in the early Hello-Agents chapters."""

from __future__ import annotations

import math
import random
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Iterable


class ElizaBot:
    """Rule-based ELIZA-style chatbot.

    It demonstrates the pre-LLM agent era: pattern matching, template filling,
    and simple pronoun transformation.
    """

    DEFAULT_RULES: dict[str, list[str]] = {
        r"I need (.*)": [
            "Why do you need {0}?",
            "Would it really help you to get {0}?",
            "Are you sure you need {0}?",
        ],
        r"Why don't you (.*)\??": [
            "Do you really think I don't {0}?",
            "Perhaps eventually I will {0}.",
            "Do you really want me to {0}?",
        ],
        r"Why can't I (.*)\??": [
            "Do you think you should be able to {0}?",
            "If you could {0}, what would you do?",
            "What would it mean if you could {0}?",
        ],
        r"I am (.*)": [
            "How long have you been {0}?",
            "How do you feel about being {0}?",
            "What makes you say you are {0}?",
        ],
        r".* mother .*": [
            "Tell me more about your mother.",
            "How do you feel about your mother?",
        ],
        r".* father .*": [
            "Tell me more about your father.",
            "What has your father taught you?",
        ],
        r".*": [
            "Please tell me more.",
            "Can you elaborate on that?",
            "Let's change focus a bit. Tell me about your family.",
        ],
    }

    PRONOUN_SWAP = {
        "i": "you",
        "you": "I",
        "me": "you",
        "my": "your",
        "your": "my",
        "am": "are",
        "are": "am",
        "was": "were",
        "were": "was",
        "mine": "yours",
        "yours": "mine",
    }

    def __init__(self, rules: dict[str, list[str]] | None = None, seed: int = 7) -> None:
        self.rules = rules or self.DEFAULT_RULES
        self.random = random.Random(seed)

    def respond(self, user_input: str) -> str:
        for pattern, templates in self.rules.items():
            match = re.search(pattern, user_input, re.I)
            if match:
                captured = match.group(1) if match.groups() else ""
                swapped = self.swap_pronouns(captured)
                return self.random.choice(templates).format(swapped)
        return self.random.choice(self.rules[r".*"])

    def swap_pronouns(self, phrase: str) -> str:
        return " ".join(self.PRONOUN_SWAP.get(word.lower(), word) for word in phrase.split())


class NGramLanguageModel:
    """Small add-k smoothed n-gram language model."""

    def __init__(self, n: int = 2, smoothing: float = 1.0) -> None:
        if n < 1:
            raise ValueError("n must be >= 1.")
        self.n = n
        self.smoothing = smoothing
        self.ngram_counts: Counter[tuple[str, ...]] = Counter()
        self.context_counts: Counter[tuple[str, ...]] = Counter()
        self.vocabulary: set[str] = set()

    def fit(self, corpus: str | Iterable[str]) -> "NGramLanguageModel":
        tokens = _tokenize(corpus if isinstance(corpus, str) else " ".join(corpus))
        padded = ["<s>"] * (self.n - 1) + tokens + ["</s>"]
        self.vocabulary.update(tokens)
        self.vocabulary.add("</s>")
        for index in range(len(padded) - self.n + 1):
            ngram = tuple(padded[index : index + self.n])
            context = ngram[:-1]
            self.ngram_counts[ngram] += 1
            self.context_counts[context] += 1
        return self

    def probability(self, token: str, context: Iterable[str] = ()) -> float:
        context_tuple = tuple(context)[-(self.n - 1) :] if self.n > 1 else tuple()
        if len(context_tuple) < self.n - 1:
            context_tuple = ("<s>",) * (self.n - 1 - len(context_tuple)) + context_tuple
        vocab_size = max(len(self.vocabulary), 1)
        count = self.ngram_counts[context_tuple + (token,)]
        context_count = self.context_counts[context_tuple]
        return (count + self.smoothing) / (context_count + self.smoothing * vocab_size)

    def sentence_probability(self, sentence: str) -> float:
        tokens = _tokenize(sentence) + ["</s>"]
        context = ["<s>"] * (self.n - 1)
        probability = 1.0
        for token in tokens:
            probability *= self.probability(token, context)
            context.append(token)
        return probability

    def generate(self, max_tokens: int = 12, seed: int = 7) -> str:
        rng = random.Random(seed)
        context = ["<s>"] * (self.n - 1)
        output: list[str] = []
        for _ in range(max_tokens):
            choices = sorted(self.vocabulary)
            weights = [self.probability(token, context) for token in choices]
            token = rng.choices(choices, weights=weights, k=1)[0]
            if token == "</s>":
                break
            output.append(token)
            context.append(token)
        return " ".join(output)


class BPETokenizer:
    """Minimal byte-pair encoding tokenizer for teaching."""

    def __init__(self, end_token: str = "</w>") -> None:
        self.end_token = end_token
        self.merges: list[tuple[str, str]] = []

    def fit(self, words: Iterable[str], num_merges: int = 10) -> "BPETokenizer":
        vocab = Counter(" ".join([*word, self.end_token]) for word in words)
        self.merges.clear()
        for _ in range(num_merges):
            pairs = self._pair_stats(vocab)
            if not pairs:
                break
            best = max(pairs, key=pairs.get)
            self.merges.append(best)
            vocab = self._merge_vocab(vocab, best)
        return self

    def tokenize(self, word: str) -> list[str]:
        tokens = [*word, self.end_token]
        for left, right in self.merges:
            merged: list[str] = []
            index = 0
            while index < len(tokens):
                if index < len(tokens) - 1 and tokens[index] == left and tokens[index + 1] == right:
                    merged.append(left + right)
                    index += 2
                else:
                    merged.append(tokens[index])
                    index += 1
            tokens = merged
        return [token for token in tokens if token != self.end_token]

    @staticmethod
    def _pair_stats(vocab: Counter[str]) -> Counter[tuple[str, str]]:
        pairs: Counter[tuple[str, str]] = Counter()
        for word, freq in vocab.items():
            symbols = word.split()
            for index in range(len(symbols) - 1):
                pairs[(symbols[index], symbols[index + 1])] += freq
        return pairs

    @staticmethod
    def _merge_vocab(vocab: Counter[str], pair: tuple[str, str]) -> Counter[str]:
        pattern = re.compile(r"(?<!\S)" + re.escape(" ".join(pair)) + r"(?!\S)")
        merged = Counter()
        for word, freq in vocab.items():
            merged[pattern.sub("".join(pair), word)] = freq
        return merged


class SimpleEmbeddingModel:
    """Bag-of-words embedding with cosine similarity."""

    def embed(self, text: str) -> Counter[str]:
        return Counter(_tokenize(text))

    def similarity(self, left: str, right: str) -> float:
        left_vec = self.embed(left)
        right_vec = self.embed(right)
        numerator = sum(left_vec[token] * right_vec[token] for token in left_vec.keys() & right_vec.keys())
        left_norm = math.sqrt(sum(value * value for value in left_vec.values()))
        right_norm = math.sqrt(sum(value * value for value in right_vec.values()))
        return numerator / (left_norm * right_norm) if left_norm and right_norm else 0.0


@dataclass(slots=True)
class TransformerBlockTrace:
    """Human-readable trace of a tiny attention calculation."""

    query: list[float]
    keys: list[list[float]]
    values: list[list[float]]
    scores: list[float] = field(default_factory=list)
    weights: list[float] = field(default_factory=list)
    output: list[float] = field(default_factory=list)


def scaled_dot_product_attention(
    query: list[float],
    keys: list[list[float]],
    values: list[list[float]],
) -> TransformerBlockTrace:
    """Compute a tiny attention step without numerical dependencies."""

    if len(keys) != len(values):
        raise ValueError("keys and values must have the same length.")
    scale = math.sqrt(max(len(query), 1))
    scores = [sum(q * k for q, k in zip(query, key)) / scale for key in keys]
    exp_scores = [math.exp(score - max(scores)) for score in scores]
    total = sum(exp_scores)
    weights = [score / total for score in exp_scores]
    output = [0.0 for _ in values[0]]
    for weight, value in zip(weights, values):
        for index, item in enumerate(value):
            output[index] += weight * item
    return TransformerBlockTrace(query=query, keys=keys, values=values, scores=scores, weights=weights, output=output)


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9_]+", text.lower())
