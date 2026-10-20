# Claude Code context window cheat sheet

| When | Do this |
|---|---|
| You want to see what's using space | `/context` (live breakdown by category, with suggestions) |
| A rule must last the whole session, and every session | Put it in `CLAUDE.md`, not in the chat |
| The session is long and you're starting a big new step | `/compact focus on <what matters>` |
| You switch to unrelated work | `/rename <name>`, then `/clear` (start fresh; `/resume` to come back) |
| A task produces lots of output (tests, logs, research) | Hand it to a subagent, so the output stays in its own context |
| You keep plugins or MCP servers you don't use | Disable them: they add descriptions to every session |

- Claude Code compacts automatically as you approach the limit: it clears older tool output first, then summarizes the conversation.
- After compaction, the project-root `CLAUDE.md` and auto memory are re-injected from disk; instructions you only typed in the chat may be lost.
- Add a `# Compact instructions` section to `CLAUDE.md` to tell Claude what to keep when it compacts.

Source: https://code.claude.com/docs/en/context-window and https://code.claude.com/docs/en/how-claude-code-works
