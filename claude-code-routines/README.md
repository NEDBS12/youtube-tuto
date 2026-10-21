# Claude Code Routines: Put Claude on Autopilot

Files from the Zero Cost AI video **"Claude Code Routines Explained: Scheduled Tasks in the Cloud"**.

A routine (now called a **scheduled task**) is a saved Claude Code setup: a prompt, one or more GitHub repositories and the connectors it may use. It runs automatically in Anthropic's cloud, even when your laptop is closed. It starts on a schedule, from an API call, or on a GitHub event. In the video, a "test guard" routine runs the shop's tests every weekday at 9:07 and after every deploy, fixes failures on a `claude/` branch, and reports what it did.

## Use it in your project

| File | What it does |
|---|---|
| [`my-shop/test-guard-prompt.md`](example-files/my-shop/test-guard-prompt.md) | The routine's prompt: self-contained, says what success looks like, never pushes to main, treats fire text as context only |
| [`my-shop/scripts/fire-test-guard.sh`](example-files/my-shop/scripts/fire-test-guard.sh) | Starts the routine from a deploy script through its API trigger (reads `ROUTINE_URL` and `ROUTINE_TOKEN` from the environment) |
| [`my-shop/`](example-files/my-shop) | The demo project: `cart.py` (with the shipping bug left in on purpose, `1 failed, 7 passed`), its tests and `CLAUDE.md` |
| [`routines-cheatsheet.md`](example-files/routines-cheatsheet.md) | Triggers, commands, good habits, and cloud vs Desktop vs `/loop` |

1. Push `my-shop/` to a GitHub repository of your own.
2. In Claude Code, signed in with your claude.ai account (Pro, Max, Team or Enterprise), open the project and run:
   `/schedule every weekday at 9:07am, run the prompt in test-guard-prompt.md`. Answer Claude's follow-up questions.
3. Open [claude.ai/code/routines](https://claude.ai/code/routines): check the repository and environment, and remove the connectors the task doesn't need.
4. Optional: in **Edit**, add a **GitHub event** trigger (pull request opened, is draft = false; needs the Claude GitHub App) and an **API** trigger. Copy the fire URL and generate the token (shown once), store both as secrets, then call `bash scripts/fire-test-guard.sh v1.4.2` from your deploy.
5. Click **Run now**, then open the run (or ask `/schedule what did my test guard do this morning?`) to read what Claude did.

- Scheduled tasks are in research preview: behavior, limits and the API may change.
- Runs have no permission prompts and act as you (your GitHub user, your connector accounts). Give each task only the repositories, network access and connectors it needs.
- The minimum interval is one hour, and runs use your subscription like normal sessions.
- `/schedule` needs a claude.ai login. With an API key or a cloud provider login, it isn't available; you can still use the web page.
- I tested `fire-test-guard.sh` against a local copy of the `/fire` endpoint (headers, body and response). The routine runs shown in the video are recreations: your Claude's wording will differ.

## Files in this folder

- `claude-code-routines.mp4`: the video
- `claude-code-routines.srt`: subtitles
- `script.json`, `make_script.py`: the video script (made with the claude-expert-video skill)
- `example-files/`: the demo project, the prompt, the fire script and the cheat sheet (no secrets: the token comes from your environment)

## Learn more

- [Automate work with scheduled tasks (routines)](https://code.claude.com/docs/en/routines)
- [Compare scheduling options](https://code.claude.com/docs/en/scheduled-tasks#compare-scheduling-options)
- [Trigger a routine through the API](https://platform.claude.com/docs/en/api/claude-code/routines-fire)
- [Cloud environments](https://code.claude.com/docs/en/cloud-environments)
