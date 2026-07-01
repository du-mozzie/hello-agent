# 基础算法

模块：`helloagents.fundamentals`

该模块覆盖教程前几章中的基础概念，用最小实现展示智能体和大语言模型出现前后的关键技术。

## 组件

- `ElizaBot`：ELIZA 风格规则聊天机器人，展示早期智能体的模式匹配和模板回复。
- `NGramLanguageModel`：带 add-k 平滑的 N-gram 语言模型。
- `BPETokenizer`：BPE 分词训练和分词过程。
- `SimpleEmbeddingModel`：基于词袋的 embedding 和余弦相似度。
- `scaled_dot_product_attention`：无第三方依赖的缩放点积注意力演示。

## 示例

```python
from helloagents import BPETokenizer, ElizaBot, NGramLanguageModel

bot = ElizaBot()
print(bot.respond("I need better tools"))

model = NGramLanguageModel(n=2).fit("datawhale agent learns datawhale agent works")
print(model.sentence_probability("datawhale agent learns"))

tokenizer = BPETokenizer().fit(["hug", "pug", "pun", "bun"], num_merges=4)
print(tokenizer.tokenize("hug"))
```

## 适用场景

这些实现用于教学和调试概念，不替代生产级 tokenizer、embedding 模型或深度学习框架。它们的价值在于让概率、分词、向量相似度和 attention 的中间过程可见。
