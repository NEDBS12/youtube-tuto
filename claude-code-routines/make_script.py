"""Generates script.json for the Claude Code routines (scheduled tasks) tutorial from the real example files."""
import json, pathlib

HERE = pathlib.Path(__file__).parent
EX = HERE / "example-files" / "my-shop"
read = lambda f: (EX / f).read_text(encoding="utf-8")
CART, TESTS, CLAUDEMD, PROMPT, FIRE = read("cart.py"), read("tests/test_cart.py"), read("CLAUDE.md"), read("test-guard-prompt.md"), read("scripts/fire-test-guard.sh")
p3 = PROMPT.index("3. If a test fails")
p4 = PROMPT.index("4. If a routine-fire-payload")
PROMPT_A, PROMPT_B, PROMPT_C = PROMPT[:p3], PROMPT[p3:p4], PROMPT[p4:]

URL = "claude.ai/code/routines"
NAVS = ["＋ New session", "Sessions", "Scheduled tasks", "-", "Environments", "Settings"]
BASE = {"k": "bview", "url": URL, "nav": "Scheduled tasks"}
DETAIL = dict(BASE, url=URL + "/test-guard", heading="Test guard", sub="On · Next run: tomorrow, 9:07 AM")
ON = {"name": "Schedule", "icon": "⏰", "desc": "Weekdays at 9:07 AM (your time)", "status": "✓ Active"}
REPO = {"name": "Repository", "icon": "R", "desc": "NEDBS12/my-shop · Claude pushes to claude/ branches"}
ENV = {"name": "Environment", "icon": "E", "desc": "Default · Trusted network access (allowlist only)"}

