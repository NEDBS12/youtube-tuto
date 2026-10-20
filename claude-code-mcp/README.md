# MCP in Claude Code: Connect Claude to Your Tools

Files from the Zero Cost AI video **"MCP in Claude Code: Give Claude a Real Browser (Step by Step)"**.

The video connects the [Playwright MCP server](https://github.com/microsoft/playwright-mcp) to Claude Code, so Claude can open a web page in Chrome, fill in a form, click buttons, and find a bug a real user would hit.

## Try it yourself

The demo page in [`example-files/my-site`](example-files/my-site) has a hidden bug: after you sign up, the thank-you message never appears. Let Claude find it.

| File | What it does |
|---|---|
| [`index.html`](example-files/my-site/index.html) | A newsletter signup page with a one-letter bug |
| [`.mcp.json`](example-files/my-site/.mcp.json) | Shares the Playwright server with everyone who opens this folder in Claude Code |

1. Install [Node.js](https://nodejs.org) 18 or later (Playwright runs through `npx`) and Google Chrome.
2. Add the server (or rely on the included `.mcp.json` and approve it when Claude Code asks):
   ```bash
   claude mcp add playwright -- npx -y @playwright/mcp@latest
   ```
3. Check it: `claude mcp list` should show `✔ Connected`. The first check can fail while `npx` downloads the package; run it again.
4. Serve the page from the `my-site` folder: `python -m http.server 8000`
5. In a second terminal, start `claude` in the same folder and ask:
   ```text
   Use playwright to open http://localhost:8000, sign up with test@example.com, and tell me what happens
   ```

- Approve the tool permission the first time Claude Code asks.
- `claude mcp add` saves the server for you, in this project only. Add `--scope project` to write it to `.mcp.json` for your team, or `--scope user` for all your projects.
- Remove it when you're done: `claude mcp remove playwright`.

## Files in this folder

- `claude-code-mcp.mp4`: the video
- `claude-code-mcp.srt`: subtitles
- `script.json`, `make_script.py`: the video script (made with the claude-expert-video skill)
- `example-files/my-site/`: the demo page and `.mcp.json`

## Learn more

- [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp)
- [MCP quickstart](https://code.claude.com/docs/en/mcp-quickstart)
