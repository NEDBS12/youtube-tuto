# Claude Code Hooks: Rules Claude Always Follows

Files from the Zero Cost AI video **"Claude Code Hooks Explained: Protect Your Files Step by Step"**.

The video builds a `PreToolUse` hook that blocks Claude Code from editing your `.env` file (or anything in a `secrets/` folder), even when auto-accept is on.

## Use the hook in your project

Copy these two files from [`example-files/my-app`](example-files/my-app) into your own project:

| File | What it does |
|---|---|
| [`.claude/hooks/protect_files.py`](example-files/my-app/.claude/hooks/protect_files.py) | Reads the tool call as JSON, exits with code `2` (block) if the file is protected, `0` otherwise |
| [`.claude/settings.json`](example-files/my-app/.claude/settings.json) | Registers the script as a `PreToolUse` hook for the `Edit` and `Write` tools |

Then start Claude Code in your project and ask it to edit `.env`: the edit is blocked and Claude explains why. Type `/hooks` to see the hook Claude Code loaded.

- Edit the `PROTECTED` list in the script to protect other files or folders.
- On Mac or Linux, change `"command": "python"` to `"command": "python3"` if `python` isn't found.
- If your settings file already has a `"hooks"` section, add `PreToolUse` inside it instead of replacing it.

Test the script on its own (it should print `Blocked: ...` and exit with code 2):

```bash
echo '{"tool_input":{"file_path":"my-app/.env"}}' | python .claude/hooks/protect_files.py
echo $?
```

## Files in this folder

- `claude-code-hooks.mp4`: the video
- `claude-code-hooks.srt`: subtitles
- `claude-code-hooks.youtube.txt`: title, description and tags
- `script.json`, `make_script.py`: the video script (made with the `claude-expert-video` skill)
- `example-files/my-app/`: the demo project (the `.env` holds fake demo values only)

## Learn more

- [Claude Code hooks guide](https://code.claude.com/docs/en/hooks-guide)
- [Hooks reference](https://code.claude.com/docs/en/hooks)
