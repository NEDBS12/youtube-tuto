"""Asks a question about the handbook, using its file ID."""
import sys
from pathlib import Path

import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
file_id = Path("file_id.txt").read_text().strip()

reply = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=300,
    messages=[{"role": "user", "content": [
        # The PDF by reference: nothing is uploaded again
        {"type": "document",
         "source": {"type": "file", "file_id": file_id}},
        {"type": "text", "text": sys.argv[1]},
    ]}],
)
print(reply.content[0].text)
