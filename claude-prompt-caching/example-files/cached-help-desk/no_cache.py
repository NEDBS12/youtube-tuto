"""Answers a question. The handbook is sent every time."""
import sys
from pathlib import Path

import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
HANDBOOK = Path("handbook.md").read_text(encoding="utf-8")

reply = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=300,
    system="Answer Maple Mugs customers.\n\n" + HANDBOOK,
    messages=[{"role": "user", "content": sys.argv[1]}],
)
print(reply.content[0].text)
print(f"input tokens: {reply.usage.input_tokens}")
