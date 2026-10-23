"""Generates script.json for the MCP server + client tutorial from the real example files."""
import json, pathlib

HERE = pathlib.Path(__file__).parent
EX = HERE / "example-files" / "mugs-mcp"
read = lambda f: (EX / f).read_text(encoding="utf-8")
SERVER, CLIENT, ORDERS = read("mugs_server.py"), read("client.py"), read("orders.json")
s2 = SERVER.index("# 2. A resource")
SV1, SV2 = SERVER[:s2], SERVER[s2:]
ORDER_1042 = "Order 1042 for Priya: Teapot (Slate), shipped, arriving Oct 25."

script = {
 "title": "claude-mcp",
 "steps": ["Build the server", "Build a client", "Run it", "Connect Claude Code"],
 "scenes": [
  {"type": "title", "chapter": "Introduction", "kicker": "Model Context Protocol · step by step",
   "title": "MCP Server & MCP Client\n[[Connect Claude to your data]]", "subtitle": "What they are, when to use each one, and a real example in Python",
   "lines": [
    {"say": "Claude can write code and answer questions. But it can't see your orders, your database, or your own tools."},
    {"say": "MCP fixes that. In this video, you'll learn what an MCP server and an MCP client are, and when to build each one."},
    {"say": "Then we'll build a real MCP server and a real client in Python, and connect the server to Claude Code.", "hold": 0.6}]},

  {"type": "bullets", "chapter": "What is MCP?", "kicker": "**01** · The concept", "heading": "What is [[MCP]]?",
   "items": ["An **open standard** that connects AI apps to data and tools",
             "**MCP server:** a program that **offers** tools and data",
             "**MCP client:** the connector **inside the AI app**, one per server"],
   "card": {"title": "ONE HOST, ONE CLIENT PER SERVER", "code": "Claude Code (the host)\n ├─ client ──▶ maple-mugs server\n ├─ client ──▶ GitHub server\n └─ client ──▶ Notion server"},
   "lines": [
    {"say": "So, what is MCP?", "do": [{"k": "show", "el": "heading"}]},
    {"say": "MCP, the Model Context Protocol, is an open standard that connects AI apps to data and tools. The official docs compare it to a USB-C port for AI apps: one standard plug, for everything.", "tts": "M C P, the Model Context Protocol, is an open standard that connects AI apps to data and tools. The official docs compare it to a USB-C port for AI apps: one standard plug, for everything.", "do": [{"k": "show", "el": "item1"}]},
    {"say": "An MCP server is a program that offers things to the AI: tools it can call, and data it can read.", "tts": "An M C P server is a program that offers things to the AI: tools it can call, and data it can read.", "do": [{"k": "show", "el": "item2"}]},
    {"say": "An MCP client is the connector inside the AI app. The app, called the host, creates one client for each server it connects to.", "tts": "An M C P client is the connector inside the AI app. The app, called the host, creates one client for each server it connects to.", "do": [{"k": "show", "el": "item3"}, {"k": "show", "el": "card", "at": 2.0}], "hold": 0.5}]},

  {"type": "rows", "chapter": "How it works", "kicker": "**02** · How it works", "heading": "Host, client, [[server]]",
   "rows": [{"label": "Host", "text": "The AI app: **Claude Code**, Claude Desktop, VS Code…"},
            {"label": "Server offers", "text": "**Tools** (actions), **resources** (data), **prompts** (templates)"},
            {"label": "Transport", "text": "**stdio**: local, on your machine · **HTTP**: remote"}],
   "banner": "Build a server once → every MCP app can use it",
   "lines": [
    {"say": "Here's how the pieces fit together.", "do": [{"k": "show", "el": "heading"}]},
    {"say": "The host is the AI app you use, like Claude Code, Claude Desktop, or VS Code.", "do": [{"k": "show", "el": "row1"}]},
    {"say": "A server offers three kinds of things: tools, which are actions the AI can call; resources, which is read-only data; and prompts, which are ready-made templates.", "do": [{"k": "show", "el": "row2"}]},
    {"say": "They talk over a transport. With stdio, the client starts the server as a program on your own machine. With Streamable HTTP, the server runs remotely, on the internet.", "tts": "They talk over a transport. With standard I O, the client starts the server as a program on your own machine. With Streamable H T T P, the server runs remotely, on the internet.", "do": [{"k": "show", "el": "row3"}]},
    {"say": "And that's the big idea: you build a server once, and every app that speaks MCP can use it.", "do": [{"k": "show", "el": "banner"}], "hold": 0.5}]},

  {"type": "cards", "chapter": "When to use each one", "kicker": "**03** · When to use it", "heading": "Server, client, or [[neither]]?",
   "cards": [{"title": "Build a server", "text": "Your data or tool should work in **many AI apps**"},
             {"title": "Build a client", "text": "**Your own AI app** should use existing servers"},
             {"title": "Add an existing server", "text": "GitHub, Notion, Sentry: **no code needed**"},
             {"title": "Skip MCP", "text": "One script, one app → plain **tool use** is simpler"}],
   "lines": [
    {"say": "So when do you build what?", "do": [{"k": "show", "el": "heading"}]},
    {"say": "Build an MCP server when your data or your tool should work in many AI apps: Claude Code, Claude Desktop, VS Code, and others, without writing one integration for each.", "do": [{"k": "show", "el": "card1"}]},
    {"say": "Build an MCP client when you're making your own AI app or agent, and you want it to use servers that already exist.", "do": [{"k": "show", "el": "card2"}]},
    {"say": "If a server already exists, for GitHub, Notion or Sentry for example, you don't build anything. You just add it.", "do": [{"k": "show", "el": "card3"}]},
    {"say": "And if it's one script, in one app, with one or two tools, skip MCP. Plain tool use in the Claude API is simpler.", "do": [{"k": "show", "el": "card4"}], "hold": 0.6}]},

  {"type": "compare", "chapter": "Our use case", "kicker": "**04** · Our use case", "heading": "Order lookups for [[Maple Mugs]]",
   "left": {"title": "Without MCP", "body": "\"Where is order 1042?\"\n\nClaude can't reach the\norders database: you look\nit up and copy-paste\n\n✗ Every time"},
   "right": {"title": "With an MCP server", "body": "maple-mugs server\n→ get_order tool\n\nClaude calls it, and\nanswers directly\n\n✓ In any MCP app"},
   "lines": [
    {"say": "Our use case: Maple Mugs, the small online shop from my earlier videos. Customers keep asking: where is my order?", "do": [{"k": "show", "el": "heading"}]},
    {"say": "Without MCP, Claude can't reach the orders database. You look up the order yourself, and copy-paste it. Every time.", "do": [{"k": "show", "el": "left"}]},
    {"say": "With an MCP server, Claude gets a get order tool. It calls it, and answers directly. In Claude Code, or in any app that speaks MCP.", "do": [{"k": "show", "el": "arrow"}, {"k": "show", "el": "right", "at": 0.4}], "hold": 0.5}]},

  {"type": "screen", "chapter": "The problem", "project": "mugs-mcp", "kicker": "**DEMO** · The problem", "lines": [
    {"say": "Here are our orders: three of them, each with a customer, an item, a status and a delivery date.", "do": [{"k": "file", "path": "orders.json", "text": ORDERS}]},
    {"say": "In a real shop, orders live in a database or an online store system, not in a file next to your code. Here, this small JSON file plays that role.", "do": [{"k": "callout", "dur": 6.0, "target": "editor", "match": "\"1042\"", "label": "Stands in for a database"}]},
    {"say": "Claude Code, Claude Desktop and VS Code can't reach that database on their own. And writing a separate integration for each app means doing the same work three times.", "hold": 0.2},
    {"say": "So let's wrap the order lookup in one MCP server, and every app can use it.", "tts": "So let's wrap the order lookup in one M C P server, and every app can use it.", "hold": 0.4}]},

  {"type": "screen", "project": "mugs-mcp", "lines": [
    {"say": "Step one: build the server.", "do": [{"k": "step", "n": 1}, {"k": "clear"}, {"k": "open", "path": "mugs_server.py", "at": 0.6}]},
    {"say": "First, install the MCP Python SDK with pip install mcp. Then I create an MCP server, and give it a name: maple mugs.", "do": [{"k": "type", "path": "mugs_server.py", "text": SV1, "cps": 60}]},
    {"say": "The tool decorator turns a normal Python function into an MCP tool. The type hint and the docstring become the tool's description and input schema. That's what Claude reads, to decide when to call it.", "do": [{"k": "callout", "dur": 7.5, "target": "editor", "match": "@mcp.tool()", "span": 2, "label": "A Python function → an MCP tool"}]},
    {"say": "Then a resource: read-only data, here the shipping policy, with its own address.", "do": [{"k": "type", "path": "mugs_server.py", "text": SV2, "cps": 60}]},
    {"say": "And at the bottom, run over stdio. The client will start this file as a program, and talk to it through its input and output.", "tts": "And at the bottom, run over standard I O. The client will start this file as a program, and talk to it through its input and output.", "do": [{"k": "callout", "dur": 5.5, "target": "editor", "match": "mcp.run(transport=\"stdio\")", "label": "Local server"}], "hold": 0.4},

    {"say": "Step two: build a client.", "do": [{"k": "step", "n": 2}, {"k": "open", "path": "client.py", "at": 0.6}]},
    {"say": "A client is what an AI app uses to talk to a server. Writing a tiny one is also the best way to test your server.", "do": [{"k": "type", "path": "client.py", "text": CLIENT, "cps": 60}]},
    {"say": "First, how to start the server: a command and its arguments, just like typing it in a terminal.", "do": [{"k": "callout", "dur": 5.0, "target": "editor", "match": "server = StdioServerParameters", "span": 2, "label": "How to start it"}]},
    {"say": "Then, async with Client. Entering this block launches the server and agrees on the protocol. Leaving it shuts the server down.", "do": [{"k": "callout", "dur": 6.0, "target": "editor", "match": "async with Client(stdio_client(server))", "label": "Connect"}]},
    {"say": "Inside, I list the server's tools, and call get order by name, with its arguments.", "do": [{"k": "callout", "dur": 5.0, "target": "editor", "match": "result = await client.call_tool", "span": 2, "label": "Call a tool"}], "hold": 0.4},

    {"say": "Step three: run it.", "do": [{"k": "step", "n": 3}]},
    {"say": "Let's look up order 1042.", "tts": "Let's look up order ten forty-two.", "do": [{"k": "cmd", "at": 0.3, "text": "python client.py 1042", "out": ["Tools: ['get_order']", ORDER_1042]}]},
    {"say": "The client started the server, found one tool, get order, and called it. Here's the order: shipped, arriving October twenty-fifth.", "do": [{"k": "callout", "dur": 6.5, "target": "term", "match": ORDER_1042[:30], "label": "Real answer from the server"}]},
    {"say": "And an order that doesn't exist gets a clear message.", "do": [{"k": "cmd", "at": 0.3, "text": "python client.py 9999", "out": ["Tools: ['get_order']", "No order 9999 found."]}]},
    {"say": "No API key needed so far. MCP is just a protocol between two programs. The files include tests that run this same server and client.", "do": [
      {"k": "cmd", "at": 0.8, "text": "python -m pytest -q", "out": [".....                                    [100%]", "5 passed in 5.50s"]}], "hold": 0.5},

    {"say": "Step four: connect Claude Code.", "do": [{"k": "step", "n": 4}]},
    {"say": "One command: claude mcp add, the stdio transport, a name, then two dashes, and the command that starts the server.", "do": [{"k": "cmd", "at": 0.3, "text": "claude mcp add --transport stdio maple-mugs -- python mugs_server.py", "out": ["Added stdio MCP server maple-mugs"]}]},
    {"say": "Everything after the two dashes is passed to the server, untouched. Now Claude Code is the host, and it creates a client for our server.", "do": [{"k": "callout", "dur": 6.0, "target": "term", "match": "-- python mugs_server.py", "label": "How to start the server"}]},
    {"say": "Now let's ask Claude where order 1042 is.", "tts": "Now let's ask Claude where order ten forty-two is.", "do": [{"k": "claude", "at": 0.2}, {"k": "cprompt", "at": 1.2, "text": "Where is order 1042?"}]},
    {"say": "Claude calls the get order tool from our server. The first time, Claude Code asks for your permission.", "do": [{"k": "cout", "dur": 4.0, "lines": ["tool:maple-mugs - get_order (MCP)(order_id: \"1042\")", f"res:{ORDER_1042}", "ai:Order 1042, Priya's Slate teapot, has shipped.", "It should arrive on October 25."]}]},
    {"say": "And there's the answer, straight from our order data. Same server, now used by a real AI app.", "do": [{"k": "callout", "dur": 5.5, "target": "term", "match": "Order 1042, Priya's Slate teapot", "label": "Answered with our tool"}], "hold": 0.6}]},

  {"type": "cards", "chapter": "Tips", "kicker": "**05** · Tips", "heading": "4 tips for [[MCP]]", "rail": True,
   "cards": [{"title": "Never print() in a stdio server", "text": "stdout carries the protocol: **log to stderr**"},
             {"title": "Write clear docstrings", "text": "They're what Claude reads to **pick a tool**"},
             {"title": "Test with a client first", "text": "Or the **MCP Inspector**, before any app"},
             {"title": "Only connect servers you trust", "text": "Outside content can carry **prompt injection**"}],
   "lines": [
    {"say": "Four tips.", "do": [{"k": "show", "el": "heading"}]},
    {"say": "One: in a stdio server, never use print. Standard output carries the protocol messages, and a print breaks them. Use the logging module instead.", "do": [{"k": "show", "el": "card1"}]},
    {"say": "Two: write clear docstrings. They're what Claude reads, to decide which tool to call, and when.", "do": [{"k": "show", "el": "card2"}]},
    {"say": "Three: test your server with a small client, like ours, or with the MCP Inspector, before you connect it to an app.", "tts": "Three: test your server with a small client, like ours, or with the M C P Inspector, before you connect it to an app.", "do": [{"k": "show", "el": "card3"}]},
    {"say": "And four: only connect servers you trust. A server that fetches outside content can expose you to prompt injection.", "do": [{"k": "show", "el": "card4"}], "hold": 0.6}]},

  {"type": "checks", "chapter": "Recap", "heading": "Recap",
   "items": ["A **server** offers tools and data; a **client** connects to it",
             "Build a server for **many apps**, a client for **your own app**",
             "Connect it: [[claude mcp add]]"],
   "lines": [
    {"say": "Let's recap.", "do": [{"k": "show", "el": "heading"}]},
    {"say": "An MCP server offers tools and data. An MCP client, inside the AI app, connects to it.", "tts": "An M C P server offers tools and data. An M C P client, inside the AI app, connects to it.", "do": [{"k": "show", "el": "item1"}]},
    {"say": "Build a server when your data should work in many AI apps. Build a client when your own app should use existing servers.", "do": [{"k": "show", "el": "item2"}]},
    {"say": "And to use a server in Claude Code, it's one command: claude mcp add.", "do": [{"k": "show", "el": "item3"}], "hold": 0.5}]},

  {"type": "outro", "title": "Thanks for [[watching]]", "subtitle": "The server, the client and the tests are in the description", "lines": [
    {"say": "The server, the client, a cheat sheet, and the tests are linked in the description. They run with no API key.", "do": [{"k": "show", "el": "line1"}]},
    {"say": "If this helped, like the video, and subscribe to Zero Cost AI for more free AI tutorials. See you in the next one!", "do": [{"k": "show", "el": "line2"}], "hold": 1.5}]},
 ]}

(HERE / "script.json").write_text(json.dumps(script, indent=1, ensure_ascii=False), encoding="utf-8")
print("script.json written:", sum(len(s["lines"]) for s in script["scenes"]), "lines")
