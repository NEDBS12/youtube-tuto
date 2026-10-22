"""Generates script.json for the embeddings + normalization tutorial from the real example files."""
import json, pathlib

HERE = pathlib.Path(__file__).parent
EX = HERE / "example-files" / "faq-search"
read = lambda f: (EX / f).read_text(encoding="utf-8")
VEC, TOY, SEARCH = read("vectors.py"), read("toy.py"), read("search.py")
v2 = VEC.index("def dot(")
V1, V2 = VEC[:v2], VEC[v2:]
s2 = SEARCH.index("# 2. Embed the customer's question")
S1, S2 = SEARCH[:s2], SEARCH[s2:]
Q = "The package never showed up"
TOY_OUT = ["doc  length   dot  cosine", "A     2.83  4.00  1.000", "B     5.10  6.00  0.832", "",
           "After normalizing to length 1:", "A     length 1.00  dot 1.000", "B     length 1.00  dot 0.832"]

script = {
 "title": "claude-embeddings",
 "steps": ["Measure length", "Compare vectors", "Normalize", "Embed the FAQ", "Search by meaning"],
 "scenes": [
  {"type": "title", "chapter": "Introduction", "kicker": "AI fundamentals · step by step",
   "title": "Embeddings & Normalization\n[[Text → Vectors → Meaning]]", "subtitle": "How AI compares meaning, and why every vector gets length 1",
   "lines": [
    {"say": "A customer writes: the package never showed up. Your FAQ says: where is my order? Not one word in common."},
    {"say": "Keyword search misses it. Embeddings find it. In this video, you'll learn what an embedding is, what normalizing a vector means, and why it matters."},
    {"say": "Then we'll build a small FAQ search in Python, step by step.", "hold": 0.6}]},

  {"type": "bullets", "chapter": "What is an embedding?", "kicker": "**01** · The concept", "heading": "What is an [[embedding]]?",
   "items": ["A **list of numbers** that captures what a text means",
             "Similar meaning → vectors that **point the same way**",
             "Made by an **embedding model**, not by Claude itself"],
   "card": {"title": "ONE TEXT → ONE VECTOR", "code": "\"Where is my order?\"\n\n→ [0.021, -0.013, 0.044,\n   0.008, -0.031, ...]\n\n1,024 numbers by default\n(voyage-4 models)"},
   "lines": [
    {"say": "So, what is an embedding?", "do": [{"k": "show", "el": "heading"}]},
    {"say": "An embedding is a list of numbers that captures what a text means. A list of numbers like this is called a vector.", "do": [{"k": "show", "el": "item1"}, {"k": "show", "el": "card", "at": 1.5}]},
    {"say": "Texts with similar meaning get vectors that point in a similar direction, even when they use different words.", "do": [{"k": "show", "el": "item2"}]},
    {"say": "They come from an embedding model. Anthropic doesn't make one; its docs point to Voyage AI. Voyage's latest models return one thousand and twenty-four numbers per text by default.", "do": [{"k": "show", "el": "item3"}], "hold": 0.5}]},

  {"type": "rows", "chapter": "Length, direction and cosine", "kicker": "**02** · How it works", "heading": "Direction is [[meaning]]",
   "rows": [{"label": "Length (L2 norm)", "text": "√(sum of squares): how **long** the arrow is"},
            {"label": "Cosine similarity", "text": "Compares **direction** only: 1 = same, 0 = unrelated"},
            {"label": "Normalize", "text": "Divide by the length → every vector has **length 1**"}],
   "banner": "Length 1 everywhere → dot product = cosine similarity",
   "lines": [
    {"say": "Picture each vector as an arrow. Two things matter: its direction, and its length.", "do": [{"k": "show", "el": "heading"}]},
    {"say": "The length, also called the L2 norm, is the square root of the sum of the squares of its numbers.", "tts": "The length, also called the L 2 norm, is the square root of the sum of the squares of its numbers.", "do": [{"k": "show", "el": "row1"}]},
    {"say": "Meaning lives in the direction. Cosine similarity compares only the direction: one means the same direction, zero means unrelated.", "do": [{"k": "show", "el": "row2"}]},
    {"say": "Normalizing means dividing a vector by its length. The direction stays the same, but the length becomes exactly one.", "do": [{"k": "show", "el": "row3"}]},
    {"say": "And here's the payoff: when every vector has length one, the simple dot product gives the same number as cosine similarity, and it's faster to compute.", "do": [{"k": "show", "el": "banner"}], "hold": 0.5}]},

  {"type": "compare", "chapter": "Two kinds of normalization", "kicker": "**03** · Don't mix them up", "heading": "Two kinds of [[normalization]]",
   "left": {"title": "Normalizing embeddings", "body": "• Scale each vector to length 1\n• You do it (or the model does)\n  before comparing vectors\n• Voyage vectors already\n  come normalized"},
   "right": {"title": "Normalization inside LLMs", "body": "• LayerNorm / RMSNorm layers\n• Rescale the numbers between\n  layers of the network\n• Keep training stable\n• Built into the model:\n  not something you call"},
   "lines": [
    {"say": "Careful: normalization means two different things in AI.", "do": [{"k": "show", "el": "heading"}]},
    {"say": "For embeddings, it means scaling each vector to length one before you compare vectors. That's today's topic.", "do": [{"k": "show", "el": "left"}]},
    {"say": "Inside a language model, normalization layers like LayerNorm and RMS Norm rescale the numbers between layers, to keep training stable. They're built into the model. You never call them yourself.", "tts": "Inside a language model, normalization layers like Layer Norm and R M S Norm rescale the numbers between layers, to keep training stable. They're built into the model. You never call them yourself.", "do": [{"k": "show", "el": "arrow"}, {"k": "show", "el": "right", "at": 0.4}], "hold": 0.5}]},

  {"type": "compare", "chapter": "When to use embeddings", "kicker": "**04** · When to use it", "heading": "When to use [[embeddings]]",
   "left": {"title": "Use embeddings for…", "body": "• Search by meaning\n• Finding the chunks for RAG\n• Spotting duplicates\n• Recommendations\n• Grouping similar texts"},
   "right": {"title": "Keyword search is better for…", "body": "• Exact codes and IDs:\n  \"order 1042\", \"SKU-77\"\n• Rare names and terms\n\nBest of both: combine them"},
   "lines": [
    {"say": "When should you use embeddings?", "do": [{"k": "show", "el": "heading"}]},
    {"say": "To search by meaning, to find the right chunks for RAG, to spot duplicates, for recommendations, and to group similar texts.", "do": [{"k": "show", "el": "left"}]},
    {"say": "But for exact codes, IDs and rare names, keyword search is better. Real systems often combine both.", "do": [{"k": "show", "el": "arrow"}, {"k": "show", "el": "right", "at": 0.4}], "hold": 0.5}]},

  {"type": "compare", "chapter": "Our use case", "kicker": "**05** · Our use case", "heading": "An FAQ search for [[Maple Mugs]]",
   "left": {"title": "Keyword search", "body": f"Customer: \"{Q}\"\n\nShared words with\n\"Where is my order?\": 0\n\n✗ No match"},
   "right": {"title": "Embedding search", "body": "Both texts → vectors\nthat point the same way\n\n✓ \"Where is my order?\"\n   is the top match"},
   "lines": [
    {"say": "Our use case: an FAQ search for Maple Mugs, the small online shop from my RAG video.", "do": [{"k": "show", "el": "heading"}]},
    {"say": "With keyword search, the package never showed up shares zero words with where is my order. No match.", "do": [{"k": "show", "el": "left"}]},
    {"say": "With embeddings, both questions become vectors that point the same way, so the right answer comes first.", "do": [{"k": "show", "el": "arrow"}, {"k": "show", "el": "right", "at": 0.4}], "hold": 0.5}]},

  {"type": "screen", "project": "faq-search", "kicker": "**DEMO** · The math first", "lines": [
    {"say": "Let's start with the math, in plain Python. No libraries.", "do": [{"k": "step", "n": 1}, {"k": "open", "path": "vectors.py", "at": 0.6}]},
    {"say": "Length is the square root of the sum of squares. Normalize divides every number by that length.", "do": [{"k": "type", "path": "vectors.py", "text": V1, "cps": 60}]},
    {"say": "So a vector like three, four has length five. Normalized, it becomes zero point six, zero point eight: same direction, length one.", "do": [{"k": "callout", "dur": 5.5, "target": "editor", "match": "return [x / n for x in v]", "label": "Same direction, length 1"}], "hold": 0.4},

    {"say": "Step two: compare vectors.", "do": [{"k": "step", "n": 2}]},
    {"say": "The dot product multiplies the numbers pair by pair, and adds them up. Cosine divides that by both lengths, so only the direction counts.", "do": [{"k": "type", "path": "vectors.py", "text": V2, "cps": 60}]},
    {"say": "Now a tiny example with arrows of just two numbers. A points the same way as the query. B points elsewhere, but it's longer.", "do": [{"k": "file", "path": "toy.py", "text": TOY}]},
    {"say": "Let's run it, and look at the numbers.", "do": [{"k": "cmd", "at": 0.3, "text": "python toy.py", "out": TOY_OUT}]},
    {"say": "Look: the raw dot product prefers B, only because B is longer. Cosine gets it right: A is a perfect match, one point zero.", "do": [{"k": "callout", "dur": 6.0, "target": "term", "match": "B     5.10  6.00  0.832", "label": "Fooled by length"}], "hold": 0.4},

    {"say": "Step three: normalize.", "do": [{"k": "step", "n": 3}]},
    {"say": "The second half of the output does the same comparison, but normalizes the query and both documents first."},
    {"say": "Every length is now one, and the dot product gives exactly the cosine values. No division needed when you compare.", "do": [{"k": "callout", "dur": 6.0, "target": "term", "match": "A     length 1.00  dot 1.000", "span": 2, "label": "dot = cosine"}]},
    {"say": "That's why embedding providers normalize their vectors. You store them once, and every comparison is a fast dot product.", "hold": 0.4}]},

  {"type": "screen", "project": "faq-search", "lines": [
    {"say": "Step four: embed the FAQ with real embeddings.", "do": [{"k": "step", "n": 4}, {"k": "clear"}, {"k": "open", "path": "search.py", "at": 0.6}]},
    {"say": "With the Voyage AI package installed, I create a client. It reads your Voyage API key from an environment variable.", "do": [{"k": "type", "path": "search.py", "text": S1, "cps": 60}]},
    {"say": "Embed sends the five FAQ questions, and gets back five vectors. Note input type: document. Questions you search with use query.", "do": [{"k": "callout", "dur": 5.5, "target": "editor", "match": "docs = vo.embed(FAQ", "span": 2, "label": "input_type matters"}]},
    {"say": "The print line shows the size of each vector, and its length.", "do": [{"k": "callout", "dur": 4.5, "target": "editor", "match": "print(f\"{len(docs)} vectors", "span": 2, "label": "Size and length"}], "hold": 0.4},

    {"say": "Step five: search by meaning.", "do": [{"k": "step", "n": 5}]},
    {"say": "I embed the customer's question, with input type query. Then I score every FAQ with a dot product, and print the top three.", "do": [{"k": "type", "path": "search.py", "text": S2, "cps": 60}]},
    {"say": "Why a dot product, not cosine? Voyage vectors already have length one, so the dot product is the cosine.", "do": [{"k": "callout", "dur": 5.5, "target": "editor", "match": "# 3. Length 1 already", "span": 2, "label": "Normalized by Voyage"}]},
    {"say": "Let's run it with our customer's question.", "do": [
      {"k": "cmd", "at": 0.6, "text": f"python search.py \"{Q}\"", "out": ["5 vectors, 1024 numbers each, length 1.000", "0.712  Where is my order?", "0.486  Can I change my delivery address?", "0.441  Is shipping free?"]}]},
    {"say": "Five vectors of one thousand and twenty-four numbers, each with length one. Already normalized.", "do": [{"k": "callout", "dur": 5.0, "target": "term", "match": "5 vectors, 1024 numbers", "label": "Length 1.000"}]},
    {"say": "And the top match is where is my order, with zero words in common. That's search by meaning.", "do": [{"k": "callout", "dur": 5.5, "target": "term", "match": "Where is my order?", "label": "Top match"}]},
    {"say": "Your exact scores will differ. The files also include an offline test, with no API key needed.", "do": [
      {"k": "cmd", "at": 0.8, "text": "python -m pytest -q", "out": [".....                                    [100%]", "5 passed in 0.04s"]}], "hold": 0.6}]},

  {"type": "cards", "chapter": "Tips", "kicker": "**06** · Tips", "heading": "4 tips for [[embeddings]]", "rail": True,
   "cards": [{"title": "One model for everything", "text": "Docs and queries: the same model"},
             {"title": "Set input_type", "text": "`document` to store, `query` to search"},
             {"title": "Shortened? Normalize again", "text": "Cut to 256 numbers → length < 1"},
             {"title": "Store normalized vectors", "text": "Then every comparison is a dot product"}],
   "lines": [
    {"say": "Four tips.", "do": [{"k": "show", "el": "heading"}]},
    {"say": "One: embed your documents and your queries with the same model. Vectors from different models can't be compared.", "do": [{"k": "show", "el": "card1"}]},
    {"say": "Two: set input type. Voyage's docs say to use document for what you store, and query for what you search with. Don't leave it out.", "do": [{"k": "show", "el": "card2"}]},
    {"say": "Three: if you shorten vectors you already stored, for example to two hundred and fifty-six numbers, their length drops below one. Normalize them again.", "do": [{"k": "show", "el": "card3"}]},
    {"say": "And four: store normalized vectors, so every comparison is a fast dot product.", "do": [{"k": "show", "el": "card4"}], "hold": 0.6}]},

  {"type": "checks", "chapter": "Recap", "heading": "Recap",
   "items": ["An embedding = a vector of numbers; **direction = meaning**",
             "Normalize: divide by the length → **length 1**",
             "Length 1 → [[dot product = cosine]] similarity"],
   "lines": [
    {"say": "Let's recap.", "do": [{"k": "show", "el": "heading"}]},
    {"say": "An embedding is a vector of numbers, and its direction carries the meaning.", "do": [{"k": "show", "el": "item1"}]},
    {"say": "Normalizing divides a vector by its length, so it has length one.", "do": [{"k": "show", "el": "item2"}]},
    {"say": "And with length one everywhere, the dot product is the cosine similarity: simple, and fast.", "do": [{"k": "show", "el": "item3"}], "hold": 0.5}]},

  {"type": "outro", "title": "Thanks for [[watching]]", "subtitle": "The code and an offline test are in the description", "lines": [
    {"say": "The code, a cheat sheet, and an offline test you can run without an API key are linked in the description.", "do": [{"k": "show", "el": "line1"}]},
    {"say": "If this helped, like the video, and subscribe to Zero Cost AI for more free AI tutorials. See you in the next one!", "do": [{"k": "show", "el": "line2"}], "hold": 1.5}]},
 ]}

(HERE / "script.json").write_text(json.dumps(script, indent=1, ensure_ascii=False), encoding="utf-8")
print("script.json written:", sum(len(s["lines"]) for s in script["scenes"]), "lines")
