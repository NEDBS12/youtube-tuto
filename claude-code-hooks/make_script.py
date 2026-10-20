"""Generates script.json for the Claude Code hooks tutorial from the real example files."""
import json, pathlib

HERE = pathlib.Path(__file__).parent
APP = HERE / "example-files" / "my-app"
SCRIPT = (APP / ".claude/hooks/protect_files.py").read_text(encoding="utf-8")
SETTINGS = (APP / ".claude/settings.json").read_text(encoding="utf-8")
APP_PY = (APP / "app.py").read_text(encoding="utf-8")
ENV = (APP / ".env").read_text(encoding="utf-8")

# split the hook script into the three chunks typed on screen
a = SCRIPT.index("# Claude Code sends")
b = SCRIPT.index("for pattern")
S1, S2, S3 = SCRIPT[:a], SCRIPT[a:b], SCRIPT[b:]
HOOK = ".claude/hooks/protect_files.py"
SET = ".claude/settings.json"
TEST_JSON = """echo '{"tool_input":{"file_path":"my-app/.env"}}' | python .claude/hooks/protect_files.py"""

script = {
 "title": "claude-code-hooks",
 "steps": ["Write the script", "Register the hook", "Test it", "Go further"],
 "scenes": [
  {"type": "title", "chapter": "Introduction", "kicker": "Claude Code tutorial · step by step",
   "title": "Claude Code Hooks\n[[Rules Claude Always Follows]]", "subtitle": "What hooks are, when to use them, and how to build one in 3 steps",
   "lines": [
    {"say": "What if Claude edited a file you never wanted it to touch, like the file with your passwords and API keys?"},
    {"say": "In this video, you'll learn how to stop that for good, with Claude Code hooks."},
    {"say": "I'll explain what a hook is, when to use one, and then we'll build a real one together, step by step.", "hold": 0.6}]},

  {"type": "bullets", "chapter": "What is a hook?", "kicker": "**01** · The concept", "heading": "What is a [[hook]]?",
   "items": ["A **command** that Claude Code runs **automatically**, at a moment you choose",
             "These moments are called **events**: before a tool runs, after an edit, when Claude stops…",
             "Your script decides what happens: **carry on**, or **block** and explain why"],
   "card": {"title": "SETTINGS.JSON · THE SHAPE OF A HOOK", "code": "\"hooks\": {\n  \"PreToolUse\": [{\n    \"matcher\": \"Edit|Write\",\n    \"hooks\": [{\n      \"type\": \"command\",\n      \"command\": \"python\" ...\n    }]\n  }]\n}"},
   "lines": [
    {"say": "So, what is a hook?", "do": [{"k": "show", "el": "heading"}]},
    {"say": "A hook is a command that Claude Code runs automatically, at a moment you choose.", "do": [{"k": "show", "el": "item1"}, {"k": "show", "el": "card", "at": 0.8}]},
    {"say": "Those moments are called events. For example: just before Claude uses a tool, right after it edits a file, or when it finishes answering.", "do": [{"k": "show", "el": "item2"}]},
    {"say": "Your command can simply let things carry on. Or it can block the action, and tell Claude why.", "do": [{"k": "show", "el": "item3"}]},
    {"say": "You set hooks up in a settings file, with a few lines of JSON, like the ones on the right.", "hold": 0.5}]},

  {"type": "rows", "chapter": "How a hook works", "kicker": "**02** · How it works", "heading": "How a hook [[works]]",
   "rows": [{"label": "Event + matcher", "text": "Before Claude uses the **Edit** or **Write** tool"},
            {"label": "Your script runs", "text": "It receives the details as JSON, and decides"},
            {"label": "The result", "text": "Exit **0** = carry on · Exit **2** = block, and Claude is told why"}],
   "banner": "✓ A hook runs every single time. It doesn't depend on Claude remembering a rule",
   "lines": [
    {"say": "Here's how a hook works, in three parts.", "do": [{"k": "show", "el": "heading"}]},
    {"say": "First, an event and a matcher. For example: just before Claude uses the Edit or Write tool.", "do": [{"k": "show", "el": "row1"}]},
    {"say": "Second, your script runs. Claude Code sends it the details, like which file Claude wants to change.", "do": [{"k": "show", "el": "row2"}]},
    {"say": "Third, the result. Exit with code zero, and Claude carries on. Exit with code two, and the action is blocked, and Claude reads your reason.", "do": [{"k": "show", "el": "row3"}]},
    {"say": "And here's the key point: a hook runs every single time. It doesn't depend on Claude remembering a rule.", "do": [{"k": "show", "el": "banner"}], "hold": 0.5}]},

  {"type": "compare", "chapter": "When to use a hook", "kicker": "**03** · When to use it", "heading": "Instruction vs. [[hook]]",
   "left": {"title": "CLAUDE.md instruction", "body": "\"Please never edit .env\"\n\n• Claude reads it as guidance\n• Usually followed, not guaranteed\n• Great for style and preferences"},
   "right": {"title": "Hook", "body": "A script that checks every edit\n\n• Runs every single time\n• Can block the action\n• Great for rules that must **always** hold"},
   "lines": [
    {"say": "So when should you use a hook, instead of just writing an instruction?", "do": [{"k": "show", "el": "heading"}]},
    {"say": "An instruction in CLAUDE.md is guidance. Claude usually follows it, but it's not guaranteed. That's perfect for style and preferences.", "tts": "An instruction in CLAUDE dot M D is guidance. Claude usually follows it, but it's not guaranteed. That's perfect for style and preferences.", "do": [{"k": "show", "el": "left"}]},
    {"say": "A hook is code that runs every time. Use it for rules that must always hold, or actions that must always happen.", "do": [{"k": "show", "el": "arrow"}, {"k": "show", "el": "right", "at": 0.4}], "hold": 0.5}]},

  {"type": "cards", "chapter": "Common hook events", "kicker": "**04** · Popular events", "heading": "Four events you'll [[use most]]",
   "cards": [{"title": "PreToolUse", "text": "Before a tool runs: check it, or block it"},
             {"title": "PostToolUse", "text": "After a tool succeeds: format or lint the file"},
             {"title": "Notification", "text": "Claude needs you: get a desktop alert"},
             {"title": "Stop", "text": "Claude finished answering: run a final check"}],
   "lines": [
    {"say": "There are many events. Here are four you'll use the most.", "do": [{"k": "show", "el": "heading"}]},
    {"say": "PreToolUse runs before a tool, so it can check the action, or block it.", "tts": "Pre Tool Use runs before a tool, so it can check the action, or block it.", "do": [{"k": "show", "el": "card1"}]},
    {"say": "PostToolUse runs after a tool succeeds. For example, to format a file Claude just edited.", "tts": "Post Tool Use runs after a tool succeeds. For example, to format a file Claude just edited.", "do": [{"k": "show", "el": "card2"}]},
    {"say": "Notification runs when Claude needs your attention, so you can get a desktop alert.", "do": [{"k": "show", "el": "card3"}]},
    {"say": "And Stop runs when Claude finishes answering.", "do": [{"k": "show", "el": "card4"}], "hold": 0.5}]},

  {"type": "compare", "chapter": "Our example", "kicker": "**05** · Our example", "heading": "Protect your [[secrets]]",
   "left": {"title": ".env · your secret keys", "code": "API_KEY=sk-demo-1234\nDB_PASSWORD=change-me"},
   "right": {"title": "With a PreToolUse hook", "body": "Claude tries to edit **.env**\n→ the hook blocks it\n→ Claude explains, and moves on\n\nEvery other file works as normal"},
   "lines": [
    {"say": "Our example: protecting your secrets.", "do": [{"k": "show", "el": "heading"}]},
    {"say": "Most projects have a dot env file, with passwords and API keys. Claude should never change it.", "do": [{"k": "show", "el": "left"}]},
    {"say": "With a PreToolUse hook, any attempt to edit it is blocked, Claude explains why, and every other file works as normal.", "tts": "With a Pre Tool Use hook, any attempt to edit it is blocked, Claude explains why, and every other file works as normal.", "do": [{"k": "show", "el": "arrow"}, {"k": "show", "el": "right", "at": 0.5}], "hold": 0.6}]},

  {"type": "screen", "chapter": "The problem without a hook", "project": "my-app", "kicker": "**DEMO** · The problem", "lines": [
    {"say": "First, the problem. Here's a small Python project, with my secrets in a dot env file.", "do": [{"k": "file", "path": ".env", "text": ENV, "open": False}, {"k": "file", "path": "app.py", "text": APP_PY}, {"k": "open", "path": ".env", "at": 2.0}]},
    {"say": "I've turned on auto-accept for edits, so Claude can work without asking me each time.", "do": [{"k": "cmd", "text": "claude", "cps": 12}, {"k": "claude", "at": 1.0}]},
    {"say": "Now I ask: clean up the formatting in my config files.", "do": [{"k": "cprompt", "text": "Clean up the formatting in my config files", "cps": 26}]},
    {"say": "Claude edited the dot env file too, where my secret keys live. It was trying to help, but I didn't want that.", "do": [{"k": "cout", "lines": ["tool:Edit(.env)", "res:Updated .env", "ai:Done! I tidied up .env and sorted the keys."], "dur": 1.2}, {"k": "callout", "at": 1.6, "dur": 5.5, "target": "term", "match": "Edit(.env)", "span": 2, "label": "It changed my secrets file"}]},
    {"say": "Let's make sure this can never happen again.", "hold": 0.4},

    {"say": "Step one: write the hook script.", "do": [{"k": "step", "n": 1}, {"k": "clear"}, {"k": "open", "path": HOOK, "at": 0.4}]},
    {"say": "I create a hooks folder inside dot claude, with a small Python file.", "do": [{"k": "callout", "dur": 3.8, "target": "tree", "match": "protect_files.py", "label": "Your hook script"}]},
    {"say": "At the top, I list what Claude must never edit: the dot env file, and a secrets folder.", "do": [{"k": "type", "path": HOOK, "text": S1, "cps": 26}, {"k": "callout", "at": 2.6, "dur": 3.5, "target": "editor", "match": "PROTECTED =", "label": "Your protected list"}]},
    {"say": "When the hook runs, Claude Code sends the details of the tool call as JSON. I read the file path Claude wants to change.", "do": [{"k": "type", "path": HOOK, "text": S2, "cps": 30}, {"k": "callout", "at": 3.6, "dur": 4.0, "target": "editor", "match": "data = json", "span": 2, "label": "The file Claude wants to edit"}]},
    {"say": "This line turns Windows backslashes into forward slashes, so the check works on every computer.", "do": [{"k": "callout", "dur": 4.5, "target": "editor", "match": "replace(", "label": "Works on Windows too"}]},
    {"say": "Then the check. If the path matches a protected pattern, I print a reason, and exit with code two.", "do": [{"k": "type", "path": HOOK, "text": S3, "cps": 30}, {"k": "callout", "at": 4.4, "dur": 4.5, "target": "editor", "match": "sys.exit(2)", "label": "2 = block · reason goes to Claude"}]},
    {"say": "Otherwise, exit with code zero, and Claude carries on as usual.", "do": [{"k": "callout", "dur": 3.6, "target": "editor", "match": "sys.exit(0)", "label": "0 = no objection"}]},
    {"say": "Before wiring it up, I test it by hand, with a fake tool call.", "do": [{"k": "cmd", "text": TEST_JSON, "cps": 40, "out": ["Blocked: my-app/.env is protected."]}]},
    {"say": "It prints the reason. And the exit code is two. The script works.", "do": [{"k": "cmd", "text": "echo $?", "cps": 12, "out": ["2"]}, {"k": "callout", "at": 1.4, "dur": 3.5, "target": "term", "match": "Blocked: my-app", "label": "Blocked, exit code 2"}], "hold": 0.4},

    {"say": "Step two: register the hook in your settings.", "do": [{"k": "step", "n": 2}, {"k": "open", "path": SET, "at": 0.4}]},
    {"say": "In the project's .claude folder, I open settings.json, and add a hooks section.", "tts": "In the project's dot claude folder, I open settings dot JSON, and add a hooks section.", "do": [{"k": "type", "path": SET, "text": SETTINGS, "cps": 40}]},
    {"say": "The event is PreToolUse, so it runs just before Claude uses a tool.", "tts": "The event is Pre Tool Use, so it runs just before Claude uses a tool.", "do": [{"k": "callout", "dur": 4.0, "target": "editor", "match": "PreToolUse", "label": "The event: before a tool runs"}]},
    {"say": "The matcher says which tools: only Edit and Write, the tools Claude uses to change files.", "do": [{"k": "callout", "dur": 4.6, "target": "editor", "match": "matcher", "label": "Only for Edit and Write"}]},
    {"say": "And the command runs my script with Python. The project dir variable always points to the project folder.", "tts": "And the command runs my script with Python. The project dir variable always points to the project folder.", "do": [{"k": "callout", "dur": 5.5, "target": "editor", "match": "\"command\": \"python\"", "span": 2, "label": "Run my script with Python"}]},
    {"say": "On a Mac or Linux, you might need to write python3 instead.", "tts": "On a Mac or Linux, you might need to write python 3 instead."},
    {"say": "Where you save the hook decides who it protects. This project's settings file can be committed, so your whole team gets it.", "do": [{"k": "note", "dur": 7.5, "title": "Where hooks live", "rows": [["`.claude/settings.json`", "this project, shared"], ["`.claude/settings.local.json`", "this project, just you"], ["`~/.claude/settings.json`", "all your projects"]]}], "hold": 0.5},

    {"say": "Step three: test it.", "do": [{"k": "step", "n": 3}, {"k": "clear"}]},
    {"say": "I start Claude Code again, still with auto-accept on, and repeat the same request.", "do": [{"k": "cmd", "text": "claude", "cps": 12}, {"k": "claude", "at": 1.0}, {"k": "cprompt", "at": 1.6, "text": "Clean up the formatting in my config files", "cps": 26}]},
    {"say": "Claude tries to edit dot env, and the hook blocks it, before anything changes.", "do": [{"k": "cout", "lines": ["tool:Edit(.env)", "res:Blocked by PreToolUse hook:", "res:Blocked: my-app/.env is protected."], "dur": 1.0}, {"k": "callout", "at": 1.2, "dur": 5.0, "target": "term", "match": "Blocked by PreToolUse", "span": 2, "label": "Blocked by the hook"}]},
    {"say": "Claude reads the reason, explains it to me, and moves on.", "do": [{"k": "cout", "lines": ["ai:I couldn't edit .env, because a project hook protects it. If a change is needed there, you can make it yourself.", ""], "dur": 0.8}]},
    {"say": "Even with auto-accept turned on, the hook still has the final word.", "hold": 0.3},
    {"say": "And normal files still work. I ask for a docstring in app dot py, and the edit goes through.", "do": [{"k": "cprompt", "text": "Add a docstring to greet in app.py", "cps": 24}, {"k": "cout", "at": 2.4, "lines": ["tool:Edit(app.py)", "res:Updated app.py", "ai:Added a docstring to greet()."], "dur": 1.0}, {"k": "callout", "at": 3.6, "dur": 4.0, "target": "term", "match": "Edit(app.py)", "span": 2, "label": "Other files: allowed"}], "hold": 0.6}]},

  {"type": "cards", "kicker": "**STEP 4** · Go further", "heading": "4 tips to [[go further]]", "rail": True,
   "cards": [{"title": "Check with /hooks", "text": "See every hook Claude Code has loaded"},
             {"title": "Test the script alone", "text": "Pipe in sample JSON, check the exit code"},
             {"title": "Share it", "text": "Commit `.claude/`: your whole team is protected"},
             {"title": "Try other events", "text": "PostToolUse to format files, Notification for alerts"}],
   "lines": [
    {"say": "Step four: go further. Here are four tips.", "do": [{"k": "step", "n": 4}, {"k": "show", "el": "heading"}]},
    {"say": "One: type slash hooks in Claude Code, to see every hook it has loaded.", "do": [{"k": "show", "el": "card1"}]},
    {"say": "Two: always test your script on its own first, like we did, by piping in sample JSON and checking the exit code.", "do": [{"k": "show", "el": "card2"}]},
    {"say": "Three: commit the dot claude folder to git, and your whole team is protected.", "do": [{"k": "show", "el": "card3"}]},
    {"say": "Four: try other events. A PostToolUse hook can format every file Claude edits, and a Notification hook can alert you when Claude needs you.", "tts": "Four: try other events. A Post Tool Use hook can format every file Claude edits, and a Notification hook can alert you when Claude needs you.", "do": [{"k": "show", "el": "card4"}], "hold": 0.6}]},

  {"type": "checks", "chapter": "Recap", "heading": "Recap",
   "items": ["A hook = a command Claude Code runs at an **event**",
             "Exit `0` to carry on · exit `2` to block, and Claude is told why",
             "Use hooks for rules that must [[always]] hold"],
   "lines": [
    {"say": "Let's recap.", "do": [{"k": "show", "el": "heading"}]},
    {"say": "A hook is a command that Claude Code runs automatically, at an event you choose.", "do": [{"k": "show", "el": "item1"}]},
    {"say": "Exit with code zero to carry on, or code two to block the action, and tell Claude why.", "do": [{"k": "show", "el": "item2"}]},
    {"say": "Use instructions for preferences, and hooks for rules that must always hold.", "do": [{"k": "show", "el": "item3"}], "hold": 0.5}]},

  {"type": "outro", "title": "Thanks for [[watching]]", "subtitle": "The hook files are in the description", "lines": [
    {"say": "The hook script and settings from this video are linked in the description, so you can copy them and try it today.", "do": [{"k": "show", "el": "line1"}]},
    {"say": "If this helped, like the video, and subscribe to Zero Cost AI for more free AI tutorials. See you in the next one!", "do": [{"k": "show", "el": "line2"}], "hold": 1.5}]},
 ]}

(HERE / "script.json").write_text(json.dumps(script, indent=1, ensure_ascii=False), encoding="utf-8")
print("script.json written:", sum(len(s["lines"]) for s in script["scenes"]), "lines")
