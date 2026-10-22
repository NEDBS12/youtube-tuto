# RAG with Claude: cheat sheet

## The three steps

| Step | What happens | In `rag.py` |
|---|---|---|
| **Retrieve** | Find the chunks that match the question | `load_chunks()` + `search()` |
| **Augment** | Put those chunks in the prompt | `search_result` blocks in the user message |
| **Generate** | Claude answers from them, and cites them | `client.messages.create(...)`, then read `block.citations` |

## Do you need RAG?

- **Knowledge base under ~200,000 tokens (about 500 pages)?** Anthropic says you can put all of it in the prompt instead. Use prompt caching to make repeat questions faster and cheaper.
- **Bigger, changing often, or answers must show sources?** Use RAG.
- **Claude needs to do something (send, update, look up live data)?** Use tools.

## A search result block

```python
{
    "type": "search_result",
    "source": "returns.md",          # required: a URL or any stable id
    "title": "Return window",        # required
    "content": [{"type": "text", "text": "You can return a mug..."}],  # required
    "citations": {"enabled": True},  # optional: off by default
}
```

- Citations are all-or-nothing: every search result in a request must use the same setting.
- Search results go in user messages only (at the top level, or inside a tool result).
- Nothing found? Send a text block like `"No results found."` instead of raising an error.
- Each citation in the reply has `source`, `title`, `cited_text` and `search_result_index`. `cited_text` doesn't count toward output tokens.
- Claude cites whole text blocks: split long content into several text blocks for finer citations.

## Better retrieval

- **Chunk by meaning:** sections or paragraphs that make sense on their own.
- **Keyword + embeddings:** keyword search (like BM25) finds exact terms; embeddings find the same meaning in different words. Anthropic doesn't make an embedding model; its docs point to Voyage AI.
- **Retrieve enough:** in Anthropic's Contextual Retrieval tests, passing the top 20 chunks worked better than 5 or 10.
- **Allow "I don't know":** tell Claude to answer only from the results.

## Links

- Search results: https://platform.claude.com/docs/en/build-with-claude/search-results
- Citations: https://platform.claude.com/docs/en/build-with-claude/citations
- Embeddings: https://platform.claude.com/docs/en/build-with-claude/embeddings
- Contextual Retrieval: https://www.anthropic.com/news/contextual-retrieval
