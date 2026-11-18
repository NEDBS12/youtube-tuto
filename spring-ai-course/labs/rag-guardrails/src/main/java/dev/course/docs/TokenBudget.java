package dev.course.docs;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

/** A token budget per user, so one user can't run up the bill. */
@Component
public class TokenBudget {

    private final Map<String, Long> used = new ConcurrentHashMap<>();

    @Value("${app.budget.tokens-per-user:1000}")
    long limit;

    public boolean exhausted(String user) {
        return used.getOrDefault(user, 0L) >= limit;
    }

    public long record(String user, long tokens) {
        return used.merge(user, tokens, Long::sum);
    }
}
