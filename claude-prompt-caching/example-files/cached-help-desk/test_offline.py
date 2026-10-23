"""Tests without an API key: the real SDK talks to a simulated API.

Run: python -m pytest -q
"""
import json
import runpy
import sys

import anthropic
import pytest

try:  # newer SDKs use httpx2, older ones httpx
    import httpx2 as httpx
except ImportError:
    import httpx

PREFIX = 1467  # tokens in the system prompt (simulated)


class FakeAPI:
    """Caches the system prompt like the API: write once, then read."""

    def __init__(self):
        self.cache, self.requests = set(), []

    def __call__(self, request):
        body = json.loads(request.content)
        self.requests.append(body)
        system = body["system"]
        marked = isinstance(system, list) and "cache_control" in system[-1]
        key = json.dumps(system)
        usage = {"input_tokens": PREFIX + 12, "output_tokens": 40,
                 "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0}
        if marked:
            usage["input_tokens"] = 12
            hit = key in self.cache
            usage["cache_read_input_tokens" if hit else "cache_creation_input_tokens"] = PREFIX
            self.cache.add(key)
        return httpx.Response(200, json={
            "id": "msg_demo", "type": "message", "role": "assistant",
            "model": body["model"], "stop_reason": "end_turn", "stop_sequence": None,
            "content": [{"type": "text", "text": "Yes, all our mugs are dishwasher safe."}],
            "usage": usage})


@pytest.fixture
def api(monkeypatch):
    fake = FakeAPI()
    real = anthropic.Anthropic
    monkeypatch.setattr(anthropic, "Anthropic", lambda: real(
        api_key="sk-demo-1234", http_client=httpx.Client(transport=httpx.MockTransport(fake))))
    return fake


def run(script, question, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", [script, question])
    runpy.run_path(script)
    return capsys.readouterr().out.splitlines()


def test_handbook_is_long_enough_to_cache():
    words = len(open("handbook.md", encoding="utf-8").read().split())
    assert words > 600  # about 1,500 tokens: over the 512-token minimum


def test_no_cache_sends_everything_every_time(api, monkeypatch, capsys):
    for q in ["Are your mugs dishwasher safe?", "Is shipping free?"]:
        out = run("no_cache.py", q, monkeypatch, capsys)
        assert out[-1] == f"input tokens: {PREFIX + 12}"


def test_first_call_writes_second_call_reads(api, monkeypatch, capsys):
    first = run("ask.py", "Are your mugs dishwasher safe?", monkeypatch, capsys)
    assert first[-1] == f"written: {PREFIX}  read: 0  new: 12"
    second = run("ask.py", "Is shipping free?", monkeypatch, capsys)
    assert second[-1] == f"written: 0  read: {PREFIX}  new: 12"


def test_breakpoint_is_on_the_handbook(api, monkeypatch, capsys):
    run("ask.py", "Is shipping free?", monkeypatch, capsys)
    system = api.requests[0]["system"]
    assert system[-1]["cache_control"] == {"type": "ephemeral"}
    assert system[-1]["text"].startswith("# Maple Mugs customer handbook")
    assert "cache_control" not in api.requests[0]["messages"][0]  # the question is not cached


def test_cost(capsys):
    runpy.run_path("cost.py")
    out = capsys.readouterr().out
    assert "No cache: $3.00" in out and "Cached:   $0.15" in out and "Saved:    95%" in out
