# Claude connectors cheat sheet

| When | Do this |
|---|---|
| Add a connector | claude.ai → **Customize > Connectors** → **Discover** → search → **Connect to Claude** → sign in |
| The service isn't in the directory | **Add custom connector** with its remote MCP server URL (Free plan: one custom connector) |
| Use it in a chat | **+** in the message box → **Connectors** → turn it on |
| Use it in Claude Code | Sign in to Claude Code with the same claude.ai account, start a new session, check `/mcp` |
| It's missing in Claude Code | `/status`: connectors load only with a claude.ai subscription login (not an API key or a cloud provider), then `/login` |
| Tell Claude where your data lives | Add a line to `CLAUDE.md`, for example: Bug reports live in Notion, on the page "my-shop bugs" |
| Control what it can do (Claude apps) | The connector's page → **Tool permissions**: Always allow / Needs approval / Blocked |
| Turn one off in a Claude Code project | `/mcp` → select it → toggle it off (this project only) |
| Turn them all off for a repo | `.claude/settings.json`: `{ "disableClaudeAiConnectors": true }` |
| Stop using it everywhere | The connector's page → **Disconnect** (or **Remove**) |

- A connector is a connection to an MCP server that the service runs. You connect it once and it's saved to your account: web, desktop, mobile and Claude Code.
- Servers you add with `claude mcp add` stay on that machine, and they work with any login.
- Only connect services you trust. Labels show how much Anthropic reviewed a connector: Verified, Community, or Custom (added by you).

Sources: https://claude.com/docs/connectors/getting-started, https://claude.com/docs/connectors/custom/add-unlisted, https://code.claude.com/docs/en/mcp#use-mcp-servers-from-claude-ai
