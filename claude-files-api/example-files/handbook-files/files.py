"""Lists your files. To delete one: python files.py delete FILE_ID"""
import sys

import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY

if len(sys.argv) == 3 and sys.argv[1] == "delete":
    client.files.delete(sys.argv[2])
    print(f"Deleted {sys.argv[2]}")
else:
    for f in client.files.list():
        print(f"{f.id}  {f.filename}  {f.size_bytes:,} bytes")
