"""Uploads the handbook PDF once and saves its file ID."""
from pathlib import Path

import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY

# 1. Upload once: file name, file, type
with open("handbook.pdf", "rb") as f:
    uploaded = client.files.upload(
        file=("handbook.pdf", f, "application/pdf"),
        expires_in_seconds=30 * 24 * 3600,  # deleted after 30 days
    )

# 2. Keep the ID: it's all you need from now on
Path("file_id.txt").write_text(uploaded.id)
print(f"Uploaded {uploaded.filename}: {uploaded.size_bytes:,} bytes")
print(f"file_id: {uploaded.id}")
