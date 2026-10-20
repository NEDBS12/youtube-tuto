# Claude Code Plugins: Share Your Setup in One Install

Files from the Zero Cost AI video **"Claude Code Plugins Explained: Build and Share Your Own Plugin"**.

The video packs three tools from earlier videos into one plugin, `team-kit`, and shares it through a marketplace, so anyone can install all three with one command:

- a **hook** that blocks edits to `.env` files ([hooks video](../claude-code-hooks))
- a **subagent**, `test-runner`, that runs your tests and reports only the failures ([subagents video](../claude-code-subagents))
- a **skill**, `youtube-description`, that writes YouTube descriptions (from the skills video)

## Try the plugin

| File | What it does |
|---|---|
| [`.claude-plugin/plugin.json`](example-files/my-marketplace/plugins/team-kit/.claude-plugin/plugin.json) | The manifest: the plugin's name (the prefix on its skills and agents), description and version |
| [`hooks/hooks.json`](example-files/my-marketplace/plugins/team-kit/hooks/hooks.json) | Runs `scripts/protect_files.py` before every Edit or Write, using `${CLAUDE_PLUGIN_ROOT}` |
| [`agents/test-runner.md`](example-files/my-marketplace/plugins/team-kit/agents/test-runner.md) | The test-runner subagent (`team-kit:test-runner`) |
| [`skills/youtube-description/`](example-files/my-marketplace/plugins/team-kit/skills/youtube-description) | The skill (`/team-kit:youtube-description`) |
| [`my-marketplace/.claude-plugin/marketplace.json`](example-files/my-marketplace/.claude-plugin/marketplace.json) | The marketplace catalog that lists `team-kit` |

Copy the `my-marketplace` folder, then from the folder that contains it:

```bash
claude plugin validate ./my-marketplace/plugins/team-kit   # ✔ Validation passed
claude --plugin-dir ./my-marketplace/plugins/team-kit      # load it for one session
```

To install it for good instead, register the marketplace and install the plugin:

```bash
claude plugin marketplace add ./my-marketplace
claude plugin install team-kit@my-marketplace
```

To share it with your team, push `my-marketplace` to its own GitHub repository (so `.claude-plugin/marketplace.json` is at the repository root). Teammates then run:

```bash
claude plugin marketplace add your-name/my-marketplace
claude plugin install team-kit@my-marketplace
```

- The hook runs `python`; on Mac or Linux, change it to `python3` in `hooks/hooks.json` if needed.
- `claude --plugin-dir ./my-marketplace/plugins/team-kit plugin details team-kit` shows what the plugin loads and its context cost (about 90 tokens per session).
- Remove it with `claude plugin uninstall team-kit@my-marketplace`, or turn it off with `claude plugin disable team-kit@my-marketplace`.

## Files in this folder

- `claude-code-plugins.mp4`: the video
- `claude-code-plugins.srt`: subtitles
- `script.json`, `make_script.py`: the video script (made with the claude-expert-video skill)
- `example-files/my-marketplace/`: the marketplace with the `team-kit` plugin

## Learn more

- [Plugins overview](https://code.claude.com/docs/en/plugins)
- [Create a plugin](https://code.claude.com/docs/en/plugins/create)
- [Create a marketplace](https://code.claude.com/docs/en/plugins/create-marketplace)
