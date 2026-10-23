# Prompt caching: cheat sheet

## The idea

Claude reads your whole prompt on every request. When the start of the prompt is the same every time (instructions, a handbook, tool definitions, a long document), prompt caching stores that part, the **prefix**, so later requests reuse it: cheaper and faster.

## Two ways to turn it on (Python SDK)

```python
# 1. Automatic: one field, best for multi-turn chats
client.messages.create(..., cache_control={"type": "ephemeral"})

# 2. Explicit breakpoint: on the last block that never changes
system = [
    {"type": "text", "text": "Answer Maple Mugs customers."},
    {"type": "text", "text": HANDBOOK,
     "cache_control": {"type": "ephemeral"}},
]
```

- The prefix is everything in the order `tools` → `system` → `messages`, up to and including the block with `cache_control`.
- Up to 4 breakpoints per request. Breakpoints themselves cost nothing.
- Automatic caching puts the breakpoint on the last block and moves it forward as a chat grows. If your last block changes every request (a timestamp, per-request context), use an explicit breakpoint on the last stable block instead.

## Check it in `usage`

| Field | Meaning |
|---|---|
| `cache_creation_input_tokens` | written to the cache on this request |
| `cache_read_input_tokens` | read from the cache (the cheap part) |
| `input_tokens` | after the last breakpoint, not cached |

Total input = read + written + input_tokens. If both cache fields are 0, nothing was cached.

## Prices and lifetime

- 5-minute cache write: 1.25 × the base input price. 1-hour cache write (`"ttl": "1h"`): 2 ×.
- Cache read: 0.1 × the base input price on most models (0.05 × on Claude Opus 5.5 and Sonnet 5.5).
- The cache lives 5 minutes by default, and every hit refreshes it for free.
- Minimum prefix: 512 tokens on the newest models (Opus 5.5, Sonnet 5.5, Haiku 5.5), up to 4,096 on some older ones. Shorter prompts are simply not cached, with no error.

## What breaks the cache

- Any change at or before the breakpoint: a different character, a new timestamp, a different order.
- Changing tool definitions breaks everything. Changing `tool_choice`, adding images, or changing thinking or effort settings breaks the message part.
- Parallel requests: the cache exists only after the first response starts. Send one request first, then the rest.

## Links

- Prompt caching (Claude docs): https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- Pricing: https://platform.claude.com/docs/en/about-claude/pricing
