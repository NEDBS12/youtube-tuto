# Claude Connectors: Connect Once, Use Everywhere

Files from the Zero Cost AI video **"Claude Connectors Explained: Use Notion from Claude Code, Step by Step"**.

A connector links Claude to an outside app (Notion, Gmail, Google Drive, your issue tracker) so Claude can find information there and act for you. You connect it once in claude.ai and it works in every Claude app, including Claude Code. In the video, Claude reads a bug list in Notion, fixes the top bug in a small shop project, runs the tests, and asks before marking the bug fixed in Notion.

## Use it in your project

| File | What it does |
|---|---|
| [`my-shop/`](example-files/my-shop) | The demo project: `cart.py` (with the shipping bug on purpose), its tests, and `CLAUDE.md` |
| [`my-shop/CLAUDE.md`](example-files/my-shop/CLAUDE.md) | Tells Claude where the bug reports live (the Notion page "my-shop bugs"), the test command, and to ask before changing Notion |
| [`notion-bug-page.md`](example-files/notion-bug-page.md) | The bug list to paste into a Notion page called **my-shop bugs** |
| [`connectors-cheatsheet.md`](example-files/connectors-cheatsheet.md) | One page: what to do, when |

1. In claude.ai, go to **Customize > Connectors**, open **Discover**, search **Notion**, select **Connect to Claude**, then sign in to Notion and approve access.
2. In Notion, create a page called **my-shop bugs** and paste the content of `notion-bug-page.md`.
3. Copy `my-shop/` to your computer, open a terminal in it, and start Claude Code signed in with the same claude.ai account (`claude`). Run `/mcp`: Notion is listed in the claude.ai section.
4. Ask: `Fix the top bug from our bug list`. Claude reads the page in Notion, fixes `cart.py`, runs `python -m pytest -q` (8 passed), and asks before updating Notion.

- Before the fix, the tests show `1 failed, 7 passed`: that's the bug from the Notion page (no free shipping at exactly 50).
- Connector missing in Claude Code? Run `/status`. Connectors only load with a claude.ai subscription login, not with an API key or a cloud provider. Then `/login`.
- Use it with your own apps: connect any service from the directory, then add one line to `CLAUDE.md` saying where your data lives.
- To turn connectors off in a repo, add `{ "disableClaudeAiConnectors": true }` to `.claude/settings.json`, or toggle one off in `/mcp` (this project only).

## Files in this folder

- `claude-code-connectors.mp4`: the video
- `claude-code-connectors.srt`: subtitles
- `script.json`, `make_script.py`: the video script (made with the claude-expert-video skill)
- `example-files/`: the demo project, the Notion page and the cheat sheet (no secrets: connectors use sign-in, not keys)

## Learn more

- [Get started with connectors](https://claude.com/docs/connectors/getting-started)
- [Add a connector that isn't in the directory](https://claude.com/docs/connectors/custom/add-unlisted)
- [Use MCP servers from claude.ai in Claude Code](https://code.claude.com/docs/en/mcp#use-mcp-servers-from-claude-ai)
- [Connector verification labels](https://claude.com/docs/connectors/verification)
