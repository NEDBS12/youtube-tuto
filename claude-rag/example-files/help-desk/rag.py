import pathlib
import re
import sys
import anthropic

client = anthropic.Anthropic()
DOCS = pathlib.Path(__file__).parent / "docs"
STOP = {"a", "an", "the", "i", "my", "is", "can", "do", "you",
        "to", "of", "and", "or", "it", "in", "for", "what", "how"}


# 1. Chunk: split every doc into its ## sections
def load_chunks():
    chunks = []
    for path in sorted(DOCS.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        for section in text.split("\n## ")[1:]:
            title, _, body = section.partition("\n")
            chunks.append({"source": path.name, "title": title,
                           "text": body.strip()})
    return chunks


# 2. Retrieve: rank chunks by the words they share with the question
def words(text):
    found = re.findall(r"[a-z0-9]+", text.lower())
    return {w.removesuffix("s") for w in found} - STOP


def search(question, chunks, k=3):
    q = words(question)
    scored = [(len(q & words(c["title"] + " " + c["text"])), c)
              for c in chunks]
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [c for score, c in scored[:k] if score > 0]


# 3. Augment: send the chunks as search results, citations on
def ask(question):
    found = search(question, load_chunks())
    for c in found:
        print(f"[retrieved] {c['source']} > {c['title']}")
    results = [{
        "type": "search_result",
        "source": c["source"],
        "title": c["title"],
        "content": [{"type": "text", "text": c["text"]}],
        "citations": {"enabled": True},
    } for c in found]
    if not results:
        results = [{"type": "text", "text": "No results found."}]

    # 4. Generate: Claude answers from the results and cites them
    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        system=("You answer customer questions for Maple Mugs. "
                "Use only the search results. If they don't contain "
                "the answer, say you don't know."),
        messages=[{"role": "user", "content": results + [
            {"type": "text", "text": question}]}],
    )
    sources = set()
    for block in response.content:
        if block.type == "text":
            print(block.text, end="")
            for cite in block.citations or []:
                sources.add(f"{cite.source} > {cite.title}")
    print("\n\nSources:", "; ".join(sorted(sources)) or "none")


if __name__ == "__main__":
    ask(sys.argv[1])
