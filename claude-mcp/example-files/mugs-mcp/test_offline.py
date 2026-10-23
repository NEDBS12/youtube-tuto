"""Tests the real server with the real client. No API key needed.

Run: python -m pytest -q
"""
import asyncio
import subprocess
import sys
from pathlib import Path

from mcp import Client, StdioServerParameters
from mcp.client.stdio import stdio_client

HERE = Path(__file__).parent
SERVER = StdioServerParameters(command=sys.executable, args=[str(HERE / "mugs_server.py")])


def run_client(order_id):
    out = subprocess.run([sys.executable, "client.py", order_id], cwd=HERE,
                         capture_output=True, text=True, timeout=60)
    assert out.returncode == 0, out.stderr
    return out.stdout.splitlines()


def test_client_lists_tools_and_gets_an_order():
    assert run_client("1042") == [
        "Tools: ['get_order']",
        "Order 1042 for Priya: Teapot (Slate), shipped, arriving Oct 25.",
    ]


def test_unknown_order():
    assert run_client("9999")[-1] == "No order 9999 found."


def test_tool_schema_comes_from_type_hints_and_docstring():
    async def go():
        async with Client(stdio_client(SERVER)) as client:
            tool = (await client.list_tools()).tools[0]
            return tool.description, tool.input_schema
    description, schema = asyncio.run(go())
    assert description.startswith("Get the status of a Maple Mugs order.")
    assert schema["properties"]["order_id"]["type"] == "string"
    assert schema["required"] == ["order_id"]


def test_resource_is_readable():
    async def go():
        async with Client(stdio_client(SERVER)) as client:
            uris = [str(r.uri) for r in (await client.list_resources()).resources]
            text = (await client.read_resource("mugs://shipping-policy")).contents[0].text
            return uris, text
    uris, text = asyncio.run(go())
    assert uris == ["mugs://shipping-policy"]
    assert "Free US shipping over $60" in text


def test_server_never_prints_to_stdout():
    # On stdio, stdout carries the protocol: a print() would break it.
    assert "print(" not in (HERE / "mugs_server.py").read_text()
