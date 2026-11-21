# Performance review after the cache release (2026-09-30)

Attendees: Lena, Sam, Omar

## Load test results (Omar)
- p95 latency of the catalog API: **210 ms** (target was 300 ms). Before the cache: 840 ms.
- Cache hit rate: **71%** during the test, 93% after a 10-minute warm-up.
- 2,000 requests per second held for 30 minutes with 6 instances.

## Problems found
- When a popular product's entry expires, many requests miss the cache at the same time and all
  go to PostgreSQL. This is a **cache stampede**. During the test it doubled the database load for
  about 20 seconds.
- The "featured products" job sometimes runs twice when two instances start at the same time.

## Decisions
- Keep the 10-minute TTL for now.
- Fix the duplicate job with a lock in Redis (owner: Sam). DONE on 2026-10-02.

## Open risks
- RISK-1: Cache stampede on popular products. Proposed fix: add a random jitter to the TTL, or
  let only one request rebuild an entry. **Status: OPEN**, owner Lena.
- RISK-2: Price eviction is not built yet. Until it is, a new price can take up to 10 minutes
  to appear. **Status: OPEN**, owner Sam.
