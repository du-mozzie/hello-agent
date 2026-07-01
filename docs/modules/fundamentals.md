# Fundamentals Module

Module: `helloagents.fundamentals`

This module covers the first part of the tutorial: rule-based agents and language-model basics.

## Components

- `ElizaBot`: pattern matching, template response, and pronoun swap.
- `NGramLanguageModel`: add-k smoothed n-gram probability and generation.
- `BPETokenizer`: byte-pair encoding merge training and tokenization.
- `SimpleEmbeddingModel`: bag-of-words embedding and cosine similarity.
- `scaled_dot_product_attention`: dependency-free attention calculation.

## Example

```python
from helloagents import BPETokenizer, ElizaBot, NGramLanguageModel

print(ElizaBot().respond("I need better tools"))

model = NGramLanguageModel(n=2).fit("datawhale agent learns datawhale agent works")
print(model.sentence_probability("datawhale agent learns"))

tokenizer = BPETokenizer().fit(["hug", "pug", "pun", "bun"], num_merges=4)
print(tokenizer.tokenize("hug"))
```

## Why It Exists

These implementations are not meant to compete with production tokenizers or transformer libraries. They make the concepts inspectable before moving to LLM APIs and full agent frameworks.
