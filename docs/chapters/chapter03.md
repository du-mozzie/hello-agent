# 第 3 章：大语言模型基础

## 学习目标

理解语言模型背后的基础概念：N-gram 概率、BPE 分词、向量相似度和 attention。

## 对应实现

- `NGramLanguageModel`
- `BPETokenizer`
- `SimpleEmbeddingModel`
- `scaled_dot_product_attention`
- `RuleBasedLLM`
- `OpenAICompatibleLLM`

## 运行示例

```powershell
python examples/chapter03_llm_fundamentals.py
```

## 代码要点

这些实现都保持依赖最小，便于观察中间结果。真实 LLM 系统会更复杂，但核心概念可以从这些小实现中看清。

## 扩展方向

接入真实 tokenizer、embedding API 或本地 transformer 框架，对比教学实现和生产实现的差异。
