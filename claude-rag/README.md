# RAG with Claude: answer from your own documents, with sources

Files from the Zero Cost AI video **"RAG Explained with Claude: Answer From Your Own Docs, With Sources"**.

A small help desk for a demo online shop, Maple Mugs. Claude has never seen the shop's policies, so `rag.py` does retrieval-augmented generation: it splits the policy docs into chunks, finds the best matches with simple keyword search, sends them to Claude as `search_result` blocks with citations on, and prints the answer with its sources. When nothing matches, Claude says it doesn't know instead of guessing.

## Use it in your project

| File | What it does |
|---|---|
| [`help-desk/docs/`](example-files/help-desk/docs) | The demo knowledge base: `returns.md`, `shipping.md`, `care.md` (one chunk per `##` section) |
| [`help-desk/no_rag.py`](example-files/help-desk/no_rag.py) | The problem: Claude without the docs can't answer |
| [`help-desk/rag.py`](example-files/help-desk/rag.py) | The RAG pipeline: chunk, retrieve, augment (`search_result` blocks), generate and cite |
| [`help-desk/test_offline.py`](example-files/help-desk/test_offline.py) | Tests retrieval for real and simulates Claude: no API key, no cost |
| [`rag-cheatsheet.md`](example-files/rag-cheatsheet.md) | The 3 steps, when you don't need RAG, the `search_result` format, retrieval tips |

1. Install the SDK: `pip install anthropic` (these files were tested with 1.15.0).
2. Try it without an API key: `pip install pytest`, then in `help-desk/` run `python -m pytest -q` (5 passed).
3. With a key: set `ANTHROPIC_API_KEY`, then run:
   - `python no_rag.py "Can I return a mug after 40 days?"`
   - `python rag.py "Can I return a mug after 40 days?"`
   - `python rag.py "Do you sell gift cards?"` (not in the docs: Claude should say it doesn't know)

- Claude's wording will differ from the video; the retrieved chunks are the same.
- On Mac or Linux, use `python3` if `python` isn't found.
- Change the model in each script (`claude-sonnet-5-5`) to any current Claude model.
- To use your own documents, put Markdown files with `##` sections in `docs/` and change the shop name in the system prompt.
- The keyword search is deliberately simple. For larger document sets, use better scoring (like BM25) and embeddings; the rest of the pipeline stays the same.
- If all your documents fit in one prompt (under ~200,000 tokens), you may not need RAG at all: send them all, with prompt caching.

## Files in this folder

- `claude-rag.mp4`: the video
- `claude-rag.srt`: subtitles
- `script.json`, `make_script.py`: the video script (made with the claude-expert-video skill)
- `example-files/`: the help desk and the cheat sheet (no secrets: the test uses the fake key `sk-demo-1234` with a simulated API)

## Learn more

- [Search results (RAG with citations)](https://platform.claude.com/docs/en/build-with-claude/search-results)
- [Citations](https://platform.claude.com/docs/en/build-with-claude/citations)
- [Embeddings](https://platform.claude.com/docs/en/build-with-claude/embeddings)
- [Introducing Contextual Retrieval (Anthropic)](https://www.anthropic.com/news/contextual-retrieval)
