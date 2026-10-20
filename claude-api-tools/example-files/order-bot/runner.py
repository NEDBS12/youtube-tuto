import anthropic
from anthropic import beta_tool
import shop_tools

client = anthropic.Anthropic()


@beta_tool
def get_order_status(order_id: str) -> str:
    """Look up a my-shop order by its number.

    Returns the status, carrier and delivery date.
    Use it whenever a customer asks where their order is.

    Args:
        order_id: Order number, e.g. 1042
    """
    return shop_tools.get_order_status(order_id)


runner = client.beta.messages.tool_runner(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    max_iterations=5,
    tools=[get_order_status],
    messages=[
        {"role": "user",
         "content": "Where are my orders 1042 and 9999?"},
    ],
)
for message in runner:
    print("stop_reason:", message.stop_reason)

print("".join(b.text for b in message.content
              if b.type == "text"))
