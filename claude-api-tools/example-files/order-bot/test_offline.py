"""Run the three scripts against a simulated Messages API (no API key, no cost).

The real SDK code runs; only the HTTP calls are answered by fake_api() below,
which plays Claude's side of the tool use lifecycle. Run: python -m pytest -q
"""
import json
import re
import runpy

import anthropic
import pytest

try:  # the SDK's HTTP library: httpx2 in SDK v1.x, httpx in older versions
    import httpx2 as httpx
except ImportError:
    import httpx

REQUESTS = []


def message(content, stop_reason):
    return {"id": "msg_test", "type": "message", "role": "assistant", "model": "claude-sonnet-5-5",
            "content": content, "stop_reason": stop_reason, "stop_sequence": None,
            "usage": {"input_tokens": 10, "output_tokens": 10}}


def fake_api(request):
    body = json.loads(request.content)
    REQUESTS.append(body)
    last = body["messages"][-1]["content"]
    if isinstance(last, list) and last and last[0].get("type") == "tool_result":
        # Claude reads the tool results and answers: end of the lifecycle
        text = "; ".join(("error: " if r.get("is_error") else "") + json.dumps(r["content"]) for r in last)
        return httpx.Response(200, json=message([{"type": "text", "text": f"Answer from: {text}"}], "end_turn"))
    if body.get("tools"):
        # Claude decides to call the tool once per order number in the question
        calls = [{"type": "tool_use", "id": f"toolu_{n}", "name": "get_order_status", "input": {"order_id": n}}
                 for n in re.findall(r"\d{4}", last)]
        return httpx.Response(200, json=message(calls, "tool_use"))
    return httpx.Response(200, json=message([{"type": "text", "text": "I don't have access to your orders."}], "end_turn"))


@pytest.fixture(autouse=True)
def simulated_api(monkeypatch):
    REQUESTS.clear()
    real = anthropic.Anthropic
    monkeypatch.setattr(anthropic, "Anthropic", lambda: real(
        api_key="sk-demo-1234", http_client=httpx.Client(transport=httpx.MockTransport(fake_api))))


def test_no_tools(capsys):
    runpy.run_path("no_tools.py")
    assert "stop_reason: end_turn" in capsys.readouterr().out


def test_manual_loop(capsys):
    runpy.run_path("manual_loop.py")
    out = capsys.readouterr().out
    assert out.index("stop_reason: tool_use") < out.index("stop_reason: end_turn")
    assert "shipped" in out and len(REQUESTS) == 2
    second = REQUESTS[1]["messages"]
    assert second[1]["role"] == "assistant" and second[2]["content"][0]["tool_use_id"] == "toolu_1042"


def test_runner(capsys):
    runpy.run_path("runner.py")
    out = capsys.readouterr().out
    assert out.count("stop_reason:") == 2 and "stop_reason: end_turn" in out
    tool = REQUESTS[0]["tools"][0]
    assert tool["name"] == "get_order_status" and "order_id" in tool["input_schema"]["properties"]
    results = REQUESTS[1]["messages"][-1]["content"]
    assert [r.get("is_error", False) for r in results] == [False, True]
    assert "not found" in json.dumps(results[1]["content"])
