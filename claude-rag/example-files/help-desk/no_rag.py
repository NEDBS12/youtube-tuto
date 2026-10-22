import sys
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    system="You answer customer questions for Maple Mugs.",
    messages=[{"role": "user", "content": sys.argv[1]}],
)
print(response.content[0].text)
