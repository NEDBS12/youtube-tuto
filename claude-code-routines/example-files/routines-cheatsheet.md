# Claude Code routines (scheduled tasks) cheat sheet

Routines are now called **scheduled tasks**. The old name stays in `claude.ai/code/routines`, the `/routines` alias,
and the API. Research preview: behavior and limits may change. Plans: Pro, Max, Team, Enterprise.

## What a routine is

A saved Claude Code setup: **a prompt + one or more GitHub repositories + connectors**, run automatically
in the cloud (your laptop can be closed). Each run is a full Claude Code cloud session that runs **without
permission prompts**, and acts **as you** (your GitHub user, your connector accounts).

## Triggers (combine as many as you like)

| Trigger | Starts a run when | Set it up |
|---|---|---|
| Schedule | Hourly, daily, weekly, a custom cron (min. 1 hour), or once at a set time | Web, or `/schedule` in the CLI |
| API | You POST to the task's `/fire` URL with its bearer token (optional `text` field) | Web only: copy the URL, **Generate token** (shown once) |
| GitHub | A pull request or release event matches (with optional filters) | Web, or `/schedule` (v2.1.225+); needs the Claude GitHub App |

## Commands

| Command | What it does |
|---|---|
| `/schedule every weekday at 9:07, ...` | Create a task conversationally (alias: `/routines`) |
| `/schedule tomorrow at 9am, ...` | A one-off run |
| `/schedule list` / `update` / `run` | See, change, or start a task now |
| `/schedule why did my ... do nothing?` | Claude reads the run history and explains (v2.1.227+) |

## Good habits

- Write a self-contained prompt that says what success looks like: nobody is watching the run.
- Scope what it can reach: only the repositories, network access and connectors it needs.
  Remove connectors you don't need: Claude can use all their tools, including writes, without asking.
- Schedule a few minutes past the hour (9:07, not 9:00): on-the-hour runs can start several minutes late.
- A green run only means the session started and exited: open the run to check what Claude did.
- API `text` arrives as untrusted data in a `<routine-fire-payload>` block. Your prompt must say how to use it.
- Never commit the API token: keep it in your CI or alerting tool's secret store.
- `/schedule` needs a claude.ai login (not an API key or cloud provider).

## Cloud task, Desktop task or /loop?

| | Cloud (routines) | Desktop | `/loop` |
|---|---|---|---|
| Runs on | Anthropic's cloud | Your machine | Your machine |
| Machine must be on | No | Yes | Yes |
| Open session needed | No | No | Yes |
| Local files | No (fresh clone) | Yes | Yes |
| Minimum interval | 1 hour | 1 minute | 1 minute |

Source: https://code.claude.com/docs/en/routines and https://code.claude.com/docs/en/scheduled-tasks
