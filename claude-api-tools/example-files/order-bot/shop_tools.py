import json
import pathlib

HERE = pathlib.Path(__file__).parent
ORDERS = json.loads((HERE / "orders.json").read_text())


def get_order_status(order_id: str) -> str:
    """Return the order as JSON, or raise a helpful error."""
    order = ORDERS.get(order_id)
    if order is None:
        raise ValueError(
            f"Order {order_id} not found. Ask the customer to "
            "check the number in their confirmation email.")
    return json.dumps(order)
