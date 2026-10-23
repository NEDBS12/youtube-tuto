"""Asks about the handbook by sending the whole PDF every time."""
import base64
import sys
from pathlib import Path

import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
data = Path("handbook.pdf").read_bytes()
pdf = base64.standard_b64encode(data).decode()
print(f"Sending {len(pdf):,} characters of PDF data...")

reply = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=300,
    messages=[{"role": "user", "content": [
        {"type": "document", "source": {
            "type": "base64", "media_type": "application/pdf",
            "data": pdf}},
        {"type": "text", "text": sys.argv[1]},
    ]}],
)
print(reply.content[0].text)
