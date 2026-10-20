import anthropic
from shop_tools import get_order_status

client = anthropic.Anthropic()

tools = [{
    "name": "get_order_status",
    "description": (
        "Look up a my-shop order by its number. "
        "Returns the status, carrier and delivery date. "
        "Use it whenever a customer asks where their order is."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "order_id": {
                "type": "string",
                "description": "Order number, e.g. 1042",
            },
        },
        "required": ["order_id"],
    },
}]
messages = [{"role": "user",
             "content": "Where is my order 1042?"}]

while True:
    response = client.messages.create(
        model="claude-sonnet-5-5", max_tokens=1024,
        tools=tools, messages=messages,
    )
    print("stop_reason:", response.stop_reason)
    if response.stop_reason != "tool_use":
        break
    messages.append({"role": "assistant",
                     "content": response.content})
    results = []
    for block in response.content:
        if block.type == "tool_use":
            print(f"  tool call: {block.name}({block.input})")
            output = get_order_status(**block.input)
            results.append({"type": "tool_result",
                            "tool_use_id": block.id,
                            "content": output})
    messages.append({"role": "user", "content": results})

print("".join(b.text for b in response.content
              if b.type == "text"))
