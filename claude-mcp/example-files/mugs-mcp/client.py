"""MCP client: starts the server, lists its tools, calls one."""
import asyncio
import sys

from mcp import Client, StdioServerParameters
from mcp.client.stdio import stdio_client

# 1. How to start the server: a command, like in a terminal
server = StdioServerParameters(command=sys.executable,
                               args=["mugs_server.py"])


async def main(order_id):
    # 2. Connect: launches the server, agrees on the protocol
    async with Client(stdio_client(server)) as client:
        tools = await client.list_tools()
        print("Tools:", [t.name for t in tools.tools])

        # 3. Call a tool by name, with arguments
        result = await client.call_tool("get_order",
                                        {"order_id": order_id})
        print(result.content[0].text)


asyncio.run(main(sys.argv[1]))
