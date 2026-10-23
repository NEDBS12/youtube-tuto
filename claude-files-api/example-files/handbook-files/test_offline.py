"""Tests without an API key: the real SDK talks to a simulated API.

Run: python -m pytest -q
"""
import json
import runpy
import shutil
import sys
from pathlib import Path

import anthropic
import pytest

try:  # newer SDKs use httpx2, older ones httpx
    import httpx2 as httpx
except ImportError:
    import httpx

HERE = Path(__file__).parent


class FakeAPI:
    """Stores uploaded files and answers messages like the Files API."""

    def __init__(self):
        self.files, self.messages = {}, []

    def meta(self, fid):
        return {"id": fid, "type": "file", "created_at": "2026-10-23T09:00:00Z",
                "downloadable": False, "expires_at": None, **self.files[fid]}

    def __call__(self, req):
        path, method = req.url.path, req.method
        if method == "POST" and path == "/v1/files":
            body = req.content
            assert b'filename="handbook.pdf"' in body and b"application/pdf" in body
            assert b'name="expires_in_seconds"' in body
            fid = f"file_demo{len(self.files) + 1}"
            self.files[fid] = {"filename": "handbook.pdf", "mime_type": "application/pdf",
                               "size_bytes": (HERE / "handbook.pdf").stat().st_size}
            return httpx.Response(200, json=self.meta(fid))
        if method == "GET" and path == "/v1/files":
            return httpx.Response(200, json={"data": [self.meta(f) for f in self.files],
                                             "next_page": None})
        if method == "DELETE" and path.startswith("/v1/files/"):
            fid = path.rsplit("/", 1)[1]
            self.files.pop(fid)
            return httpx.Response(200, json={"id": fid, "type": "file_deleted"})
        if method == "POST" and path == "/v1/messages":
            body = json.loads(req.content)
            self.messages.append(body)
            doc = body["messages"][0]["content"][0]
            src = doc["source"]
            if src["type"] == "file":
                assert src["file_id"] in self.files, "404: file not found"
            return httpx.Response(200, json={
                "id": "msg_demo", "type": "message", "role": "assistant",
                "model": body["model"], "stop_reason": "end_turn", "stop_sequence": None,
                "content": [{"type": "text", "text": "Yes, all our mugs are dishwasher safe."}],
                "usage": {"input_tokens": 3500, "output_tokens": 12}})
        return httpx.Response(404, json={"type": "error", "error": {"type": "not_found_error"}})


@pytest.fixture
def api(monkeypatch, tmp_path):
    for f in ["handbook.pdf", "no_files.py", "upload.py", "ask.py", "files.py"]:
        shutil.copy(HERE / f, tmp_path)
    monkeypatch.chdir(tmp_path)
    fake = FakeAPI()
    real = anthropic.Anthropic
    monkeypatch.setattr(anthropic, "Anthropic", lambda: real(
        api_key="sk-demo-1234", http_client=httpx.Client(transport=httpx.MockTransport(fake))))
    return fake


def run(monkeypatch, capsys, *argv):
    monkeypatch.setattr(sys, "argv", list(argv))
    runpy.run_path(argv[0])
    return capsys.readouterr().out.splitlines()


def test_without_files_api_the_pdf_is_sent_every_time(api, monkeypatch, capsys):
    out = run(monkeypatch, capsys, "no_files.py", "Are your mugs dishwasher safe?")
    assert out[0] == "Sending 120,004 characters of PDF data..."
    assert api.messages[0]["messages"][0]["content"][0]["source"]["type"] == "base64"


def test_upload_saves_the_file_id(api, monkeypatch, capsys):
    out = run(monkeypatch, capsys, "upload.py")
    assert out == ["Uploaded handbook.pdf: 90,001 bytes", "file_id: file_demo1"]
    assert Path("file_id.txt").read_text() == "file_demo1"


def test_ask_sends_only_the_file_id(api, monkeypatch, capsys):
    run(monkeypatch, capsys, "upload.py")
    for q in ["Are your mugs dishwasher safe?", "Is shipping free?"]:
        run(monkeypatch, capsys, "ask.py", q)
    assert len(api.files) == 1  # uploaded once, used twice
    for body in api.messages:
        doc, text = body["messages"][0]["content"]
        assert doc == {"type": "document", "source": {"type": "file", "file_id": "file_demo1"}}
        assert text["type"] == "text"


def test_list_and_delete(api, monkeypatch, capsys):
    run(monkeypatch, capsys, "upload.py")
    assert run(monkeypatch, capsys, "files.py") == ["file_demo1  handbook.pdf  90,001 bytes"]
    assert run(monkeypatch, capsys, "files.py", "delete", "file_demo1") == ["Deleted file_demo1"]
    assert run(monkeypatch, capsys, "files.py") == []


def test_pdf_is_real():
    data = (HERE / "handbook.pdf").read_bytes()
    assert data.startswith(b"%PDF") and len(data) > 10_000
