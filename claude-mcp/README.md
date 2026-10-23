# MCP server and MCP client: connect Claude to your own data

Files from the Zero Cost AI video **"MCP Server vs MCP Client Explained Simply (Python Example)"**.

A tiny MCP server gives AI apps a `get_order` tool for Maple Mugs orders (a made-up shop), plus a read-only shipping-policy resource. A small Python MCP client starts the server, lists its tools and calls one. Then the same server is connected to Claude Code with one command. Everything here runs **without an API key**.

## Use it in your project

| File | What it does |
|---|---|
| [`mugs-mcp/mugs_server.py`](example-files/mugs-mcp/mugs_server.py) | The MCP server: a `get_order` tool and a `mugs://shipping-policy` resource, over stdio |
| [`mugs-mcp/orders.json`](example-files/mugs-mcp/orders.json) | Three sample orders (stands in for a real database) |
| [`mugs-mcp/client.py`](example-files/mugs-mcp/client.py) | The MCP client: starts the server, lists its tools, calls `get_order` |
| [`mugs-mcp/test_offline.py`](example-files/mugs-mcp/test_offline.py) | Runs the real server with the real client: tool, schema, resource, errors |
| [`mcp-cheatsheet.md`](example-files/mcp-cheatsheet.md) | Host, client, server, tools, resources, transports, and when to build what |

1. Install the MCP Python SDK (Python 3.10 or newer): `pip install "mcp>=2"`
2. In `mugs-mcp/`, run the client: `python client.py 1042`
   ```
   Tools: ['get_order']
   Order 1042 for Priya: Teapot (Slate), shipped, arriving Oct 25.
   ```
3. Run the tests: `pip install pytest`, then `python -m pytest -q` (5 passed).
4. Connect it to Claude Code: `claude mcp add --transport stdio maple-mugs -- python /full/path/to/mugs_server.py`, start `claude`, and ask "Where is order 1042?". Claude Code asks for permission the first time it uses the tool.

- The client and test output above are real. The Claude Code part of the video is a recreation: the exact wording on your screen will differ.
- Use the full path to `mugs_server.py` in `claude mcp add`, so it works from any folder. On Mac or Linux, use `python3` if `python` isn't found.
- To use your own data, change what `get_order` reads (a database, an API…). Keep the docstring clear: it's what Claude reads to decide when to call the tool.
- Never use `print()` in a stdio server: stdout carries the protocol. Use `logging` instead.
- To remove it later: `claude mcp remove maple-mugs`.

## Files in this folder

- `claude-mcp.mp4`: the video
- `claude-mcp.srt`: subtitles
- `script.json`, `make_script.py`: the video script (made with the claude-expert-video skill)
- `example-files/`: the server, the client, sample data, tests and the cheat sheet (no secrets, no API key needed)

## Learn more

- [MCP architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)
- [Build an MCP server](https://modelcontextprotocol.io/docs/develop/build-server)
- [Build an MCP client](https://modelcontextprotocol.io/docs/develop/build-client)
- [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp)
