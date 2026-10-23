# Files API: cheat sheet

## The idea

Upload a file **once**, get back a `file_id`, and use that ID in as many Messages requests as you want, instead of sending the whole file every time. The Files API is generally available: no beta header needed.

## The four operations (Python SDK)

```python
import anthropic
client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY

# Upload (expires_in_seconds is optional: 3,600 to 7,776,000 = 1 hour to 90 days)
with open("handbook.pdf", "rb") as f:
    up = client.files.upload(file=("handbook.pdf", f, "application/pdf"),
                             expires_in_seconds=30 * 24 * 3600)
print(up.id)  # file_...

# Use it in a message
{"type": "document", "source": {"type": "file", "file_id": up.id}}

# List, details, delete
for f in client.files.list(): print(f.id, f.filename)
client.files.retrieve_metadata(up.id)
client.files.delete(up.id)
```

## Which content block?

| File | Block |
|---|---|
| PDF, plain text | `document` |
| JPEG, PNG, GIF, WebP | `image` |
| Datasets and other files for the code execution tool | `container_upload` |

- `.docx` and `.xlsx` aren't supported as `document`: convert them to text first.
- `.csv` and `.md` can be uploaded with an explicit `text/plain` type, or simply pasted as text.

## Limits and prices

- Up to 500 MB per file, 1 TB per organization. About 500 file requests per minute.
- Uploading, listing, getting details, downloading and deleting are **free**.
- The file's content is still billed as **input tokens** every time a message uses it. To pay less for a file you reuse, add prompt caching.

## Rules to remember

- **Files belong to the whole workspace.** Any API key in that workspace can use any file. Never accept a `file_id` from your users: keep the user → file mapping in your own app.
- **Files can't be edited or renamed.** Upload a new one, then delete the old one.
- **Files you upload can't be downloaded.** Only files created by skills or the code execution tool can.
- Files stay until you delete them, or until `expires_at` if you set an expiration.

## Links

- Files API (Claude docs): https://platform.claude.com/docs/en/build-with-claude/files
- PDF support: https://platform.claude.com/docs/en/build-with-claude/pdf-support
