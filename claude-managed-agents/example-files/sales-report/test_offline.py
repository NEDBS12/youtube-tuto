"""Run setup_agent.py and run_report.py against a simulated Managed Agents API.

No API key, no cost: the real SDK code runs, and fake_api() below answers its HTTP
calls, playing the part of Anthropic's servers and the agent. Run: python -m pytest -q
"""
import json
import os
import runpy
import time

import anthropic
import pytest

try:  # the SDK's HTTP library: httpx2 in SDK v1.x, httpx in older versions
    import httpx2 as httpx
except ImportError:
    import httpx

CALLS = []
EVENTS = [  # what a real session streams while the agent works (shortened)
    {"type": "session.status_running"},
    {"type": "agent.tool_use", "name": "bash", "input": {"command": "python3 analyze.py"}},
    {"type": "agent.tool_result"},
    {"type": "agent.tool_use", "name": "write", "input": {"file_path": "/mnt/session/outputs/report.md"}},
    {"type": "agent.message", "content": [{"type": "text", "text": "Done: report.md and weekly.png are saved."}]},
    {"type": "session.status_idle", "stop_reason": {"type": "end_turn"}},
]


def fake_api(request):
    path, method = request.url.path, request.method
    CALLS.append((method, path, request.headers.get("anthropic-beta")))
    body = json.loads(request.content) if request.headers.get("content-type") == "application/json" else {}
    if (method, path) == ("POST", "/v1/agents"):
        assert body["tools"] == [{"type": "agent_toolset_20260401"}]
        return httpx.Response(200, json={"id": "agent_demo", "type": "agent", "version": 1, **body})
    if (method, path) == ("POST", "/v1/environments"):
        assert body["config"]["networking"]["type"] == "limited"
        return httpx.Response(200, json={"id": "env_demo", "type": "environment", **body})
    if (method, path) == ("POST", "/v1/files"):
        assert b'filename="orders.csv"' in request.content
        return httpx.Response(200, json={"id": "file_orders", "type": "file", "filename": "orders.csv"})
    if (method, path) == ("POST", "/v1/sessions"):
        assert body["agent"] == "agent_demo" and body["resources"][0]["file_id"] == "file_orders"
        return httpx.Response(200, json={"id": "sesn_demo", "type": "session", "status": "idle"})
    if (method, path) == ("GET", "/v1/sessions/sesn_demo/events/stream"):
        sse = "".join(f"event: {e['type']}\ndata: {json.dumps({'id': f'evt_{i}', **e})}\n\n" for i, e in enumerate(EVENTS))
        return httpx.Response(200, headers={"content-type": "text/event-stream"}, content=sse.encode())
    if (method, path) == ("POST", "/v1/sessions/sesn_demo/events"):
        assert body["events"][0]["type"] == "user.message"
        return httpx.Response(200, json={"data": []})
    if (method, path) == ("GET", "/v1/files"):
        assert request.url.params.get("scope_id") == "sesn_demo"
        files = [{"id": i, "type": "file", "filename": n} for i, n in
                 [("file_orders", "orders.csv"), ("file_report", "report.md"), ("file_chart", "weekly.png")]]
        return httpx.Response(200, json={"data": files, "has_more": False, "first_id": None, "last_id": None})
    if method == "GET" and path.startswith("/v1/files/") and path.endswith("/content"):
        return httpx.Response(200, content=b"# October sales report\n")
    return httpx.Response(404, json={"type": "error", "error": {"type": "not_found_error", "message": path}})


@pytest.fixture(autouse=True)
def simulated_api(monkeypatch, tmp_path):
    CALLS.clear()
    real = anthropic.Anthropic
    monkeypatch.setattr(anthropic, "Anthropic", lambda: real(
        api_key="sk-demo-1234", max_retries=0, http_client=httpx.Client(transport=httpx.MockTransport(fake_api))))
    monkeypatch.setattr(time, "sleep", lambda s: None)
    here = os.path.dirname(os.path.abspath(__file__))
    for name in ("setup_agent.py", "run_report.py", "orders.csv"):
        (tmp_path / name).write_bytes(open(os.path.join(here, name), "rb").read())
    monkeypatch.chdir(tmp_path)


def test_setup_then_run(capsys, tmp_path):
    runpy.run_path("setup_agent.py")
    assert json.loads((tmp_path / "ids.json").read_text()) == {"agent": "agent_demo", "environment": "env_demo"}
    runpy.run_path("run_report.py")
    out = capsys.readouterr().out
    assert "[tool] bash" in out and "[tool] write" in out
    assert "Idle: end_turn" in out
    assert "Downloaded report.md" in out and "Downloaded weekly.png" in out and "Downloaded orders.csv" not in out
    assert (tmp_path / "report.md").exists()
    # every Managed Agents call carries the beta header (the SDK adds it)
    assert all(beta == "managed-agents-2026-04-01" for m, p, beta in CALLS
               if p.startswith(("/v1/agents", "/v1/environments", "/v1/sessions")))
