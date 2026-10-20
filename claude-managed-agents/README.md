# Claude Managed Agents vs Your Own Agent

Files from the Zero Cost AI video **"Claude Managed Agents vs Your Own Agent: Which One to Build?"**.

With your own agent, you write the loop and run every tool (like the order bot in the previous video). With Claude Managed Agents (beta), Anthropic runs the loop, the built-in tools and a cloud sandbox. This example uses a Managed Agent to turn a month of shop orders into a sales report and a chart: Claude writes and runs Python in the sandbox, and the script downloads the files it saved.

## Use it in your project

| File | What it does |
|---|---|
| [`sales-report/orders.csv`](example-files/sales-report/orders.csv) | 24 demo orders from October 2026 |
| [`sales-report/setup_agent.py`](example-files/sales-report/setup_agent.py) | Run once: creates the agent (model, system prompt, `agent_toolset_20260401`) and a cloud environment with `limited` networking, saves both IDs to `ids.json` |
| [`sales-report/run_report.py`](example-files/sales-report/run_report.py) | Run per task: uploads the CSV, starts a session with it mounted, sends the task, streams the events, downloads the outputs |
| [`sales-report/test_offline.py`](example-files/sales-report/test_offline.py) | Runs both scripts against a simulated API: no API key, no cost |
| [`managed-vs-own-agent-cheatsheet.md`](example-files/managed-vs-own-agent-cheatsheet.md) | Own agent vs Managed Agent, the four concepts, idle stop reasons |

1. Install the SDK: `pip install anthropic` (these files were tested with version 1.15.0).
2. Try it without an API key: `pip install pytest`, then in `sales-report/` run `python -m pytest -q` (1 passed).
3. With a key: set `ANTHROPIC_API_KEY`, then in `sales-report/` run `python setup_agent.py` once, then `python run_report.py`. You get `report.md` and `weekly.png`.

- Managed Agents is in beta. Its endpoints need the `managed-agents-2026-04-01` beta header, which the SDK adds for you.
- For this data the real numbers are: total revenue $499.80, best week Oct 12-18 ($147.45), top products Tote bag, Mug, T-shirt. The agent's exact tool calls and wording will differ from the video.
- Managed Agents usage is billed to your API account: check the Claude Console for pricing before running it often.
- Sessions are stored server-side, so Managed Agents isn't currently eligible for Zero Data Retention or HIPAA BAA coverage. You can delete sessions and files at any time.
- On Mac or Linux, use `python3` if `python` isn't found.

## Files in this folder

- `claude-managed-agents.mp4`: the video
- `claude-managed-agents.srt`: subtitles
- `script.json`, `make_script.py`: the video script (made with the claude-expert-video skill)
- `example-files/`: the sales report agent and the cheat sheet (no secrets: the test uses the fake key `sk-demo-1234` with a simulated API)

## Learn more

- [Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview)
- [Quickstart](https://platform.claude.com/docs/en/managed-agents/quickstart)
- [Attach and download files](https://platform.claude.com/docs/en/managed-agents/files)
- [Session event stream](https://platform.claude.com/docs/en/managed-agents/events-and-streaming)
