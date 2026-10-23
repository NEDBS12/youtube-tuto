# MCP server and MCP client: cheat sheet

## The words

- **MCP (Model Context Protocol):** an open standard that connects AI apps to data and tools. Think of it as a USB-C port for AI apps.
- **MCP host:** the AI app, such as Claude Code, Claude Desktop or VS Code.
- **MCP client:** the connector inside the host. The host creates **one client per server**.
- **MCP server:** a program that offers things to the AI app:
  - **Tools:** actions the AI can call with arguments (`get_order`)
  - **Resources:** read-only data the app can load (`mugs://shipping-policy`)
  - **Prompts:** ready-made instruction templates
- **Transports:** `stdio` (a local server: the client starts it as a process on your machine) or **Streamable HTTP** (a remote server, usually with many clients).

## A server in Python (MCP Python SDK 2.x)

```python
from mcp.server import MCPServer

mcp = MCPServer("maple-mugs")

@mcp.tool()
def get_order(order_id: str) -> str:
    """Get the status of a Maple Mugs order."""   # becomes the tool description
    ...

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

The type hints and the docstring become the tool's name, description and input schema.

## A client in Python

```python
from mcp import Client, StdioServerParameters
from mcp.client.stdio import stdio_client

server = StdioServerParameters(command="python", args=["mugs_server.py"])
async with Client(stdio_client(server)) as client:
    tools = await client.list_tools()
    result = await client.call_tool("get_order", {"order_id": "1042"})
```

## Connect a server to Claude Code

```bash
claude mcp add --transport stdio maple-mugs -- python /full/path/to/mugs_server.py
claude mcp add --transport http notion https://mcp.notion.com/mcp   # a remote server
claude mcp list
claude mcp remove maple-mugs
```

Everything after `--` is the command that starts the server. Inside Claude Code, `/mcp` shows your servers.

## When to use what

| You want to… | Build |
|---|---|
| Give your data or tool to **many AI apps** (Claude Code, Claude Desktop, VS Code…) | an MCP **server** |
| Make **your own AI app or agent** that uses existing MCP servers | an MCP **client** |
| Use GitHub, Notion, Sentry… from Claude | nothing: **add an existing server** |
| One script, one app, one or two tools | no MCP: plain **tool use** in the Claude API is simpler |

## Rules to remember

- In a stdio server, **never `print()`**: stdout carries the protocol messages. Log with `logging` (it writes to stderr).
- Write clear docstrings: they're what the AI reads to decide when to call a tool.
- Test your server with a small client (or the MCP Inspector) before connecting it to an app.
- Only connect servers you trust. Servers that fetch outside content can expose you to prompt injection.

## Links

- MCP architecture: https://modelcontextprotocol.io/docs/learn/architecture
- Build an MCP server: https://modelcontextprotocol.io/docs/develop/build-server
- Build an MCP client: https://modelcontextprotocol.io/docs/develop/build-client
- MCP in Claude Code: https://code.claude.com/docs/en/mcp
