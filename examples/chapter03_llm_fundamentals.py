from helloagents import BPETokenizer, NGramLanguageModel, SimpleEmbeddingModel, scaled_dot_product_attention


if __name__ == "__main__":
    corpus = "datawhale agent learns datawhale agent works"
    ngram = NGramLanguageModel(n=2).fit(corpus)
    print("P(datawhale agent learns) =", round(ngram.sentence_probability("datawhale agent learns"), 4))

    bpe = BPETokenizer().fit(["hug", "pug", "pun", "bun"], num_merges=4)
    print("BPE merges:", bpe.merges)
    print("BPE tokenize('hug'):", bpe.tokenize("hug"))

    embeddings = SimpleEmbeddingModel()
    print("Similarity:", round(embeddings.similarity("agent memory retrieval", "agent retrieval tool"), 3))

    trace = scaled_dot_product_attention([1, 0], [[1, 0], [0, 1]], [[10, 0], [0, 10]])
    print("Attention weights:", [round(item, 3) for item in trace.weights])
