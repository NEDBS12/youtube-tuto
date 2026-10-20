import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[{"role": "user",
               "content": "Where is my order 1042?"}],
)
print("stop_reason:", response.stop_reason)
print(response.content[0].text)
