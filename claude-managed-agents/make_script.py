"""Generates script.json for the Managed Agents vs your own agent tutorial from the real example files."""
import json, pathlib

HERE = pathlib.Path(__file__).parent
EX = HERE / "example-files" / "sales-report"
read = lambda f: (EX / f).read_text(encoding="utf-8")
SETUP, RUN, ORDERS = read("setup_agent.py"), read("run_report.py"), read("orders.csv")
s_env = SETUP.index("# The environment")
s_ids = SETUP.index("ids = {")
SETUP_AGENT, SETUP_ENV, SETUP_SAVE = SETUP[:s_env], SETUP[s_env:s_ids], SETUP[s_ids:]
r_task = RUN.index("TASK = (")
r_stream = RUN.index("# 2. Send the task")
r_dl = RUN.index("# 3. Download")
RUN_SESSION, RUN_TASK, RUN_STREAM, RUN_DL = RUN[:r_task], RUN[r_task:r_stream], RUN[r_stream:r_dl], RUN[r_dl:]

LOOP = 'while True:\n    response = client.messages.create(...)\n    if response.stop_reason != "tool_use":\n        break\n    # run each tool YOURSELF\n    # send back tool_result\n    # keep the history YOURSELF'

script = {
 "title": "claude-managed-agents",
 "steps": ["Define the agent", "Create the environment", "Start a session", "Stream the events", "Get the outputs"],
 "scenes": [
  {"type": "title", "chapter": "Introduction", "kicker": "Claude API tutorial · step by step",
   "title": "Claude Managed Agents\n[[vs Your Own Agent]]", "subtitle": "Which one to build, and how: a real example in Python",
   "lines": [
    {"say": "You want Claude to do real work: run code, create files, and keep going for minutes. Should you build the agent yourself, or let Anthropic run it for you?"},
    {"say": "In this video, you'll learn the difference between your own agent and Claude Managed Agents, when to choose each one, and how to build a Managed Agent, step by step.", "hold": 0.6}]},

  {"type": "bullets", "chapter": "What is an agent?", "kicker": "**01** · The concept", "heading": "What is an [[agent]]?",
   "items": ["Claude + **tools** + a **loop**: it acts, looks at the result, and acts again",
             "**Your own agent:** you write the loop and run every tool",
             "**Managed Agent:** Anthropic runs the loop, the tools and a sandbox"],
   "card": {"title": "YOUR OWN AGENT: THE LOOP YOU WRITE", "code": LOOP},
   "lines": [
    {"say": "First, what is an agent?", "do": [{"k": "show", "el": "heading"}]},
    {"say": "An agent is Claude, plus tools, plus a loop. Claude acts, looks at the result, and acts again, until the task is done.", "do": [{"k": "show", "el": "item1"}]},
    {"say": "With your own agent, you write that loop, like in my last video: you call the API, run each tool yourself, and keep the history.", "do": [{"k": "show", "el": "item2"}, {"k": "show", "el": "card", "at": 1.5}]},
    {"say": "With Claude Managed Agents, Anthropic runs the loop for you, with built-in tools, inside a secure cloud sandbox. It's in beta today.", "do": [{"k": "show", "el": "item3"}], "hold": 0.5}]},

  {"type": "rows", "chapter": "The four building blocks", "kicker": "**02** · How it works", "heading": "Managed Agents: [[4 building blocks]]",
   "rows": [{"label": "Agent", "text": "Model, system prompt, tools: created once, reused by ID"},
            {"label": "Environment", "text": "Where it runs: a cloud sandbox and its network rules"},
            {"label": "Session", "text": "One running agent, doing one task, with its own files"},
            {"label": "Events", "text": "You send messages; it streams back what it does"}],
   "lines": [
    {"say": "Managed Agents is built on four building blocks.", "do": [{"k": "show", "el": "heading"}]},
    {"say": "The agent: the model, the system prompt, and the tools. You create it once, and reuse it by its ID.", "do": [{"k": "show", "el": "row1"}]},
    {"say": "The environment: where the agent runs. A cloud sandbox, with the network rules you choose.", "do": [{"k": "show", "el": "row2"}]},
    {"say": "A session: one running agent, doing one task, with its own sandbox and files.", "do": [{"k": "show", "el": "row3"}]},
    {"say": "And events: you send messages as events, and the session streams back everything the agent does.", "do": [{"k": "show", "el": "row4"}], "hold": 0.5}]},

  {"type": "compare", "chapter": "Who does what", "kicker": "**03** · The difference", "heading": "Who does [[what]]?",
   "left": {"title": "Your own agent (Messages API)", "body": "• You write the loop\n• You run every tool, on your machine\n• You keep the message history\n• You handle retries and context\n• Full control of every step"},
   "right": {"title": "Claude Managed Agents", "body": "• Anthropic runs the loop\n• Built-in tools: bash, files,\n  web search, web fetch\n• Runs in a secure cloud sandbox\n• Sessions keep history and files\n• Caching and compaction built in"},
   "lines": [
    {"say": "So, who does what?", "do": [{"k": "show", "el": "heading"}]},
    {"say": "With your own agent, you do everything: the loop, running every tool on your machine, the message history, retries, and the context. In return, you control every step.", "do": [{"k": "show", "el": "left"}]},
    {"say": "With Managed Agents, Anthropic runs the loop. Claude gets built-in tools: bash, file tools, web search and web fetch, inside a cloud sandbox. Sessions keep the history and the files, and caching and compaction are built in.", "do": [{"k": "show", "el": "arrow"}, {"k": "show", "el": "right", "at": 0.4}], "hold": 0.5}]},

  {"type": "compare", "chapter": "When to choose each", "kicker": "**04** · When to use it", "heading": "When to choose [[each one]]",
   "left": {"title": "Build your own agent when…", "body": "• Tasks are short: ask, answer\n• You need a custom loop,\n  or approval at every step\n• Tools must run inside\n  your own systems\n• You need Zero Data Retention"},
   "right": {"title": "Use a Managed Agent when…", "body": "• Tasks run for minutes or hours\n• Claude must run code or\n  create files safely\n• Work is async or scheduled\n• You don't want to build\n  a loop, sandbox and tools"},
   "lines": [
    {"say": "When should you choose each one?", "do": [{"k": "show", "el": "heading"}]},
    {"say": "Build your own agent for short tasks, when you need a custom loop, when tools must run inside your own systems, or when you need Zero Data Retention. Managed Agents isn't eligible for it today, because sessions are stored server-side.", "do": [{"k": "show", "el": "left"}]},
    {"say": "Choose a Managed Agent for long tasks that run for minutes or hours, when Claude must run code or create files safely, for async or scheduled work, or when you just don't want to build the loop, the sandbox and the tools.", "do": [{"k": "show", "el": "arrow"}, {"k": "show", "el": "right", "at": 0.4}], "hold": 0.5}]},

  {"type": "compare", "chapter": "Our use case", "kicker": "**05** · Our use case", "heading": "A monthly [[sales report]]",
   "left": {"title": "The order bot (last video)", "body": "\"Where is order 1042?\"\n\n• One quick lookup\n• Seconds, one tool\n\n→ Your own agent is perfect"},
   "right": {"title": "The sales report (today)", "body": "\"Analyze October's orders,\n write a report and a chart\"\n\n• Writes and runs Python\n• Creates files, takes minutes\n\n→ A Managed Agent fits"},
   "lines": [
    {"say": "Here's our use case, from the same small shop as my last video.", "do": [{"k": "show", "el": "heading"}]},
    {"say": "The order bot answered one quick question, with one tool. Your own agent is perfect for that.", "do": [{"k": "show", "el": "left"}]},
    {"say": "Now I want a monthly sales report: analyze October's orders, write a report, and draw a chart. Claude has to write and run Python, and create files. That's a job for a Managed Agent.", "do": [{"k": "show", "el": "arrow"}, {"k": "show", "el": "right", "at": 0.4}], "hold": 0.5}]},

  {"type": "screen", "chapter": "Doing it yourself", "project": "sales-report", "kicker": "**DEMO** · Doing it yourself", "lines": [
    {"say": "Here's the data: twenty-four orders from October, in a CSV file.", "do": [{"k": "file", "path": "orders.csv", "text": ORDERS}]},
    {"say": "To do this with your own agent, you'd have to build a lot first.", "do": [{"k": "note", "dur": 12.5, "title": "With your own agent, you'd build…", "rows": [["a bash tool", "+ a safe place to run code"], ["file tools", "read, write, edit"], ["the loop", "that runs for minutes"], ["history + retries", "and somewhere to keep files"]]}]},
    {"say": "A bash tool, and a safe place to run Claude's code, because you don't want it running on your laptop. File tools. A loop that keeps going for minutes. History, retries, and somewhere to keep the files.", "hold": 0.3},
    {"say": "Managed Agents gives you all of that. Let's build it.", "hold": 0.4},

    {"say": "Step one: define the agent. I create setup agent dot p y.", "tts": "Step one: define the agent. I create setup agent dot P Y.", "do": [{"k": "step", "n": 1}, {"k": "open", "path": "setup_agent.py", "at": 1.6}]},
    {"say": "Client dot beta dot agents dot create: a name, the model, a system prompt, and the tools.", "do": [{"k": "type", "path": "setup_agent.py", "text": SETUP_AGENT, "cps": 60}]},
    {"say": "The system prompt says where to save outputs: in mnt, session, outputs. That folder matters later.", "do": [{"k": "callout", "dur": 4.5, "target": "editor", "match": "every output in /mnt/session/outputs/", "label": "Where outputs go"}]},
    {"say": "And this one line gives Claude the full agent toolset: bash, read, write, edit, glob, grep, web search and web fetch.", "do": [{"k": "callout", "dur": 5.0, "target": "editor", "match": "agent_toolset_20260401", "label": "All built-in tools"}], "hold": 0.4},

    {"say": "Step two: create the environment, where sessions run.", "do": [{"k": "step", "n": 2}]},
    {"say": "A cloud sandbox. Python, pandas and Matplotlib are already installed in it.", "do": [{"k": "type", "path": "setup_agent.py", "text": SETUP_ENV, "cps": 60}]},
    {"say": "I set networking to limited. If you leave it out, you get unrestricted network access. My agent doesn't need the internet, so I keep it closed.", "do": [{"k": "callout", "dur": 5.5, "target": "editor", "match": '"networking": {"type": "limited"}', "label": "No open internet"}]},
    {"say": "Then I save both IDs, and run the setup once. You create the agent and the environment once, and reuse them for every task.", "do": [{"k": "type", "path": "setup_agent.py", "text": SETUP_SAVE, "cps": 70}, {"k": "cmd", "at": 2.6, "text": "python setup_agent.py", "out": ["Agent: agent_01J8XkN5uT3vHpLqRfWdY2", "Environment: env_01K2mPsT7hNwR4jXuLvCqD8"]}], "hold": 0.4},

    {"say": "Step three: start a session. This is the part you run for each task.", "do": [{"k": "step", "n": 3}, {"k": "open", "path": "run_report.py", "at": 1.4}]},
    {"say": "I upload the CSV with the Files API, then create a session with my agent and environment, and mount the file inside the sandbox.", "do": [{"k": "type", "path": "run_report.py", "text": RUN_SESSION, "cps": 70}, {"k": "callout", "at": 3.6, "dur": 4.5, "target": "editor", "match": '"mount_path": "/orders.csv"', "label": "Mounted in the sandbox"}]},
    {"say": "Then the task, in plain English: the total revenue, revenue per week, the top three products, and a chart.", "do": [{"k": "type", "path": "run_report.py", "text": RUN_TASK, "cps": 70}], "hold": 0.4},

    {"say": "Step four: send the task, and stream the events.", "do": [{"k": "step", "n": 4}]},
    {"say": "I open the stream first, then send a user message event. For each event, I print the tools Claude uses, and its messages.", "do": [{"k": "type", "path": "run_report.py", "text": RUN_STREAM, "cps": 70}]},
    {"say": "When the session goes idle, the agent has stopped. Like stop reason in the Messages API, the idle event says why: end turn means it's done.", "do": [{"k": "callout", "dur": 5.5, "target": "editor", "match": '"session.status_idle"', "span": 3, "label": "Stopped: and why"}], "hold": 0.4},

    {"say": "Step five: get the outputs. Files the agent saves in the outputs folder can be listed for this session, and downloaded.", "do": [{"k": "step", "n": 5}, {"k": "type", "path": "run_report.py", "text": RUN_DL, "cps": 70}]},
    {"say": "I skip the CSV I uploaded, and wait a few seconds first, because the docs say outputs can appear just after the session goes idle.", "do": [{"k": "callout", "dur": 5.0, "target": "editor", "match": "time.sleep(5)", "label": "Outputs can lag a little"}]},
    {"say": "Now, let's run it, and watch the agent work.", "do": [{"k": "cmd", "text": "python run_report.py", "out": ["[tool] bash", "[tool] write", "[tool] bash", "[tool] write", "Total revenue: $499.80. Best week: Oct 12-18", "($147.45). Top products: Tote bag, Mug, T-shirt.", "report.md and weekly.png are saved in outputs.", "Idle: end_turn", "Downloaded report.md", "Downloaded weekly.png"]}]},
    {"say": "Claude wrote and ran Python in the sandbox, saved the report and the chart, and went idle with end turn. Then my script downloaded both files.", "do": [{"k": "callout", "dur": 5.5, "target": "term", "match": "Idle: end_turn", "span": 3, "label": "Done, files downloaded"}]},
    {"say": "Those numbers are real for this data. I checked them. Your agent's exact tool calls and wording will differ.", "do": [{"k": "tree", "path": "report.md", "at": 0.3}, {"k": "tree", "path": "weekly.png", "at": 0.5}], "hold": 0.6}]},

  {"type": "cards", "chapter": "Tips", "kicker": "**TIPS** · Before production", "heading": "4 tips for [[Managed Agents]]",
   "cards": [{"title": "Create once, reuse", "text": "One agent + environment, one session per task"},
             {"title": "Keep the network limited", "text": "Omit `networking` and you get unrestricted"},
             {"title": "Handle every idle reason", "text": "`end_turn`, `requires_action`, `budget_reached`"},
             {"title": "Mind the data rules", "text": "Sessions are stored: not ZDR or HIPAA eligible today"}],
   "lines": [
    {"say": "Four tips before production.", "do": [{"k": "show", "el": "heading"}]},
    {"say": "One: create the agent and the environment once, then start one session per task.", "do": [{"k": "show", "el": "card1"}]},
    {"say": "Two: always set networking. Limited is safer, and if you leave it out, the sandbox gets unrestricted access.", "do": [{"k": "show", "el": "card2"}]},
    {"say": "Three: handle every idle reason. End turn means done. Requires action means a custom tool, or a confirmation, needs your answer. Budget reached means the session hit its budget.", "do": [{"k": "show", "el": "card3"}]},
    {"say": "And four: sessions are stored server-side, so Managed Agents isn't eligible for Zero Data Retention or HIPAA today. You can delete sessions and files at any time.", "do": [{"k": "show", "el": "card4"}], "hold": 0.6}]},

  {"type": "checks", "chapter": "Recap", "heading": "Recap",
   "items": ["**Your own agent:** you run the loop and the tools, with full control",
             "**Managed Agent:** Anthropic runs the loop, tools and a sandbox",
             "Agent + environment once, then a [[session per task]]"],
   "lines": [
    {"say": "Let's recap.", "do": [{"k": "show", "el": "heading"}]},
    {"say": "With your own agent, you run the loop and the tools, and you control every step. Great for short, custom tasks.", "do": [{"k": "show", "el": "item1"}]},
    {"say": "With a Managed Agent, Anthropic runs the loop, the tools, and a sandbox. Great for long tasks that run code and create files.", "do": [{"k": "show", "el": "item2"}]},
    {"say": "Create the agent and environment once, then start a session for each task, stream its events, and download the outputs.", "do": [{"k": "show", "el": "item3"}], "hold": 0.5}]},

  {"type": "outro", "title": "Thanks for [[watching]]", "subtitle": "The code, an offline test and a cheat sheet are in the description", "lines": [
    {"say": "All the code, an offline test you can run without an API key, and a comparison cheat sheet are linked in the description.", "do": [{"k": "show", "el": "line1"}]},
    {"say": "If this helped, like the video, and subscribe to Zero Cost AI for more free AI tutorials. See you in the next one!", "do": [{"k": "show", "el": "line2"}], "hold": 1.5}]},
 ]}

(HERE / "script.json").write_text(json.dumps(script, indent=1, ensure_ascii=False), encoding="utf-8")
print("script.json written:", sum(len(s["lines"]) for s in script["scenes"]), "lines")
