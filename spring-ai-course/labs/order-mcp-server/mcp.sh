#!/usr/bin/env bash
# Send one MCP request with curl.  usage: ./mcp.sh <method> ['<params as JSON>']
# Example: ./mcp.sh tools/call '{"name":"find_order","arguments":{"id":"A-1001"}}'
URL=http://localhost:8081/mcp
H=(-H "Content-Type: application/json" -H "Accept: application/json, text/event-stream")

# 1. Initialize once, and keep the session id the server returns
if [ ! -f .mcp-session ]; then
  curl -s -D - -o /dev/null "${H[@]}" "$URL" \
    -d '{"jsonrpc":"2.0","id":0,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"curl","version":"1.0"}}}' \
    | grep -i '^mcp-session-id' | cut -d' ' -f2 | tr -d '\r' > .mcp-session
  curl -s "${H[@]}" -H "Mcp-Session-Id: $(cat .mcp-session)" "$URL" -d '{"jsonrpc":"2.0","method":"notifications/initialized"}'
fi

# 2. Send the request in that session, and print the JSON answer
curl -s "${H[@]}" -H "Mcp-Session-Id: $(cat .mcp-session)" "$URL" \
  -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"$1\",\"params\":${2:-"{}"}}" | sed -n 's/^data://p'
echo
