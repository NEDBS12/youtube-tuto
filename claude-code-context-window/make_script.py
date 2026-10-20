"""Generates script.json for the Claude Code context window tutorial from the real example files."""
import json, pathlib

HERE = pathlib.Path(__file__).parent
CLAUDEMD = (HERE / "example-files" / "my-shop" / "CLAUDE.md").read_text(encoding="utf-8")
ci = CLAUDEMD.index("# Compact instructions")
MD_RULES, MD_COMPACT = CLAUDEMD[:ci], CLAUDEMD[ci:]
CART = pathlib.Path(r"C:\Users\nadia\Desktop\youtube\claude-code-subagents\example-files\my-shop\cart.py").read_text(encoding="utf-8").replace("if total > 100:", "if total >= 100:")

LONG = ["tool:Read(cart.py)", "res:Read 15 lines", "tool:Bash(python -m pytest -q)", "res:30 passed",
        "tool:Read(tests/test_cart.py)", "res:Read 55 lines", "tool:Edit(cart.py)", "res:Updated cart.py",
        "res:… 2 hours, 40 file reads, 15 test runs later …"]

script = {
 "title": "claude-code-context-window",
 "steps": ["See what's inside", "Save lasting rules", "Compact with a focus", "Clear between tasks", "Go further"],
 "scenes": [
  {"type": "title", "chapter": "Introduction", "kicker": "Claude Code tutorial · step by step",
   "title": "The Context Window\n[[Claude's Working Memory]]", "subtitle": "What it is, why it fills up, and how to manage it in Claude Code",
   "lines": [
    {"say": "Have you ever had a long Claude Code session, where Claude suddenly forgot something you told it at the start?"},
    {"say": "That's the context window at work. In this video, you'll learn what it is, and how to manage it like a pro."},
    {"say": "I'll explain how it works, when it causes problems, and then show you four practical habits, step by step.", "hold": 0.6}]},

  {"type": "bullets", "chapter": "What is the context window?", "kicker": "**01** · The concept", "heading": "What is the [[context window]]?",
   "items": ["Everything Claude can **see right now**: your messages, files it read, command output",
             "Plus what loads **automatically**: instructions, `CLAUDE.md`, memory, skill and tool names",
             "It has a **limit**, measured in tokens: 200,000 on most models"],
   "card": {"title": "A SESSION'S CONTEXT WINDOW", "code": "██        instructions + tools\n█         CLAUDE.md + memory\n█         skill descriptions\n████████  conversation + files\n░░░░░░░░  free space"},
   "lines": [
    {"say": "So, what is the context window?", "do": [{"k": "show", "el": "heading"}]},
    {"say": "It's Claude's working memory. Everything Claude can see right now: your messages, the files it read, and the output of the commands it ran.", "do": [{"k": "show", "el": "item1"}, {"k": "show", "el": "card", "at": 1.2}]},
    {"say": "Some things load automatically, before you even type: Claude Code's instructions, your CLAUDE.md file, memory, and the names of your skills and tools.", "tts": "Some things load automatically, before you even type: Claude Code's instructions, your CLAUDE dot M D file, memory, and the names of your skills and tools.", "do": [{"k": "show", "el": "item2"}]},
    {"say": "And it has a limit, measured in tokens. Most models give you two hundred thousand tokens. Some offer up to a million.", "do": [{"k": "show", "el": "item3"}], "hold": 0.5}]},

  {"type": "compare", "chapter": "What is a token?", "kicker": "**02** · Tokens", "heading": "What fills it [[fastest]]",
   "left": {"title": "What is a token?", "body": "A small piece of text:\na short word, or part of one\n\n200,000 tokens\n≈ a few hundred pages of text"},
   "right": {"title": "What uses the most space", "body": "• Big files Claude reads\n• Long command output: tests, logs\n• Long back-and-forth conversations\n• Plugins, MCP servers and skills\n  you don't use"},
   "lines": [
    {"say": "A token is a small piece of text: a short word, or part of a longer one. Two hundred thousand tokens is roughly a few hundred pages.", "do": [{"k": "show", "el": "heading"}, {"k": "show", "el": "left", "at": 0.8}]},
    {"say": "That sounds like a lot. But big files, long test output, and long conversations fill it up surprisingly fast.", "do": [{"k": "show", "el": "arrow"}, {"k": "show", "el": "right", "at": 0.4}], "hold": 0.5}]},

  {"type": "rows", "chapter": "What happens when it fills up", "kicker": "**03** · How it works", "heading": "When the window [[fills up]]",
   "rows": [{"label": "It fills as you work", "text": "Every file read and command output takes space"},
            {"label": "Claude Code compacts automatically", "text": "Old tool output is cleared, then the chat is summarized"},
            {"label": "Some details get lost", "text": "Instructions from early in the chat may not survive"}],
   "banner": "✓ Rules that must last belong in CLAUDE.md, not in the chat",
   "lines": [
    {"say": "Here's what happens as you work.", "do": [{"k": "show", "el": "heading"}]},
    {"say": "First, the window fills up. Every file read, and every command output, takes space.", "do": [{"k": "show", "el": "row1"}]},
    {"say": "Second, near the limit, Claude Code compacts automatically. It clears older tool output first, then summarizes the conversation. So your session keeps going.", "do": [{"k": "show", "el": "row2"}]},
    {"say": "But third: a summary is shorter than the original. Detailed instructions from early in the chat can get lost.", "do": [{"k": "show", "el": "row3"}]},
    {"say": "That's why rules that must last belong in a CLAUDE.md file, not just in the chat.", "tts": "That's why rules that must last belong in a CLAUDE dot M D file, not just in the chat.", "do": [{"k": "show", "el": "banner"}], "hold": 0.5}]},

  {"type": "screen", "chapter": "The long-session problem", "project": "my-shop", "kicker": "**DEMO** · The long-session problem", "lines": [
    {"say": "Let's see the problem. At the start of this session, I told Claude: always run the tests after every change.", "do": [{"k": "file", "path": "cart.py", "text": CART}, {"k": "claude"}, {"k": "cprompt", "at": 2.2, "text": "Always run the tests after every change", "cps": 30}]},
    {"say": "Two hours later, after dozens of file reads and test runs, the context window is getting full.", "do": [{"k": "cout", "lines": LONG, "dur": 3.0}]},
    {"say": "Now I ask for another change. Claude edits the file, and stops. No tests. After compaction, my early instruction didn't survive.", "do": [{"k": "cprompt", "text": "Make shipping free from 40 instead of 50", "cps": 30}, {"k": "cout", "at": 1.6, "lines": ["tool:Edit(cart.py)", "res:Updated cart.py", "ai:Done: shipping is now free from 40."], "dur": 1.0}, {"k": "callout", "at": 3.0, "dur": 5.0, "target": "term", "match": "Done: shipping", "label": "Forgot to run the tests"}]},
    {"say": "Let's fix that, with four simple habits.", "hold": 0.4},

    {"say": "Habit one: see what's inside your context window.", "do": [{"k": "step", "n": 1}]},
    {"say": "Type slash context. You get a live breakdown of what's using space, by category, with suggestions.", "do": [{"k": "cprompt", "text": "/context", "cps": 12}, {"k": "cout", "at": 0.4, "lines": ["b:Context usage   142k / 200k tokens (71%)", "System prompt + tools    16k", "Memory files (CLAUDE.md)  1k", "Skills                    1k", "Messages                124k", "Free space               58k"], "dur": 1.6}]},
    {"say": "Here, the conversation itself is by far the biggest part: all those file reads and test runs.", "do": [{"k": "callout", "dur": 5.0, "target": "term", "match": "Messages", "label": "The conversation"}]},
    {"say": "The numbers in your own session will be different. The point is to check, before the window fills up.", "hold": 0.4},

    {"say": "Habit two: save lasting rules in CLAUDE.md.", "tts": "Habit two: save lasting rules in CLAUDE dot M D.", "do": [{"k": "step", "n": 2}, {"k": "open", "path": "CLAUDE.md", "at": 0.6}]},
    {"say": "CLAUDE.md is loaded at the start of every session. And after compaction, Claude Code reloads it from disk. So rules here don't get lost.", "tts": "CLAUDE dot M D is loaded at the start of every session. And after compaction, Claude Code reloads it from disk. So rules here don't get lost.", "do": [{"k": "type", "path": "CLAUDE.md", "text": MD_RULES, "cps": 40}]},
    {"say": "I move my test rule here, plus a couple of others I always want.", "do": [{"k": "callout", "dur": 4.5, "target": "editor", "match": "After every code change", "span": 3, "label": "Rules that always apply"}]},
    {"say": "And I add a Compact instructions section. It tells Claude what to keep when it summarizes: test output, code changes, and failing tests.", "do": [{"k": "type", "path": "CLAUDE.md", "text": MD_COMPACT, "cps": 40}, {"k": "callout", "at": 3.6, "dur": 4.5, "target": "editor", "match": "# Compact instructions", "span": 3, "label": "What to keep when compacting"}], "hold": 0.4},

    {"say": "Habit three: compact with a focus.", "do": [{"k": "step", "n": 3}]},
    {"say": "Claude Code compacts on its own near the limit. But before a big new step, you can do it yourself, and say what matters.", "do": [{"k": "cprompt", "text": "/compact focus on the discount bug fix", "cps": 24}]},
    {"say": "The summary keeps what you chose, instead of what the automatic pass guesses is important. And you get lots of free space back.", "do": [{"k": "cout", "lines": ["res:Conversation compacted", "res:Kept: the discount bug fix, files changed, test results"], "dur": 1.0}, {"k": "callout", "at": 1.4, "dur": 5.0, "target": "term", "match": "Kept: the discount", "label": "You choose what stays"}], "hold": 0.4},

    {"say": "Habit four: clear between tasks.", "do": [{"k": "step", "n": 4}]},
    {"say": "When you switch to unrelated work, old conversation just gets in the way, and costs tokens on every message.", "do": [{"k": "cprompt", "text": "/rename discount-fix", "cps": 18}]},
    {"say": "So I give this session a name with slash rename, then type slash clear, to start fresh.", "do": [{"k": "cprompt", "text": "/clear", "cps": 10}, {"k": "clear", "at": 1.2}, {"k": "claude", "at": 1.3}]},
    {"say": "A clean context window, for the next task. And I can come back to the old session any time, with slash resume.", "do": [{"k": "note", "dur": 6.0, "title": "Four habits", "rows": [["`/context`", "see what's using space"], ["`CLAUDE.md`", "rules that must last"], ["`/compact focus on …`", "keep what matters"], ["`/clear`", "fresh start between tasks"]]}]},
    {"say": "Now, with the rule in CLAUDE.md, the same request ends the right way: Claude edits the file, and runs the tests.", "tts": "Now, with the rule in CLAUDE dot M D, the same request ends the right way: Claude edits the file, and runs the tests.", "do": [{"k": "cprompt", "text": "Make shipping free from 40 instead of 50", "cps": 30}, {"k": "cout", "at": 1.6, "lines": ["tool:Edit(cart.py)", "res:Updated cart.py", "tool:Bash(python -m pytest -q)", "res:1 failed, 29 passed", "ai:Shipping is now free from 40. One shipping test (49.99) still expects a shipping fee: should I update it?"], "dur": 2.0}, {"k": "callout", "at": 4.0, "dur": 5.0, "target": "term", "match": "Bash(python -m pytest", "label": "Tests run every time"}], "hold": 0.6}]},

  {"type": "cards", "kicker": "**STEP 5** · Go further", "heading": "4 tips to [[save context]]", "rail": True,
   "cards": [{"title": "Delegate big jobs", "text": "Subagents keep long output in their own context"},
             {"title": "Trim always-on extras", "text": "Disable plugins and MCP servers you don't use"},
             {"title": "Check before it's full", "text": "Run `/context` during long sessions"},
             {"title": "Need more room?", "text": "Some models support a 1 million token window"}],
   "lines": [
    {"say": "Step five: go further. Four more tips.", "do": [{"k": "step", "n": 5}, {"k": "show", "el": "heading"}]},
    {"say": "One: delegate big jobs, like test runs or research, to a subagent. The long output stays in its own context window, not yours.", "do": [{"k": "show", "el": "card1"}]},
    {"say": "Two: disable plugins and MCP servers you don't use. Their descriptions load into every session.", "do": [{"k": "show", "el": "card2"}]},
    {"say": "Three: run slash context during long sessions, before the window fills up.", "do": [{"k": "show", "el": "card3"}]},
    {"say": "And four: if you really need more room, some models support a one million token context window.", "do": [{"k": "show", "el": "card4"}], "hold": 0.6}]},

  {"type": "checks", "chapter": "Recap", "heading": "Recap",
   "items": ["The context window = everything Claude can see **right now**",
             "When it fills up, Claude Code compacts, and early details can get lost",
             "`/context` · `CLAUDE.md` · `/compact` · `/clear`: [[four habits]]"],
   "lines": [
    {"say": "Let's recap.", "do": [{"k": "show", "el": "heading"}]},
    {"say": "The context window is Claude's working memory: everything it can see right now.", "do": [{"k": "show", "el": "item1"}]},
    {"say": "When it fills up, Claude Code compacts the conversation, and early details can get lost.", "do": [{"k": "show", "el": "item2"}]},
    {"say": "So check it with slash context, keep lasting rules in CLAUDE.md, compact with a focus, and clear between tasks.", "tts": "So check it with slash context, keep lasting rules in CLAUDE dot M D, compact with a focus, and clear between tasks.", "do": [{"k": "show", "el": "item3"}], "hold": 0.5}]},

  {"type": "outro", "title": "Thanks for [[watching]]", "subtitle": "The CLAUDE.md example and a cheat sheet are in the description", "lines": [
    {"say": "The CLAUDE.md example and a one-page cheat sheet are linked in the description.", "tts": "The CLAUDE dot M D example and a one-page cheat sheet are linked in the description.", "do": [{"k": "show", "el": "line1"}]},
    {"say": "If this helped, like the video, and subscribe to Zero Cost AI for more free AI tutorials. See you in the next one!", "do": [{"k": "show", "el": "line2"}], "hold": 1.5}]},
 ]}

(HERE / "script.json").write_text(json.dumps(script, indent=1, ensure_ascii=False), encoding="utf-8")
print("script.json written:", sum(len(s["lines"]) for s in script["scenes"]), "lines")
