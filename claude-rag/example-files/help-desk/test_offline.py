"""Tests rag.py without an API key: retrieval is real, Claude is simulated.

Run: python -m pytest -q
"""
import os
import sys
from types import SimpleNamespace as NS

os.environ.setdefault("ANTHROPIC_API_KEY", "sk-demo-1234")  # fake key
import rag


class FakeMessages:
    """Checks the request like the API would, then answers like Claude."""

    def create(self, **kw):
        self.request = kw
        content = kw["messages"][0]["content"]
        results = [b for b in content if b["type"] == "search_result"]
        for r in results:
            assert {"source", "title", "content"} <= r.keys()
            assert r["content"] and r["content"][0]["text"]
        # citations are all-or-nothing across search results
        assert len({str(r.get("citations")) for r in results}) <= 1
        assert content[-1]["type"] == "text"  # the question comes last
        if not results:
            return NS(content=[NS(type="text", citations=None,
                                  text="Sorry, I don't know that.")])
        top = results[0]
        cite = NS(source=top["source"], title=top["title"],
                  cited_text=top["content"][0]["text"])
        return NS(content=[NS(type="text", citations=[cite],
                              text=f"From {top['title']}: ...")])


def fake_client(monkeypatch):
    fake = FakeMessages()
    monkeypatch.setattr(rag, "client", NS(messages=fake))
    return fake


def test_chunks():
    titles = [c["title"] for c in rag.load_chunks()]
    assert len(titles) == 8 and "Return window" in titles


def test_retrieves_the_right_sections():
    chunks = rag.load_chunks()
    found = rag.search("Can I return a mug after 40 days?", chunks)
    assert "Return window" in [c["title"] for c in found]
    found = rag.search("Is shipping free?", chunks)
    assert found[0]["title"] == "Shipping costs"


def test_answer_cites_its_source(monkeypatch, capsys):
    fake_client(monkeypatch)
    rag.ask("Is shipping free?")
    out = capsys.readouterr().out
    assert "[retrieved] shipping.md > Shipping costs" in out
    assert "Sources: shipping.md > Shipping costs" in out


def test_no_match_means_no_documents(monkeypatch, capsys):
    fake = fake_client(monkeypatch)
    rag.ask("Do you sell gift cards?")
    content = fake.request["messages"][0]["content"]
    assert content[0] == {"type": "text", "text": "No results found."}
    assert "Sources: none" in capsys.readouterr().out


def test_real_sdk_parses_citations(monkeypatch, capsys):
    """The real SDK sends the request and parses a real-shaped reply."""
    import json
    import anthropic
    try:  # newer SDKs use httpx2, older ones httpx
        import httpx2 as httpx
    except ImportError:
        import httpx

    sent = {}

    def handler(request):
        sent.update(json.loads(request.content))
        cite = {"type": "search_result_location", "source": "shipping.md",
                "title": "Shipping costs", "search_result_index": 0,
                "start_block_index": 0, "end_block_index": 1,
                "cited_text": "Shipping is free on orders over 40 euros."}
        return httpx.Response(200, json={
            "id": "msg_demo", "type": "message", "role": "assistant",
            "model": "claude-sonnet-5-5", "stop_reason": "end_turn",
            "stop_sequence": None,
            "usage": {"input_tokens": 10, "output_tokens": 10},
            "content": [{"type": "text", "citations": [cite],
                         "text": "Yes, on orders over 40 euros."}]})

    client = anthropic.Anthropic(
        api_key="sk-demo-1234",
        http_client=httpx.Client(transport=httpx.MockTransport(handler)))
    monkeypatch.setattr(rag, "client", client)
    rag.ask("Is shipping free?")
    assert sent["messages"][0]["content"][0]["type"] == "search_result"
    assert "Sources: shipping.md > Shipping costs" in capsys.readouterr().out