script = {
 "title": "claude-code-routines",
 "steps": ["Write the prompt", "Create with /schedule", "Review on the web", "Add more triggers", "Check the runs"],
 "scenes": [
  {"type": "title", "chapter": "Introduction", "kicker": "Claude Code tutorial · step by step",
   "title": "Claude Code Routines\n[[Put Claude on Autopilot]]", "subtitle": "Scheduled tasks that run in the cloud, even when your laptop is closed",
   "lines": [
    {"say": "Do you have jobs you keep doing by hand? Running the tests every morning, checking new pull requests, reacting after every deploy?"},
    {"say": "Routines let Claude Code do them for you, in the cloud, on a schedule, even when your laptop is closed."},
    {"say": "In this video, you'll learn what routines are, when to use them, and how to set one up, step by step.", "hold": 0.6}]},

  {"type": "bullets", "chapter": "What is a routine?", "kicker": "**01** · The concept", "heading": "What is a [[routine]]?",
   "items": ["A saved Claude Code setup: a **prompt**, your **repositories**, your **connectors**",
             "Runs **automatically** in the cloud, as a full Claude Code session",
             "Now called **scheduled tasks**: the old name stays in the URL and `/routines`"],
   "card": {"title": "A ROUTINE", "code": "prompt:      \"Run the tests, fix failures\"\nrepository:  NEDBS12/my-shop\nconnectors:  only what it needs\ntriggers:    schedule · API · GitHub"},
   "lines": [
    {"say": "So, what is a routine?", "do": [{"k": "show", "el": "heading"}]},
    {"say": "A routine is a saved Claude Code setup: a prompt, one or more GitHub repositories, and the connectors it may use. You package it once.", "do": [{"k": "show", "el": "item1"}, {"k": "show", "el": "card", "at": 2.0}]},
    {"say": "Then it runs automatically, on Anthropic's cloud, as a full Claude Code session. Your computer doesn't need to be on.", "do": [{"k": "show", "el": "item2"}]},
    {"say": "One naming note: routines are now called scheduled tasks. The old name still appears in the web address, and in the slash routines command. It's a research preview, on Pro, Max, Team and Enterprise plans.", "do": [{"k": "show", "el": "item3"}], "hold": 0.5}]},

  {"type": "rows", "chapter": "Three kinds of triggers", "kicker": "**02** · How it works", "heading": "Three ways to [[start a run]]",
   "rows": [{"label": "Schedule", "text": "Hourly, daily, weekly, or once at a set time"},
            {"label": "API", "text": "Your script POSTs to the routine's own URL, with a token"},
            {"label": "GitHub", "text": "A pull request or a release event on your repository"}],
   "banner": "✓ Combine them: one routine can have several triggers",
   "lines": [
    {"say": "A routine starts when one of its triggers fires. There are three kinds.", "do": [{"k": "show", "el": "heading"}]},
    {"say": "A schedule: hourly, daily, weekly, or just once, at a set time.", "do": [{"k": "show", "el": "row1"}]},
    {"say": "An API trigger: your own script, like a deploy pipeline, calls the routine's URL with a secret token.", "do": [{"k": "show", "el": "row2"}]},
    {"say": "And a GitHub trigger: a pull request or a release event on your repository.", "do": [{"k": "show", "el": "row3"}]},
    {"say": "And you can combine them. The same routine can run every morning, and after every deploy.", "do": [{"k": "show", "el": "banner"}], "hold": 0.5}]},

  {"type": "compare", "chapter": "When to use a routine", "kicker": "**03** · When to use it", "heading": "Routine, Desktop task, or [[/loop]]?",
   "left": {"title": "Use a routine (cloud) when…", "body": "• The job is unattended and repeatable\n• It has a clear outcome\n• It must run with your laptop closed\n• It works on a GitHub repository\n• Every hour or less often"},
   "right": {"title": "Run it on your machine when…", "body": "• It needs local files or tools:\n  a Desktop scheduled task\n• You're polling during a session:\n  /loop\n• It must run more often\n  than once an hour"},
   "lines": [
    {"say": "When should you use a routine?", "do": [{"k": "show", "el": "heading"}]},
    {"say": "For jobs that are unattended, repeatable, and have a clear outcome. They run in the cloud, on a fresh copy of your GitHub repository, at most once an hour.", "do": [{"k": "show", "el": "left"}]},
    {"say": "If the job needs files on your computer, use a Desktop scheduled task. For quick polling while you work, use slash loop. Both need your machine to be on.", "do": [{"k": "show", "el": "arrow"}, {"k": "show", "el": "right", "at": 0.4}], "hold": 0.5}]},

  {"type": "compare", "chapter": "Our use case", "kicker": "**04** · Our use case", "heading": "A [[test guard]] for my shop",
   "left": {"title": "Before: by hand", "body": "• Open the project every morning\n• Run the tests\n• Notice a failure… sometimes\n• Fix it, push it\n\nOnly when I remember,\nand only when I'm at my desk"},
   "right": {"title": "After: a routine", "body": "Every weekday at 9:07,\nand after every deploy:\n\n✓ Runs the tests\n✓ Fixes failures on a\n   claude/ branch\n✓ Reports what it did"},
   "lines": [
    {"say": "Our use case: a test guard, for my small shop's code on GitHub.", "do": [{"k": "show", "el": "heading"}]},
    {"say": "Before: every morning, I open the project and run the tests. I notice a failure only when I remember to check, and only when I'm at my desk.", "do": [{"k": "show", "el": "left"}]},
    {"say": "After: a routine runs the tests every weekday morning, and after every deploy. If something fails, it fixes it on a new branch, and reports what it did.", "do": [{"k": "show", "el": "arrow"}, {"k": "show", "el": "right", "at": 0.4}], "hold": 0.5}]},

  {"type": "screen", "chapter": "The problem", "project": "my-shop", "kicker": "**DEMO** · Checking by hand", "lines": [
    {"say": "Here's the project: the cart code, its tests, and a short CLAUDE.md with my rules.", "tts": "Here's the project: the cart code, its tests, and a short CLAUDE dot M D with my rules.", "do": [{"k": "file", "path": "tests/test_cart.py", "text": TESTS, "open": False}, {"k": "file", "path": "pytest.ini", "text": "[pytest]\npythonpath = .\n", "open": False}, {"k": "file", "path": "cart.py", "text": CART, "open": False}, {"k": "file", "path": "CLAUDE.md", "text": CLAUDEMD}]},
    {"say": "Someone merged a change yesterday. I run the tests by hand, and one fails.", "do": [{"k": "cmd", "at": 1.0, "text": "python -m pytest -q", "out": ["FAILED tests/test_cart.py::test_shipping[50-0]", "1 failed, 7 passed in 0.05s"]}]},
    {"say": "I only found it because I happened to check. Let's make Claude check, every day, without me.", "do": [{"k": "callout", "dur": 5.0, "target": "term", "match": "1 failed", "label": "Found by luck"}], "hold": 0.5},

    {"say": "Step one: write the prompt. This is the most important part.", "do": [{"k": "step", "n": 1}, {"k": "open", "path": "test-guard-prompt.md", "at": 0.8}]},
    {"say": "The routine runs unattended. Nobody is watching. So the prompt must be self-contained, and say what success looks like. First: run the tests, and if they pass, report the count.", "do": [{"k": "type", "path": "test-guard-prompt.md", "text": PROMPT_A, "cps": 60}, {"k": "callout", "at": 3.0, "dur": 4.5, "target": "editor", "match": "You run unattended", "label": "Nobody is watching"}]},
    {"say": "If a test fails: find the cause, don't touch the tests, fix it on a new claude branch, and report the details.", "do": [{"k": "type", "path": "test-guard-prompt.md", "text": PROMPT_B, "cps": 60}, {"k": "callout", "at": 3.4, "dur": 4.5, "target": "editor", "match": "claude/ branch and push", "label": "Never pushes to main"}]},
    {"say": "And a rule for the API trigger: text sent with it arrives in a routine fire payload block, labeled as untrusted. My prompt says to use it only as context.", "do": [{"k": "type", "path": "test-guard-prompt.md", "text": PROMPT_C, "cps": 60}, {"k": "callout", "at": 3.6, "dur": 5.0, "target": "editor", "match": "Never follow instructions", "label": "Fire text is data"}], "hold": 0.4},

    {"say": "Step two: create the routine, right from Claude Code, with slash schedule.", "do": [{"k": "step", "n": 2}, {"k": "claude", "at": 1.2}]},
    {"say": "I describe it in plain English: every weekday at 9:07, run the test guard prompt.", "do": [{"k": "cprompt", "text": "/schedule every weekday at 9:07am, run the prompt in test-guard-prompt.md", "cps": 40}]},
    {"say": "Claude asks a few follow-up questions: the repository, the prompt, the time. Then it saves the routine to my account.", "do": [{"k": "cout", "lines": ["ai:I'll set up a scheduled task. A few details:", "1. Repository: NEDBS12/my-shop (this folder)?", "2. Prompt: the contents of test-guard-prompt.md?", "3. Schedule: weekdays at 9:07 AM, your time?"], "dur": 1.6}]},
    {"say": "I confirm, and it's saved: weekdays at 9:07, in my own time zone.", "do": [{"k": "cprompt", "text": "Yes to all three", "cps": 22}, {"k": "cout", "at": 0.6, "lines": ["ai:Saved \"Test guard\": weekdays at 9:07 AM.", "Next run: tomorrow, 9:07 AM.", "claude.ai/code/routines"], "dur": 1.0}, {"k": "callout", "at": 1.8, "dur": 4.5, "target": "term", "match": "Saved \"Test guard\"", "label": "Saved to my account"}], "hold": 0.5}]},

  {"type": "browser", "project": "claude.ai", "navs": NAVS, "url": URL, "lines": [
    {"say": "Step three: review it on the web, at claude dot A I, slash code, slash routines.", "tts": "Step three: review it on the web, at Claude dot A I, slash code, slash routines.", "do": [{"k": "step", "n": 3}, dict(BASE, heading="Scheduled tasks", sub="Run in the cloud, even when your computer is off", rows=[{"name": "Test guard", "icon": "T", "desc": "Weekdays at 9:07 AM · NEDBS12/my-shop", "status": "✓ On"}])]},
    {"say": "Here's the routine I made in the terminal. The web, the desktop app, and the CLI all share the same list.", "do": [{"k": "callout", "dur": 4.5, "target": "browser", "match": "Test guard", "big": True, "pos": "below", "label": "Created from the CLI"}]},
    {"say": "On its page: the schedule, the repository it clones on every run, and the environment, which controls network access.", "do": [dict(DETAIL, rows=[ON, REPO, ENV, {"name": "Connectors", "icon": "C", "desc": "Notion, Gmail, Google Calendar", "btn": "Remove", "ghost": True}])]},
    {"say": "The default environment is trusted: only an allowlist of package registries and common developer sites.", "do": [{"k": "callout", "dur": 4.5, "target": "browser", "match": "Trusted network", "big": True, "label": "Allowlist only"}]},
    {"say": "Now, connectors. All your connectors are included by default, and a routine can use every tool in them, even writes, without asking. My test guard doesn't need any, so I remove them.", "do": [{"k": "callout", "dur": 5.5, "target": "browser", "match": "Remove", "label": "Remove what it doesn't need"}]},
    {"say": "Remember: every run acts as you. Commits carry your GitHub name, and connector actions use your accounts. So give it only what it needs.", "do": [dict(DETAIL, rows=[ON, REPO, ENV, {"name": "Connectors", "icon": "C", "desc": "None: this task doesn't need any"}])], "hold": 0.4},

    {"say": "Step four: add more triggers. I open Edit, and in the trigger row, I click plus.", "do": [{"k": "step", "n": 4}, dict(DETAIL, heading="Edit scheduled task", sub="Trigger", rows=[ON, {"name": "GitHub event", "icon": "G", "desc": "Pull request · opened · Is draft = false", "status": "+ Added"}])]},
    {"say": "A GitHub event: when a pull request is opened, and it's not a draft. A pull request run starts from that pull request's code, so the guard tests the change before I merge it.", "do": [{"k": "callout", "dur": 5.5, "target": "browser", "match": "Is draft = false", "big": True, "pos": "center", "label": "Ready PRs only"}]},
    {"say": "This needs the Claude GitHub App installed on the repository. The web page asks you to install it if it's missing.", "hold": 0.2},
    {"say": "Then an API trigger. I copy the fire URL, and generate a token.", "do": [dict(DETAIL, heading="Edit scheduled task", sub="Trigger", rows=[ON, {"name": "GitHub event", "icon": "G", "desc": "Pull request · opened · Is draft = false", "status": "✓ Added"}, {"name": "API", "icon": "A", "desc": "Fire URL: api.anthropic.com/v1/claude_code/routines/trig_01…/fire", "btn": "Generate token"}])]},
    {"say": "The token is shown only once. I store it straight away, in my deploy pipeline's secrets. Never in the repository.", "do": [{"k": "bmodal", "at": 0.3, "title": "Token generated", "lines": ["Copy this token now: it won't be shown again.", "`sk-ant-oat01-••••••••••••••••••••`"], "btns": ["Copy", "Done"]}, {"k": "callout", "at": 1.6, "dur": 4.0, "target": "browser", "match": "won't be shown again", "big": True, "label": "Shown once"}], "hold": 0.4}]},

  {"type": "screen", "project": "my-shop", "lines": [
    {"say": "Now my deploy script can start the routine. Here's the script.", "do": [{"k": "clear"}, {"k": "tree", "path": "scripts/"}, {"k": "open", "path": "scripts/fire-test-guard.sh", "at": 0.4}, {"k": "type", "at": 0.6, "path": "scripts/fire-test-guard.sh", "text": FIRE, "cps": 80}]},
    {"say": "A POST to the fire URL, with the token as a bearer header, and the routines beta header. Both come from secrets, not the file. The text field adds context, like which version just shipped.", "do": [{"k": "callout", "dur": 5.0, "target": "editor", "match": "Authorization: Bearer", "span": 2, "label": "Token + beta header"}]},
    {"say": "I run it after a deploy. The response is a new session, with a link to watch it live.", "do": [{"k": "cmd", "text": "bash scripts/fire-test-guard.sh v1.4.2", "out": ["{\"type\": \"routine_fire\",", " \"claude_code_session_id\": \"session_01HJK…\",", " \"claude_code_session_url\":", "   \"https://claude.ai/code/session_01HJK…\"}"]}, {"k": "callout", "at": 3.4, "dur": 4.5, "target": "term", "match": "claude_code_session_url", "span": 2, "label": "Watch the run live"}], "hold": 0.4},

    {"say": "Step five: check the runs. Here's what happened at 9:07 this morning.", "do": [{"k": "step", "n": 5}, {"k": "claude", "at": 0.8}]},
    {"say": "I ask Claude directly: what did my test guard do this morning? Claude reads the run's log, and explains.", "do": [{"k": "cprompt", "text": "/schedule what did my test guard do this morning?", "cps": 34}, {"k": "cout", "at": 0.4, "lines": ["b:Test guard · today 9:07 AM · run finished", "tool:Bash(python -m pytest -q)", "res:1 failed: test_shipping[50-0]", "ai:Cause: shipping() used total > 50, so an order of", "exactly 50 paid 4.99. Fixed to total >= 50.", "tool:Bash(python -m pytest -q)", "res:8 passed", "ai:Pushed branch claude/fix-free-shipping-at-50."], "dur": 2.6}]},
    {"say": "The test guard found the failing test, fixed the cause, ran the tests again, and pushed a claude branch. I just review it, and merge.", "do": [{"k": "callout", "dur": 5.5, "target": "term", "match": "Pushed branch claude/", "label": "Ready for my review"}]},
    {"say": "One warning: in the runs list, a green status only means the session started and exited. It doesn't mean the work succeeded. Always open the run, and read what Claude did.", "do": [{"k": "note", "dur": 8.0, "title": "Managing routines from the CLI", "rows": [["`/schedule list`", "see your routines"], ["`/schedule update`", "change one, or a cron"], ["`/schedule run`", "start one now"], ["green status", "≠ the work succeeded"]]}], "hold": 0.6}]},

  {"type": "cards", "chapter": "Tips", "kicker": "**TIPS** · Before you automate more", "heading": "4 tips for [[routines]]",
   "cards": [{"title": "Scope what it reaches", "text": "Only the repos, network and connectors it needs"},
             {"title": "Pick 9:07, not 9:00", "text": "On-the-hour runs can start minutes late"},
             {"title": "Treat fire text as data", "text": "Your prompt decides how to use the payload"},
             {"title": "Mind the limits", "text": "Min. 1 hour between runs; usage counts"}],
   "lines": [
    {"say": "Four tips before you automate more.", "do": [{"k": "show", "el": "heading"}]},
    {"say": "One: scope what it can reach. Runs have no permission prompts, so choose only the repositories, network access, and connectors the job needs.", "do": [{"k": "show", "el": "card1"}]},
    {"say": "Two: schedule a few minutes past the hour, because on-the-hour runs can start late.", "do": [{"k": "show", "el": "card2"}]},
    {"say": "Three: treat API text as data. It arrives labeled as untrusted, and your saved prompt decides how to use it.", "do": [{"k": "show", "el": "card3"}]},
    {"say": "And four: mind the limits. The minimum interval is one hour, and runs use your subscription, just like normal sessions. Slash schedule also needs a claude dot A I login, not an API key.", "tts": "And four: mind the limits. The minimum interval is one hour, and runs use your subscription, just like normal sessions. Slash schedule also needs a Claude dot A I login, not an API key.", "do": [{"k": "show", "el": "card4"}], "hold": 0.6}]},

  {"type": "checks", "chapter": "Recap", "heading": "Recap",
   "items": ["A routine = prompt + repos + connectors, run in the **cloud**",
             "Start it on a **schedule**, from an **API** call, or on a **GitHub** event",
             "Write a self-contained prompt, and [[scope what it can reach]]"],
   "lines": [
    {"say": "Let's recap.", "do": [{"k": "show", "el": "heading"}]},
    {"say": "A routine is a saved prompt, repositories, and connectors, that runs in the cloud, even with your laptop closed.", "do": [{"k": "show", "el": "item1"}]},
    {"say": "It starts on a schedule, from an API call, or on a GitHub event, or any mix of the three.", "do": [{"k": "show", "el": "item2"}]},
    {"say": "Write a prompt that works with nobody watching, give it only what it needs, and always read the runs.", "do": [{"k": "show", "el": "item3"}], "hold": 0.5}]},

  {"type": "outro", "title": "Thanks for [[watching]]", "subtitle": "The prompt, the fire script and a cheat sheet are in the description", "lines": [
    {"say": "The test guard prompt, the fire script, the demo project, and a cheat sheet are linked in the description.", "do": [{"k": "show", "el": "line1"}]},
    {"say": "If this helped, like the video, and subscribe to Zero Cost AI for more free AI tutorials. See you in the next one!", "do": [{"k": "show", "el": "line2"}], "hold": 1.5}]},
 ]}

(HERE / "script.json").write_text(json.dumps(script, indent=1, ensure_ascii=False), encoding="utf-8")
print("script.json written:", sum(len(s["lines"]) for s in script["scenes"]), "lines")
