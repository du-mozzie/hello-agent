import sys
from types import SimpleNamespace

from helloagents.llms import ALI_API_KEY, ALI_CHAT_BASE_URL, ALI_CHAT_MODEL, OpenAICompatibleLLM


def test_openai_compatible_llm_uses_configured_ali_defaults(monkeypatch):
    captured = {}

    class FakeOpenAI:
        def __init__(self, **kwargs):
            captured.update(kwargs)

    monkeypatch.setitem(sys.modules, "openai", SimpleNamespace(OpenAI=FakeOpenAI))

    llm = OpenAICompatibleLLM()

    assert llm.model == ALI_CHAT_MODEL
    assert captured["api_key"] == ALI_API_KEY
    assert captured["base_url"] == ALI_CHAT_BASE_URL
    assert captured["timeout"] == 60
