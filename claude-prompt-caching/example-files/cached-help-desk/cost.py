"""Cost of 1,000 questions a day (the handbook part only)."""
# Claude Sonnet 5.5, dollars per million tokens (October 2026)
BASE, WRITE, READ = 2.00, 2.50, 0.10

HANDBOOK = 1_500    # tokens in the cached part
QUESTIONS = 1_000   # a day, all within the cache lifetime


def dollars(tokens, price):
    return tokens * price / 1_000_000


no_cache = QUESTIONS * dollars(HANDBOOK, BASE)
cached = (dollars(HANDBOOK, WRITE)
          + (QUESTIONS - 1) * dollars(HANDBOOK, READ))

print(f"No cache: ${no_cache:.2f}")
print(f"Cached:   ${cached:.2f}")
print(f"Saved:    {1 - cached / no_cache:.0%}")
