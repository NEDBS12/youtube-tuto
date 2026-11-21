# Incident report: stale prices shown (2026-10-14)

Severity: SEV-2
Duration: 9 minutes (10:42 to 10:51)

## What happened
Marketing lowered the price of 40 products at 10:42 for a flash sale.
The product pages kept showing the old, higher price for up to 9 minutes, because the prices
were still in the Redis cache (TTL 10 minutes). 312 customers saw the old price; the cart
showed the new price, so nobody was charged the wrong amount.

## Root cause
The price eviction path (RISK-2 from the performance review) was not built yet.

## Fix
- The pricing service now publishes a `price-changed` event.
- The checkout service listens to it and evicts the product's entries from Redis right away.
- Released on 2026-10-17. Tested: a new price appears in under 2 seconds.
- RISK-2 is now **CLOSED**.

## Follow-ups
- Add an alert when a price in the cart and on the page differ (owner: Omar). DONE.
- Write a runbook for "wrong price on the site" (owner: Priya). DONE.
