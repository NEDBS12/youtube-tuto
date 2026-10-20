# Claude tool use cheat sheet

## The lifecycle (client tools)

1. You send `messages` + `tools` (each tool: `name`, `description`, `input_schema`).
2. Claude answers with `stop_reason: "tool_use"` and one or more `tool_use` blocks: `id`, `name`, `input`.
3. You run the tool, then send a `user` message whose content starts with `tool_result` blocks:
   `tool_use_id` (the same `id`), `content`, and `is_error: true` if the tool failed.
4. Repeat while `stop_reason` is `"tool_use"`. Any other stop reason ends the loop.

Rules: the `tool_result` message must come right after the assistant's `tool_use` message, and the
`tool_result` blocks must come first in its content (any text goes after them).

## stop_reason values

| Value | Meaning | What to do |
|---|---|---|
| `end_turn` | Claude finished its answer | Use the response |
| `tool_use` | Claude wants a tool run | Run it, send the `tool_result`, call again |
| `max_tokens` | Hit your `max_tokens` limit | Raise `max_tokens` or continue the response |
| `stop_sequence` | One of your `stop_sequences` was emitted | Read `stop_sequence` to see which |
| `pause_turn` | A server-tool loop (web search, code execution) hit its iteration limit | Send the assistant content back to continue |
| `refusal` | Claude declined to respond | Read `stop_details`, retry on a fallback model |
| `model_context_window_exceeded` | The response filled the context window | Treat it as truncated |

## Manual loop or Tool Runner?

| Tool Runner (`client.beta.messages.tool_runner`, beta) | Manual loop (`client.messages.create` in a `while`) |
|---|---|
| Runs tools, appends messages, loops until no tool call | You control every step |
| `@beta_tool` builds the schema from type hints + docstring | You write the JSON schema |
| A tool exception becomes a `tool_result` with `is_error: true` | You catch errors and set `is_error` yourself |
| `max_iterations=` bounds the loop; `until_done()` returns the final message | Best for human approval, custom logging, conditional execution |

Sources: https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works,
https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner,
https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons
