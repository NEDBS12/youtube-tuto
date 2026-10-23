"""MCP server: gives any AI app access to Maple Mugs orders."""
import json
from pathlib import Path

from mcp.server import MCPServer

mcp = MCPServer("maple-mugs")
ORDERS = Path(__file__).with_name("orders.json")


# 1. A tool: the AI can call it with arguments
@mcp.tool()
def get_order(order_id: str) -> str:
    """Get the status of a Maple Mugs order.

    Args:
        order_id: The order number, for example 1042
    """
    o = json.loads(ORDERS.read_text()).get(order_id)
    if o is None:
        return f"No order {order_id} found."
    return (f"Order {order_id} for {o['customer']}: {o['item']}, "
            f"{o['status']}, arriving {o['eta']}.")


# 2. A resource: read-only data the app can load
@mcp.resource("mugs://shipping-policy")
def shipping_policy() -> str:
    """The shop's shipping rules."""
    return "Free US shipping over $60. Otherwise $6. Ships Mon-Fri."


# 3. Run over stdio: the client starts this file
if __name__ == "__main__":
    mcp.run(transport="stdio")
