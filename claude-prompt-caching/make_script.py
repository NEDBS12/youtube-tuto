"""Generates script.json for the prompt caching tutorial from the real example files."""
import json, pathlib

HERE = pathlib.Path(__file__).parent
EX = HERE / "example-files" / "cached-help-desk"
read = lambda f: (EX / f).read_text(encoding="utf-8")
HANDBOOK, NO_CACHE, ASK, COST = read("handbook.md"), read("no_cache.py"), read("ask.py"), read("cost.py")
a2, a3 = ASK.index("# 2. The part"), ASK.index("# 3. Check")
A1, A2, A3 = ASK[:a2], ASK[a2:a3], ASK[a3:]
Q1, Q2 = "Are your mugs dishwasher safe?", "Is shipping free?"
ANS1 = "Yes! All our mugs are dishwasher and microwave safe. They're not oven safe, though."
ANS2 = "Standard US shipping is free on orders over $60. Otherwise it's $6."

script = {
 "title": "claude-prompt-caching",
 "steps": ["Stable part first", "Mark the breakpoint", "Check the usage", "Count the savings"],
 "scenes": [
  {"type": "title", "chapter": "Introduction", "kicker": "Claude API · step by step",
   "title": "Prompt Caching\n[[Pay once, reuse many times]]", "subtitle": "Make Claude cheaper and faster when your prompt repeats",
   "lines": [
    {"say": "Your help desk bot sends the same long handbook to Claude with every single question. And you pay for it every single time."},
    {"say": "Prompt caching fixes that. In this video, you'll learn what it is, how it works, and when to use it."},
    {"say": "Then we'll add it to a real Python app, step by step, and measure the savings.", "hold": 0.6}]},

  {"type": "bullets", "chapter": "What is prompt caching?", "kicker": "**01** · The concept", "heading": "What is [[prompt caching]]?",
   "items": ["Claude **stores the start** of your prompt, the **prefix**",
             "Later requests with the same prefix **reuse it**",
             "**Cheaper** to read, and Claude answers **faster**"],
   "card": {"title": "THE EASIEST WAY: ONE FIELD", "code": "client.messages.create(\n  model=\"claude-sonnet-5-5\",\n  max_tokens=300,\n  cache_control={\n    \"type\": \"ephemeral\"},\n  messages=...,\n)"},
   "lines": [
    {"say": "So, what is prompt caching?", "do": [{"k": "show", "el": "heading"}]},
    {"say": "Claude reads your whole prompt on every request. With prompt caching, it stores the start of the prompt, called the prefix.", "do": [{"k": "show", "el": "item1"}]},
    {"say": "The next request that starts with exactly the same prefix reuses it, instead of processing it again.", "do": [{"k": "show", "el": "item2"}]},
    {"say": "Think of a teacher who already read the textbook. For the next question, they don't reread it from page one.", "hold": 0.2},
    {"say": "Reading from the cache costs much less, and Claude starts answering faster. The easiest way to turn it on is one field: cache control, type ephemeral.", "do": [{"k": "show", "el": "item3"}, {"k": "show", "el": "card", "at": 2.5}], "hold": 0.5}]},

  {"type": "rows", "chapter": "How it works", "kicker": "**02** · How it works", "heading": "Write once, [[read many times]]",
   "rows": [{"label": "The prefix", "text": "tools → system → messages, **up to the breakpoint**"},
            {"label": "First request", "text": "**Writes** the cache: 1.25× the normal input price"},
            {"label": "Next requests", "text": "**Read** it: 0.1× the price (0.05× on Sonnet 5.5)"}],
   "banner": "The cache lives 5 minutes, and every hit resets the timer",
   "lines": [
    {"say": "Here's how it works.", "do": [{"k": "show", "el": "heading"}]},
    {"say": "Claude reads a request in a fixed order: tools, then the system prompt, then the messages. The prefix is everything up to a point you mark, called the cache breakpoint.", "do": [{"k": "show", "el": "row1"}]},
    {"say": "The first request writes the prefix to the cache. That costs a little more: one and a quarter times the normal input price.", "do": [{"k": "show", "el": "row2"}]},
    {"say": "Every request after that reads it, for a tenth of the price. On the newest models, like Claude Sonnet 5.5, it's even a twentieth.", "tts": "Every request after that reads it, for a tenth of the price. On the newest models, like Claude Sonnet five point five, it's even a twentieth.", "do": [{"k": "show", "el": "row3"}]},
    {"say": "The cache lives five minutes by default, and every time it's used, the timer starts again, for free.", "do": [{"k": "show", "el": "banner"}], "hold": 0.5}]},

  {"type": "compare", "chapter": "When to use it", "kicker": "**03** · When to use it", "heading": "When to use [[prompt caching]]",
   "left": {"title": "Use it when…", "body": "• The start of your prompt\n  stays the same\n• Long instructions, a handbook,\n  documents, tool definitions\n• Long chats and agents\n• Many requests in a row"},
   "right": {"title": "Skip it when…", "body": "• The prompt is short\n  (under 512 tokens on the\n  newest models: not cached)\n• The start changes every time\n• One-off requests, far apart"},
   "lines": [
    {"say": "When should you use it?", "do": [{"k": "show", "el": "heading"}]},
    {"say": "When the start of your prompt stays the same across many requests: long instructions, a handbook, documents, tool definitions, long chats and agents.", "do": [{"k": "show", "el": "left"}]},
    {"say": "Skip it for short prompts. Under the minimum, 512 tokens on the newest models, nothing is cached at all. And skip it when the start of the prompt changes every time, or for one-off requests far apart.", "tts": "Skip it for short prompts. Under the minimum, five hundred and twelve tokens on the newest models, nothing is cached at all. And skip it when the start of the prompt changes every time, or for one-off requests far apart.", "do": [{"k": "show", "el": "arrow"}, {"k": "show", "el": "right", "at": 0.4}], "hold": 0.5}]},

  {"type": "compare", "chapter": "Our use case", "kicker": "**04** · Our use case", "heading": "A help desk bot for [[Maple Mugs]]",
   "left": {"title": "Without caching", "body": "Every question sends\nthe whole handbook\n(about 1,500 tokens)\n\n✗ Full price, every time"},
   "right": {"title": "With caching", "body": "The handbook is written\nto the cache once\n\n✓ Then read for a\n   twentieth of the price"},
   "lines": [
    {"say": "Our use case: a help desk bot for Maple Mugs, the small online shop from my earlier videos. It answers customers using the store's handbook.", "do": [{"k": "show", "el": "heading"}]},
    {"say": "Without caching, every question sends the whole handbook, about 1,500 tokens, at full price.", "tts": "Without caching, every question sends the whole handbook, about fifteen hundred tokens, at full price.", "do": [{"k": "show", "el": "left"}]},
    {"say": "With caching, the handbook is written once. Then every question reads it, for a twentieth of the price.", "do": [{"k": "show", "el": "arrow"}, {"k": "show", "el": "right", "at": 0.4}], "hold": 0.5}]},

  {"type": "screen", "chapter": "The problem", "project": "cached-help-desk", "kicker": "**DEMO** · The problem", "lines": [
    {"say": "Here's the handbook: products, shipping, returns, care. About a thousand words.", "do": [{"k": "file", "path": "handbook.md", "text": HANDBOOK}]},
    {"say": "And here's the bot without caching. The handbook goes into the system prompt, and the customer's question into the message.", "do": [{"k": "file", "path": "no_cache.py", "text": NO_CACHE}]},
    {"say": "Let's ask two questions, and look at the input tokens.", "do": [
      {"k": "cmd", "at": 0.5, "text": f"python no_cache.py \"{Q1}\"", "out": [ANS1, "input tokens: 1479"]},
      {"k": "cmd", "at": 3.2, "text": f"python no_cache.py \"{Q2}\"", "out": [ANS2, "input tokens: 1476"]}]},
    {"say": "Almost 1,500 input tokens, each time. The question is only a few words. The rest is the same handbook, processed and billed again and again.", "tts": "Almost fifteen hundred input tokens, each time. The question is only a few words. The rest is the same handbook, processed and billed again and again.", "do": [{"k": "callout", "dur": 6.5, "target": "term", "match": "input tokens: 1476", "label": "Same handbook, full price"}], "hold": 0.4}]},

  {"type": "screen", "project": "cached-help-desk", "lines": [
    {"say": "Step one: put the stable part first.", "do": [{"k": "step", "n": 1}, {"k": "clear"}, {"k": "open", "path": "ask.py", "at": 0.6}]},
    {"say": "Same start as before. But this time, the system prompt is a list of two text blocks: the short instruction, then the whole handbook.", "do": [{"k": "type", "path": "ask.py", "text": A1, "cps": 60}]},
    {"say": "Why this order? The cache only matches the start of a prompt. So everything that's the same in every request goes first.", "do": [{"k": "callout", "dur": 6.0, "target": "editor", "match": "# 1. Stable part first", "span": 2, "label": "Never changes"}], "hold": 0.4},

    {"say": "Step two: mark the cache breakpoint.", "do": [{"k": "step", "n": 2}]},
    {"say": "On the handbook block, I add cache control, type ephemeral. That's the breakpoint. Everything up to here, and including this block, is the prefix that gets cached.", "do": [{"k": "callout", "dur": 7.5, "target": "editor", "match": "\"cache_control\": {\"type\": \"ephemeral\"}", "label": "Cache up to here"}]},
    {"say": "Then the request. The customer's question changes every time, so it goes after the breakpoint, in the messages.", "do": [{"k": "type", "path": "ask.py", "text": A2, "cps": 60}]},
    {"say": "That's the key rule: put the breakpoint on the last block that stays the same. Never on the part that changes.", "do": [{"k": "callout", "dur": 5.5, "target": "editor", "match": "messages=[{\"role\": \"user\"", "label": "Changes: not cached"}], "hold": 0.4},

    {"say": "Step three: check the usage.", "do": [{"k": "step", "n": 3}]},
    {"say": "Every response tells you what happened with the cache. I print three numbers: tokens written to the cache, tokens read from it, and new tokens after the breakpoint.", "do": [{"k": "type", "path": "ask.py", "text": A3, "cps": 60}]},
    {"say": "Let's ask the first question.", "do": [{"k": "cmd", "at": 0.3, "text": f"python ask.py \"{Q1}\"", "out": [ANS1, "written: 1467  read: 0  new: 12"]}]},
    {"say": "The first request wrote about 1,500 tokens to the cache. Only twelve tokens were new: the question.", "tts": "The first request wrote about fifteen hundred tokens to the cache. Only twelve tokens were new: the question.", "do": [{"k": "callout", "dur": 5.5, "target": "term", "match": "written: 1467  read: 0", "label": "Cache written"}]},
    {"say": "Now a second question, within five minutes.", "do": [{"k": "cmd", "at": 0.3, "text": f"python ask.py \"{Q2}\"", "out": [ANS2, "written: 0  read: 1467  new: 9"]}]},
    {"say": "This time, the whole handbook was read from the cache. Nothing written. That's a cache hit.", "do": [{"k": "callout", "dur": 5.5, "target": "term", "match": "written: 0  read: 1467", "label": "Cache hit"}]},
    {"say": "If both numbers are zero, nothing was cached. Usually the prompt is too short, or something changed in the prefix.", "hold": 0.4},

    {"say": "Step four: count the savings.", "do": [{"k": "step", "n": 4}]},
    {"say": "This little script does the math for a thousand questions a day, using Claude Sonnet 5.5 prices, for the handbook part of the prompt.", "tts": "This little script does the math for a thousand questions a day, using Claude Sonnet five point five prices, for the handbook part of the prompt.", "do": [{"k": "file", "path": "cost.py", "text": COST}]},
    {"say": "Without caching, every question pays the base price. With caching, one write, then 999 cheap reads.", "tts": "Without caching, every question pays the base price. With caching, one write, then nine hundred and ninety-nine cheap reads.", "do": [{"k": "callout", "dur": 6.0, "target": "editor", "match": "cached = (dollars(HANDBOOK, WRITE)", "span": 2, "label": "1 write + 999 reads"}]},
    {"say": "Let's run it, and compare the two numbers.", "do": [{"k": "cmd", "at": 0.3, "text": "python cost.py", "out": ["No cache: $3.00", "Cached:   $0.15", "Saved:    95%"]}]},
    {"say": "Three dollars become fifteen cents. Ninety-five percent saved on that part, and the bigger the handbook, the more you save.", "do": [{"k": "callout", "dur": 6.0, "target": "term", "match": "Saved:    95%", "label": "95% cheaper"}]},
    {"say": "The files also include an offline test, so you can try everything with no API key.", "do": [
      {"k": "cmd", "at": 0.8, "text": "python -m pytest -q", "out": [".....                                    [100%]", "5 passed in 0.31s"]}], "hold": 0.6}]},

  {"type": "cards", "chapter": "Tips", "kicker": "**05** · Tips", "heading": "4 tips for [[prompt caching]]", "rail": True,
   "cards": [{"title": "Stable first, changes last", "text": "Dates and per-request data at the **end**"},
             {"title": "Check the usage", "text": "Both cache numbers 0 → **not cached**"},
             {"title": "Parallel requests? Wait", "text": "Send one first: the cache starts with its response"},
             {"title": "Long gaps? Use 1 hour", "text": "`\"ttl\": \"1h\"`: writes cost 2×"}],
   "lines": [
    {"say": "Four tips.", "do": [{"k": "show", "el": "heading"}]},
    {"say": "One: stable content first, changing content last. A date or a timestamp at the top of your prompt breaks the cache on every request.", "do": [{"k": "show", "el": "card1"}]},
    {"say": "Two: always check the usage. If both cache numbers are zero, nothing was cached, and you get no error.", "do": [{"k": "show", "el": "card2"}]},
    {"say": "Three: for parallel requests, send one first. The cache is only there once the first response starts.", "do": [{"k": "show", "el": "card3"}]},
    {"say": "And four: if requests come more than five minutes apart, you can use a one-hour cache. Writing it costs twice the normal input price.", "do": [{"k": "show", "el": "card4"}], "hold": 0.6}]},

  {"type": "checks", "chapter": "Recap", "heading": "Recap",
   "items": ["Caching stores the **prefix**: the start of your prompt",
             "Stable part first, then **cache_control** on its last block",
             "One write, then [[cheap reads]]: check the usage"],
   "lines": [
    {"say": "Let's recap.", "do": [{"k": "show", "el": "heading"}]},
    {"say": "Prompt caching stores the prefix, the start of your prompt, for five minutes.", "do": [{"k": "show", "el": "item1"}]},
    {"say": "Put the stable part first, and mark its last block with cache control.", "do": [{"k": "show", "el": "item2"}]},
    {"say": "You pay for one write, then cheap reads. And the usage numbers tell you if it worked.", "do": [{"k": "show", "el": "item3"}], "hold": 0.5}]},

  {"type": "outro", "title": "Thanks for [[watching]]", "subtitle": "The code and an offline test are in the description", "lines": [
    {"say": "The code, the handbook, a cheat sheet, and an offline test you can run without an API key are linked in the description.", "do": [{"k": "show", "el": "line1"}]},
    {"say": "If this helped, like the video, and subscribe to Zero Cost AI for more free AI tutorials. See you in the next one!", "do": [{"k": "show", "el": "line2"}], "hold": 1.5}]},
 ]}

(HERE / "script.json").write_text(json.dumps(script, indent=1, ensure_ascii=False), encoding="utf-8")
print("script.json written:", sum(len(s["lines"]) for s in script["scenes"]), "lines")
