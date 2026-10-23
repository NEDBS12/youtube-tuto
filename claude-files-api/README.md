# Files API: upload a PDF once, use it in every request

Files from the Zero Cost AI video **"Claude Files API Explained Simply: Upload Once (Python)"**.

The Maple Mugs help desk (a made-up shop) answers questions about a 3-page handbook PDF. Without the Files API, every question sends the whole PDF again (120,004 characters of base64). With it, the PDF is uploaded once and every question sends a short `file_id`. The scripts also list and delete your files.

## Use it in your project

| File | What it does |
|---|---|
| [`handbook-files/handbook.pdf`](example-files/handbook-files/handbook.pdf) | The store handbook, 3 pages |
| [`handbook-files/no_files.py`](example-files/handbook-files/no_files.py) | The usual way: sends the whole PDF as base64 with every question |
| [`handbook-files/upload.py`](example-files/handbook-files/upload.py) | Uploads the PDF once (deleted automatically after 30 days) and saves its ID to `file_id.txt` |
| [`handbook-files/ask.py`](example-files/handbook-files/ask.py) | Asks a question using a `document` block with the `file_id` |
| [`handbook-files/files.py`](example-files/handbook-files/files.py) | Lists your files, or deletes one: `python files.py delete FILE_ID` |
| [`handbook-files/test_offline.py`](example-files/handbook-files/test_offline.py) | Runs every script with the real SDK against a simulated API: no API key, no cost |
| [`files-api-cheatsheet.md`](example-files/files-api-cheatsheet.md) | Upload, use, list, delete, block types, limits and rules |

1. Run the tests, no key needed: in `handbook-files/`, run `pip install anthropic pytest`, then `python -m pytest -q` (5 passed).
2. With an API key: set `ANTHROPIC_API_KEY`, then run `python upload.py` once.
3. Ask as many questions as you like: `python ask.py "Are your mugs dishwasher safe?"`
4. Clean up: `python files.py`, then `python files.py delete <your file id>`.

- Your file ID will differ from the video (the runs on screen are a recreation).
- On Mac or Linux, use `python3` if `python` isn't found.
- Files belong to your whole API workspace: in a real app, never accept a `file_id` from your users.
- The PDF's content still counts as input tokens on each question. To pay less for a file you reuse, add prompt caching (see the `claude-prompt-caching` folder).

## Files in this folder

- `claude-files-api.mp4`: the video
- `claude-files-api.srt`: subtitles
- `script.json`, `make_script.py`: the video script (made with the claude-expert-video skill)
- `example-files/`: the help desk scripts, the handbook PDF and the cheat sheet (no secrets: the test uses a fake key, `sk-demo-1234`)

## Learn more

- [Files API (Claude docs)](https://platform.claude.com/docs/en/build-with-claude/files)
- [PDF support (Claude docs)](https://platform.claude.com/docs/en/build-with-claude/pdf-support)
