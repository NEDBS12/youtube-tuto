#!/usr/bin/env bash
# Start the "Test guard" scheduled task, for example after a deploy.
# ROUTINE_URL and ROUTINE_TOKEN come from the task's API trigger.
# Keep them in your CI secrets: never commit the token.
curl -sS -X POST "$ROUTINE_URL" \
  -H "Authorization: Bearer $ROUTINE_TOKEN" \
  -H "anthropic-beta: experimental-cc-routine-2026-04-01" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Deploy ${1:-unknown} just shipped to production.\"}"
