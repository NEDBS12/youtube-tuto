# Managed Agent or your own agent?

| | Your own agent (Messages API) | Claude Managed Agents (beta) |
|---|---|---|
| What it is | Direct model access: you write the agent loop | A pre-built agent harness running on Anthropic's infrastructure |
| The loop | Yours: `while stop_reason == "tool_use"` (or the SDK's Tool Runner) | Runs server-side: you send events, Claude runs the tools |
| Where tools run | In your app, on your machine or servers | In a cloud sandbox (or a self-hosted sandbox you run) |
| Built-in tools | None: you write each tool | bash, read, write, edit, glob, grep, web_fetch, web_search, plus MCP servers and custom tools |
| State | You keep the messages list | Sessions keep history, files and sandbox state server-side |
| Best for | Short tasks, custom loops, fine-grained control | Long-running tasks (minutes or hours), async work, scheduled runs |
| Data retention | Standard Messages API options | Stateful by design: not currently eligible for ZDR or HIPAA BAA coverage |

## The four Managed Agents concepts

| Concept | What it is | Create it |
|---|---|---|
| Agent | Model, system prompt, tools, MCP servers, skills | Once: `client.beta.agents.create(...)`, reuse by ID |
| Environment | Where sessions run: a cloud sandbox and its networking | Once: `client.beta.environments.create(...)` |
| Session | One running agent instance doing one task | Per task: `client.beta.sessions.create(agent=..., environment_id=...)` |
| Events | Messages between your app and the agent | `client.beta.sessions.events.send(...)` and `.stream(...)` |

## Session lifecycle

- Send a `user.message` event; the session streams `agent.tool_use`, `agent.message` and status events.
- `session.status_idle` means the agent stopped. Its `stop_reason.type` says why:
  `end_turn` (done: send more work any time), `requires_action` (a custom tool or a confirmation needs your answer),
  `budget_reached` (the session hit its budget).
- Uploaded files mount under `/mnt/session/uploads/`. Files the agent saves in `/mnt/session/outputs/`
  can be listed with `client.beta.files.list(scope_id=session.id, ...)` and downloaded.

## Good habits

- Set `networking` explicitly: a create request without it gets `unrestricted` access. Use `limited` unless the agent must reach sites you can't list.
- Create the agent and environment once, then start one session per task.
- Every Managed Agents request needs the `managed-agents-2026-04-01` beta header; the SDK adds it for you.

Sources: https://platform.claude.com/docs/en/managed-agents/overview,
https://platform.claude.com/docs/en/managed-agents/quickstart,
https://platform.claude.com/docs/en/managed-agents/files,
https://platform.claude.com/docs/en/managed-agents/events-and-streaming
