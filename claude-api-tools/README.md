# Claude Tools and the Tool Runner: The Tool Use Lifecycle

Files from the Zero Cost AI video **"Claude API Tool Use Explained: Tool Runner and stop_reason"**.

A small order status assistant for an online shop. Claude can't see your orders on its own, so we give it a `get_order_status` tool: Claude asks for the order (`stop_reason: "tool_use"`), our code reads `orders.json` and sends back a `tool_result`, and Claude answers (`stop_reason: "end_turn"`). It's built twice: once with a manual loop, once with the SDK's Tool Runner.

## Use it in your project

| File | What it does |
|---|---|
| [`order-bot/orders.json`](example-files/order-bot/orders.json) | Three demo orders (1042, 1043, 1044) |
| [`order-bot/shop_tools.py`](example-files/order-bot/shop_tools.py) | The real function: looks up an order, or raises a helpful error |
| [`order-bot/no_tools.py`](example-files/order-bot/no_tools.py) | The problem: Claude without tools can't answer |
| [`order-bot/manual_loop.py`](example-files/order-bot/manual_loop.py) | The tool use lifecycle by hand: a `while` loop on `stop_reason` |
| [`order-bot/runner.py`](example-files/order-bot/runner.py) | The same with `@beta_tool` and `client.beta.messages.tool_runner` (errors become `is_error: true`) |
| [`order-bot/test_offline.py`](example-files/order-bot/test_offline.py) | Runs all three scripts against a simulated API: no API key, no cost |
| [`tool-lifecycle-cheatsheet.md`](example-files/tool-lifecycle-cheatsheet.md) | The lifecycle, every `stop_reason`, manual loop vs Tool Runner |

1. Install the SDK: `pip install anthropic` (the Tool Runner needs a recent version; these files were tested with 1.15.0).
2. Try it without an API key: `pip install pytest`, then in `order-bot/` run `python -m pytest -q` (3 passed).
3. With a key: set `ANTHROPIC_API_KEY`, then run `python no_tools.py`, `python manual_loop.py` and `python runner.py`.

- Claude's wording will differ from the video; the stop reasons follow the same pattern.
- On Mac or Linux, use `python3` if `python` isn't found.
- Change the model in each script (`claude-sonnet-5-5`) to any current Claude model.
- To use your own data, replace `shop_tools.get_order_status` and update the tool's description: it's what Claude reads to decide when to call it.

## Files in this folder

- `claude-api-tools.mp4`: the video
- `claude-api-tools.srt`: subtitles
- `script.json`, `make_script.py`: the video script (made with the claude-expert-video skill)
- `example-files/`: the order bot and the cheat sheet (no secrets: the test uses the fake key `sk-demo-1234` with a simulated API)

## Learn more

- [How tool use works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works)
- [Tool Runner (SDK)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner)
- [Stop reasons](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons)
- [Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls)
