"""Generates script.json for the Claude Code plugins tutorial from the real example files."""
import json, pathlib

HERE = pathlib.Path(__file__).parent
MKT = HERE / "example-files" / "my-marketplace"
KIT = MKT / "plugins" / "team-kit"
MANIFEST = (KIT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
HOOKS = (KIT / "hooks" / "hooks.json").read_text(encoding="utf-8")
MARKET = (MKT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8")
CART = (pathlib.Path(r"C:\Users\nadia\Desktop\youtube\claude-code-subagents\example-files\my-shop\cart.py")).read_text(encoding="utf-8").replace("if total > 100:", "if total >= 100:")
ENV = "API_KEY=sk-demo-1234\nDB_PASSWORD=change-me\n"

script = {
 "title": "claude-code-plugins",
 "steps": ["Create the plugin", "Add components", "Test it", "Share it", "Go further"],
 "scenes": [
  {"type": "title", "chapter": "Introduction", "kicker": "Claude Code tutorial · step by step",
   "title": "Claude Code Plugins\n[[Share Your Setup in One Install]]", "subtitle": "What plugins are, when to use them, and how to build and share one",
   "lines": [
    {"say": "You've built great tools for Claude Code: a hook, a subagent, a skill. Now your teammate wants them too."},
    {"say": "Copying files into every project by hand? There's a better way: plugins."},
    {"say": "I'll explain what a plugin is, when to use one, and then we'll build one and share it, step by step.", "hold": 0.6}]},

  {"type": "bullets", "chapter": "What is a plugin?", "kicker": "**01** · The concept", "heading": "What is a [[plugin]]?",
   "items": ["A **plugin** bundles skills, subagents, hooks and MCP servers into **one package**",
             "A small **manifest**, `plugin.json`, gives it a name and a description",
             "A **marketplace** is a catalog where people install it **by name**"],
   "card": {"title": "THE TEAM-KIT PLUGIN", "code": "team-kit/\n  .claude-plugin/plugin.json\n  skills/youtube-description/\n  agents/test-runner.md\n  hooks/hooks.json\n  scripts/protect_files.py"},
   "lines": [
    {"say": "So, what is a plugin?", "do": [{"k": "show", "el": "heading"}]},
    {"say": "A plugin bundles skills, subagents, hooks, and MCP servers into one package, that installs as one unit.", "do": [{"k": "show", "el": "item1"}, {"k": "show", "el": "card", "at": 1.0}]},
    {"say": "A small file called a manifest, plugin dot JSON, gives it a name and a description.", "do": [{"k": "show", "el": "item2"}]},
    {"say": "And a marketplace is a catalog, usually a Git repository, where people find your plugin and install it by name.", "do": [{"k": "show", "el": "item3"}], "hold": 0.5}]},

  {"type": "rows", "chapter": "How plugins work", "kicker": "**02** · How it works", "heading": "How a plugin [[works]]",
   "rows": [{"label": "Build", "text": "Put your components in one folder, with a manifest"},
            {"label": "List", "text": "Add it to a marketplace: a catalog in a Git repo"},
            {"label": "Install", "text": "One command, and every component loads"}],
   "banner": "✓ Components get the plugin's name as a prefix: /team-kit:youtube-description",
   "lines": [
    {"say": "Here's the whole journey, in three parts.", "do": [{"k": "show", "el": "heading"}]},
    {"say": "First, build: put your components in one folder, with a manifest.", "do": [{"k": "show", "el": "row1"}]},
    {"say": "Second, list it in a marketplace: a small catalog file in a Git repository.", "do": [{"k": "show", "el": "row2"}]},
    {"say": "Third, install: one command, and every component in the plugin loads in Claude Code.", "do": [{"k": "show", "el": "row3"}]},
    {"say": "Each skill and subagent gets the plugin's name as a prefix, so nothing clashes with your own tools.", "do": [{"k": "show", "el": "banner"}], "hold": 0.5}]},

  {"type": "compare", "chapter": "When to use a plugin", "kicker": "**03** · When to use it", "heading": "On its own vs. [[plugin]]",
   "left": {"title": "On its own (no plugin)", "body": "Just for you, set up once\n\n• A skill in ~/.claude/skills\n• A hook in your settings\n• Quick and simple"},
   "right": {"title": "Plugin", "body": "Several pieces, many people\n\n• One install for the whole kit\n• The same setup in every project\n• Updates from the marketplace"},
   "lines": [
    {"say": "So when do you need a plugin?", "do": [{"k": "show", "el": "heading"}]},
    {"say": "Skills, subagents, hooks, and MCP servers all work on their own. If it's one tool, just for you, you don't need a plugin.", "do": [{"k": "show", "el": "left"}]},
    {"say": "Use a plugin when you want several pieces packaged together: to share with teammates, reuse in many projects, or ship updates.", "do": [{"k": "show", "el": "arrow"}, {"k": "show", "el": "right", "at": 0.4}], "hold": 0.5}]},

  {"type": "compare", "chapter": "Our example", "kicker": "**04** · Our example", "heading": "A [[team kit]] plugin",
   "left": {"title": "Tools from earlier videos", "code": "protect_files.py   a hook\ntest-runner.md     a subagent\nyoutube-description  a skill\n\n3 setups, copied by hand\ninto every project"},
   "right": {"title": "The team-kit plugin", "body": "**One install** for the whole team\n\n`/plugin install team-kit@my-marketplace`\n\n→ the hook, the subagent and the skill,\n   ready in every project"},
   "lines": [
    {"say": "Our example: a team kit.", "do": [{"k": "show", "el": "heading"}]},
    {"say": "In earlier videos, we built a hook that protects your secrets, a test-runner subagent, and a YouTube description skill. Sharing them means copying files, project by project.", "do": [{"k": "show", "el": "left"}]},
    {"say": "We'll pack all three into one plugin, called team-kit, so anyone can install everything with a single command.", "do": [{"k": "show", "el": "arrow"}, {"k": "show", "el": "right", "at": 0.5}], "hold": 0.6}]},

  {"type": "screen", "project": "my-shop", "kicker": "**DEMO** · Build the plugin", "lines": [
    {"say": "Step one: create the plugin.", "do": [{"k": "step", "n": 1}, {"k": "file", "path": ".env", "text": ENV, "open": False}, {"k": "file", "path": "tests/test_cart.py", "text": "# 30 tests\n", "open": False}, {"k": "file", "path": "cart.py", "text": CART}]},
    {"say": "I'm in my project. I make a folder called team-kit, with a dot claude plugin folder inside it.", "tts": "I'm in my project. I make a folder called team-kit, with a dot claude dash plugin folder inside it.", "do": [{"k": "cmd", "text": "mkdir -p team-kit/.claude-plugin", "cps": 20}, {"k": "open", "path": "team-kit/.claude-plugin/plugin.json", "at": 2.4}]},
    {"say": "Inside, the manifest: plugin dot JSON.", "do": [{"k": "type", "path": "team-kit/.claude-plugin/plugin.json", "text": MANIFEST, "cps": 40}]},
    {"say": "The name is required. It becomes the prefix on every skill and subagent in the plugin. No spaces.", "do": [{"k": "callout", "dur": 5.0, "target": "editor", "match": "\"name\"", "label": "Becomes the prefix"}]},
    {"say": "The description is what people see when they browse plugins. And the version lets you release updates.", "do": [{"k": "callout", "dur": 3.6, "target": "editor", "match": "\"description\"", "label": "Shown in /plugin"}, {"k": "callout", "at": 3.8, "dur": 3.0, "target": "editor", "match": "\"version\"", "label": "For updates"}]},
    {"say": "Only plugin dot JSON goes in that hidden folder. Everything else goes next to it.", "do": [{"k": "callout", "dur": 4.0, "target": "tree", "match": ".claude-plugin", "label": "Manifest only"}], "hold": 0.3},

    {"say": "Step two: add the components.", "do": [{"k": "step", "n": 2}]},
    {"say": "Each type has its own folder: agents, hooks, scripts, and skills.", "do": [{"k": "cmd", "text": "mkdir -p team-kit/agents team-kit/hooks team-kit/scripts team-kit/skills", "cps": 34}]},
    {"say": "I copy in the three tools from earlier videos: the subagent, the hook script, and the skill.", "do": [
        {"k": "cmd", "text": "cp ~/my-tools/test-runner.md team-kit/agents/", "cps": 34},
        {"k": "tree", "at": 1.6, "path": "team-kit/agents/test-runner.md"},
        {"k": "cmd", "at": 1.8, "text": "cp ~/my-tools/protect_files.py team-kit/scripts/", "cps": 34},
        {"k": "tree", "at": 3.5, "path": "team-kit/scripts/protect_files.py"},
        {"k": "cmd", "at": 3.7, "text": "cp -r ~/my-tools/youtube-description team-kit/skills/", "cps": 34},
        {"k": "tree", "at": 5.4, "path": "team-kit/skills/youtube-description/SKILL.md"}]},
    {"say": "The hook needs one file: hooks, slash hooks dot JSON. It's the same format as the hooks section in a settings file.", "do": [{"k": "type", "path": "team-kit/hooks/hooks.json", "text": HOOKS, "cps": 44}]},
    {"say": "One difference: the script path starts with the plugin root variable. It always points to wherever the plugin is installed.", "do": [{"k": "callout", "dur": 6.5, "target": "editor", "match": "CLAUDE_PLUGIN_ROOT", "label": "Wherever the plugin is installed"}], "hold": 0.4},

    {"say": "Step three: test it, before sharing.", "do": [{"k": "step", "n": 3}, {"k": "clear"}]},
    {"say": "First, claude plugin validate checks the manifest and every component.", "do": [{"k": "cmd", "text": "claude plugin validate ./team-kit", "cps": 22, "out": ["Validating plugin manifest: team-kit/.claude-plugin/plugin.json", "", "✔ Validation passed"]}, {"k": "callout", "at": 2.8, "dur": 3.5, "target": "term", "match": "Validation passed", "label": "Ready"}]},
    {"say": "Then I load it for one session with the plugin dir flag. No install needed while you're building.", "do": [{"k": "cmd", "text": "claude --plugin-dir ./team-kit", "cps": 20}, {"k": "claude", "at": 2.0}]},
    {"say": "Let's try the hook. I ask Claude to add a comment to my dot env file.", "do": [{"k": "cprompt", "text": "Add a comment at the top of .env", "cps": 24}, {"k": "cout", "at": 1.4, "lines": ["tool:Edit(.env)", "res:Blocked by PreToolUse hook:", "res:Blocked: my-shop/.env is protected."], "dur": 1.0}, {"k": "callout", "at": 2.6, "dur": 4.0, "target": "term", "match": "Blocked by PreToolUse", "span": 2, "label": "The plugin's hook"}]},
    {"say": "Blocked, by the hook inside the plugin. Now, the subagent: run the tests.", "do": [{"k": "cprompt", "at": 1.8, "text": "Run the tests", "cps": 16}]},
    {"say": "Claude delegates to team-kit colon test-runner. Notice the plugin's name, as a prefix.", "do": [{"k": "cout", "lines": ["tool:team-kit:test-runner(Run the test suite)", "res:Done", "ai:All 30 tests pass."], "dur": 1.0}, {"k": "callout", "at": 1.2, "dur": 4.5, "target": "term", "match": "team-kit:test-runner", "label": "The plugin's subagent"}]},
    {"say": "And the skill is ready too, as slash team-kit colon youtube-description. Everything works. Time to share it.", "do": [{"k": "note", "dur": 6.5, "title": "What team-kit adds", "rows": [["Hook", "blocks edits to .env"], ["Subagent", "team-kit:test-runner"], ["Skill", "/team-kit:youtube-description"]]}], "hold": 0.4},

    {"say": "Step four: share it, with a marketplace.", "do": [{"k": "step", "n": 4}, {"k": "clear"}]},
    {"say": "A marketplace is just a folder with a catalog file, and your plugins inside. I create one, and copy team-kit into it.", "do": [{"k": "cmd", "text": "mkdir -p my-marketplace/.claude-plugin my-marketplace/plugins", "cps": 34}, {"k": "cmd", "at": 2.4, "text": "cp -r team-kit my-marketplace/plugins/", "cps": 30}, {"k": "tree", "at": 4.0, "path": "my-marketplace/plugins/team-kit/"}]},
    {"say": "The catalog is marketplace dot JSON: a name, an owner, and the list of plugins.", "do": [{"k": "type", "path": "my-marketplace/.claude-plugin/marketplace.json", "text": MARKET, "cps": 46}]},
    {"say": "Each plugin entry has a name, and a source: the path to the plugin, from the marketplace folder.", "do": [{"k": "callout", "dur": 5.0, "target": "editor", "match": "\"source\"", "label": "Where the plugin lives"}]},
    {"say": "I validate it, then push the my-marketplace folder to GitHub, as its own repository.", "do": [{"k": "cmd", "text": "claude plugin validate ./my-marketplace", "cps": 24, "out": ["Validating marketplace manifest: my-marketplace/.claude-plugin/marketplace.json", "", "✔ Validation passed"]}]},
    {"say": "Now, any teammate runs two commands. Add the marketplace, using the GitHub owner and repository name.", "do": [{"k": "clear", "at": 0.3}, {"k": "cmd", "at": 0.4, "text": "claude plugin marketplace add your-name/my-marketplace", "cps": 30, "out": ["✔ Successfully added marketplace: my-marketplace (declared in user settings)"]}]},
    {"say": "Then install the plugin: its name, at, the marketplace name.", "do": [{"k": "cmd", "text": "claude plugin install team-kit@my-marketplace", "cps": 26, "out": ["✔ Successfully installed plugin: team-kit@my-marketplace (scope: user)"]}, {"k": "callout", "at": 2.6, "dur": 4.5, "target": "term", "match": "Successfully installed", "label": "Whole kit, one install"}]},
    {"say": "That's it. The hook, the subagent, and the skill, in every project, from one install.", "hold": 0.6}]},

  {"type": "cards", "kicker": "**STEP 5** · Go further", "heading": "4 tips for [[using plugins]]", "rail": True,
   "cards": [{"title": "Browse with /plugin", "text": "The Discover tab lists Anthropic's official plugins"},
             {"title": "Check the cost", "text": "`claude plugin details` shows tokens added per session"},
             {"title": "Trust before you install", "text": "A plugin runs code as you: review it first"},
             {"title": "Ship updates", "text": "Bump the version, teammates get the new release"}],
   "lines": [
    {"say": "Step five: go further. Here are four tips.", "do": [{"k": "step", "n": 5}, {"k": "show", "el": "heading"}]},
    {"say": "One: type slash plugin in Claude Code. The Discover tab lists plugins from Anthropic's official marketplace, ready to install.", "do": [{"k": "show", "el": "card1"}]},
    {"say": "Two: check the cost. An enabled plugin adds its descriptions to every session. Claude plugin details shows how many tokens. Our team-kit adds about ninety.", "do": [{"k": "show", "el": "card2"}]},
    {"say": "Three: only install plugins you trust. A plugin runs code with your permissions, so review it first.", "do": [{"k": "show", "el": "card3"}]},
    {"say": "Four: when you improve your plugin, bump the version in the manifest, and your teammates get the update.", "do": [{"k": "show", "el": "card4"}], "hold": 0.6}]},

  {"type": "checks", "chapter": "Recap", "heading": "Recap",
   "items": ["A plugin = skills, subagents, hooks and MCP servers in **one package**",
             "`plugin.json` + component folders · test with `--plugin-dir`",
             "Share it through a [[marketplace]], install with one command"],
   "lines": [
    {"say": "Let's recap.", "do": [{"k": "show", "el": "heading"}]},
    {"say": "A plugin packages skills, subagents, hooks, and MCP servers into one unit.", "do": [{"k": "show", "el": "item1"}]},
    {"say": "You build it with a plugin dot JSON manifest and a folder per component, and test it with the plugin dir flag.", "do": [{"k": "show", "el": "item2"}]},
    {"say": "And you share it through a marketplace, so anyone can install the whole kit with one command.", "do": [{"k": "show", "el": "item3"}], "hold": 0.5}]},

  {"type": "outro", "title": "Thanks for [[watching]]", "subtitle": "The team-kit plugin and marketplace are in the description", "lines": [
    {"say": "The team-kit plugin and the marketplace from this video are linked in the description. Copy them, and make them yours.", "do": [{"k": "show", "el": "line1"}]},
    {"say": "If this helped, like the video, and subscribe to Zero Cost AI for more free AI tutorials. See you in the next one!", "do": [{"k": "show", "el": "line2"}], "hold": 1.5}]},
 ]}

(HERE / "script.json").write_text(json.dumps(script, indent=1, ensure_ascii=False), encoding="utf-8")
print("script.json written:", sum(len(s["lines"]) for s in script["scenes"]), "lines")
