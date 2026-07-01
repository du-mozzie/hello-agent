from helloagents import BPETokenizer, ElizaBot, NGramLanguageModel, SimpleEmbeddingModel, scaled_dot_product_attention


def test_eliza_matches_need_pattern():
    response = ElizaBot(seed=1).respond("I need better tools")
    assert "better tools" in response


def test_ngram_sentence_probability_is_positive():
    model = NGramLanguageModel(n=2).fit("datawhale agent learns datawhale agent works")
    assert model.sentence_probability("datawhale agent learns") > 0


def test_bpe_tokenizer_learns_merges():
    tokenizer = BPETokenizer().fit(["hug", "pug", "pun", "bun"], num_merges=2)
    assert tokenizer.merges
    assert tokenizer.tokenize("hug")


def test_embedding_similarity_detects_overlap():
    model = SimpleEmbeddingModel()
    assert model.similarity("agent memory", "agent tools") > 0


def test_attention_weights_sum_to_one():
    trace = scaled_dot_product_attention([1, 0], [[1, 0], [0, 1]], [[10, 0], [0, 10]])
    assert round(sum(trace.weights), 6) == 1.0
