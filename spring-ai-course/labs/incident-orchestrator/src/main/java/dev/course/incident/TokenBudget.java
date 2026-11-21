package dev.course.incident;

import java.util.concurrent.atomic.AtomicInteger;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

/** One token budget shared by every agent of the team, for one incident. */
@Component
public class TokenBudget {

    public static class ExceededException extends RuntimeException {
        ExceededException(int used, int limit) {
            super("Token budget reached: " + used + " of " + limit);
        }
    }

    private final int limit;
    private final AtomicInteger used = new AtomicInteger();

    public TokenBudget(@Value("${incident.token-budget}") int limit) {
        this.limit = limit;
    }

    /** Called before each model call: stop the team when the budget is spent. */
    public void check() {
        if (used.get() >= limit) {
            throw new ExceededException(used.get(), limit);
        }
    }

    public int add(int tokens) {
        return used.addAndGet(tokens);
    }

    public int used() {
        return used.get();
    }

    public int limit() {
        return limit;
    }

    public void reset() {
        used.set(0);
    }
}
