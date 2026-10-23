# Prompt caching: pay once for the part that repeats

Files from the Zero Cost AI video **"Prompt Caching Explained Simply: Cheaper, Faster Claude (Python)"**.

A help desk bot for Maple Mugs (a made-up shop) sends the same store handbook with every customer question. With one `cache_control` breakpoint, the handbook is written to Claude's cache once and then read for a fraction of the price. On Claude Sonnet 5.5 prices, that's 95% cheaper for that part of the prompt.

## Use it in your project

| File | What it does |
|---|---|
| [`cached-help-desk/handbook.md`](example-files/cached-help-desk/handbook.md) | The store handbook: the long part that never changes (about 1,500 tokens) |
| [`cached-help-desk/no_cache.py`](example-files/cached-help-desk/no_cache.py) | The bot without caching: the whole handbook is billed on every question |
| [`cached-help-desk/ask.py`](example-files/cached-help-desk/ask.py) | The bot with caching: the handbook block has `cache_control`, and the script prints written, read and new tokens |
| [`cached-help-desk/cost.py`](example-files/cached-help-desk/cost.py) | The savings for 1,000 questions a day, in plain Python |
| [`cached-help-desk/test_offline.py`](example-files/cached-help-desk/test_offline.py) | Runs both bots with the real SDK against a simulated API: no API key, no cost |
| [`prompt-caching-cheatsheet.md`](example-files/prompt-caching-cheatsheet.md) | The two ways to turn caching on, the usage fields, prices, and what breaks the cache |

1. Do the math, no key needed: in `cached-help-desk/`, run `python cost.py`.
2. Run the tests, no key needed: `pip install anthropic pytest`, then `python -m pytest -q` (5 passed).
3. With an API key: set `ANTHROPIC_API_KEY`, then run `python ask.py "Are your mugs dishwasher safe?"` and, within 5 minutes, `python ask.py "Is shipping free?"`. The first run writes the cache, the second reads it.

- Your token numbers will differ a little from the video (the runs on screen are a recreation).
- On Mac or Linux, use `python3` if `python` isn't found.
- To use your own content, replace `handbook.md`. It must be over the minimum size for your model (512 tokens on Claude Sonnet 5.5), or nothing is cached and you get no error.
- Keep anything that changes (the question, today's date, user data) after the block with `cache_control`.

## Files in this folder

- `claude-prompt-caching.mp4`: the video
- `claude-prompt-caching.srt`: subtitles
- `script.json`, `make_script.py`: the video script (made with the claude-expert-video skill)
- `example-files/`: the help desk bot and the cheat sheet (no secrets: the test uses a fake key, `sk-demo-1234`)

## Learn more

- [Prompt caching (Claude docs)](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [Claude pricing](https://platform.claude.com/docs/en/about-claude/pricing)
