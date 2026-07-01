# Chapter 03 - LLM Fundamentals

## Goal

Make tokenization, probability, embeddings, and attention visible in small dependency-free examples.

## Implemented Code

- `NGramLanguageModel`
- `BPETokenizer`
- `SimpleEmbeddingModel`
- `scaled_dot_product_attention`
- `RuleBasedLLM`
- `OpenAICompatibleLLM`

## Run

```powershell
python examples/chapter03_llm_fundamentals.py
```

## Extension

Replace `SimpleEmbeddingModel` with a real embedding provider and replace the toy attention function with a deep learning framework when training or serving models.
