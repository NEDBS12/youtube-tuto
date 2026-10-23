"""Answers a customer question. The handbook is cached."""
import sys
from pathlib import Path

import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
HANDBOOK = Path("handbook.md").read_text(encoding="utf-8")

# 1. Stable part first: the same in every request
system = [
    {"type": "text", "text": "Answer Maple Mugs customers."},
    {"type": "text", "text": HANDBOOK,
     "cache_control": {"type": "ephemeral"}},  # cache up to here
]

# 2. The part that changes goes after the breakpoint
reply = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=300,
    system=system,
    messages=[{"role": "user", "content": sys.argv[1]}],
)
print(reply.content[0].text)

# 3. Check the cache
u = reply.usage
print(f"written: {u.cache_creation_input_tokens}  "
      f"read: {u.cache_read_input_tokens}  new: {u.input_tokens}")
