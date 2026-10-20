# The Context Window: Claude's Working Memory

Files from the Zero Cost AI video **"Claude Code Context Window Explained: 4 Habits to Stop Claude Forgetting"**.

The context window is everything Claude can see right now: your messages, the files it read, command output, plus what loads automatically (Claude Code's instructions, `CLAUDE.md`, memory, skill and tool names). When it fills up, Claude Code compacts the conversation, and instructions you only typed in the chat can get lost. The video shows four habits to manage it.

## Use it in your project

| File | What it does |
|---|---|
| [`my-shop/CLAUDE.md`](example-files/my-shop/CLAUDE.md) | Lasting rules (run the tests after every change, never edit `.env`, keep answers short) and a `# Compact instructions` section that tells Claude what to keep when it summarizes |
| [`context-cheatsheet.md`](example-files/context-cheatsheet.md) | One page: which command to use when |

1. Copy `CLAUDE.md` to the root of your project and replace the rules with your own (for example your test command).
2. Start Claude Code in the project: `CLAUDE.md` loads automatically, and comes back after every compaction.
3. During long sessions, run `/context` to see what's using space.
4. Before a big new step, run `/compact focus on <what matters>`; when you switch to unrelated work, run `/rename <name>`, then `/clear` (and `/resume` to come back).

- The numbers `/context` shows depend on your model, your setup and your session.
- Big, noisy jobs (test runs, logs, research) are a good fit for a subagent: its output stays in its own context window.

## Files in this folder

- `claude-code-context-window.mp4`: the video
- `claude-code-context-window.srt`: subtitles
- `script.json`, `make_script.py`: the video script (made with the claude-expert-video skill)
- `example-files/`: the `CLAUDE.md` example and the cheat sheet

## Learn more

- [Explore the context window](https://code.claude.com/docs/en/context-window)
- [How Claude Code works: the context window](https://code.claude.com/docs/en/how-claude-code-works)
- [Reduce token usage](https://code.claude.com/docs/en/costs)
