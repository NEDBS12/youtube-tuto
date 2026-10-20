# Claude Code Subagents: Your AI Helpers

Files from the Zero Cost AI video **"Claude Code Subagents Explained: Build a Test Runner Step by Step"**.

The video builds a `test-runner` subagent: it runs your tests in its own context window and sends back only the failures, so 68 lines of test output never land in your main conversation. It can't edit files, and it runs on the faster, cheaper Haiku model.

## Use the subagent in your project

Copy this file from [`example-files/my-shop`](example-files/my-shop) into your project:

| File | What it does |
|---|---|
| [`.claude/agents/test-runner.md`](example-files/my-shop/.claude/agents/test-runner.md) | The subagent: name, description, allowed tools (no Edit/Write), model, and its instructions |

1. Save it as `.claude/agents/test-runner.md` in your project (or `~/.claude/agents/` for all your projects).
2. If the `agents` folder is new, start a new Claude Code session so it's picked up.
3. Ask: `Run the tests`. Claude delegates to `test-runner` and gets back a short summary.
4. To force it: `@agent-test-runner check everything still passes`.

- The subagent runs `python -m pytest -q`. Change step 1 of its instructions for your test command (for example `npm test`).
- `model: haiku` keeps it cheap; use `model: inherit` to use the same model as your conversation.

## Try the demo project

[`example-files/my-shop`](example-files/my-shop) is a tiny cart with 30 tests and one bug: an order of exactly 100 gets no discount.

```bash
pip install pytest
cd example-files/my-shop
python -m pytest -q        # 1 failed, 29 passed
```

Then start `claude` in `my-shop` and ask it to run the tests: the `test-runner` subagent finds the bug in `cart.py`.

## Files in this folder

- `claude-code-subagents.mp4`: the video
- `claude-code-subagents.srt`: subtitles
- `script.json`, `make_script.py`: the video script (made with the claude-expert-video skill)
- `example-files/my-shop/`: the demo project and the subagent

## Learn more

- [Create custom subagents](https://code.claude.com/docs/en/sub-agents)
