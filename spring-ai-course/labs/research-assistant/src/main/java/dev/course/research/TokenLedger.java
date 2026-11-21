package dev.course.research;

import java.util.Map;
import java.util.TreeMap;

import org.springframework.stereotype.Component;

/** Counts model calls and tokens per agent, for the current question. */
@Component
public class TokenLedger {

    public record Usage(int calls, int promptTokens, int completionTokens, int largestPrompt) {
    }

    private final Map<String, Usage> usage = new TreeMap<>();

    public synchronized void add(String agent, int prompt, int completion) {
        Usage u = usage.getOrDefault(agent, new Usage(0, 0, 0, 0));
        usage.put(agent, new Usage(u.calls() + 1, u.promptTokens() + prompt,
                u.completionTokens() + completion, Math.max(u.largestPrompt(), prompt)));
    }

    public synchronized Map<String, Usage> snapshotAndReset() {
        Map<String, Usage> copy = new TreeMap<>(usage);
        usage.clear();
        return copy;
    }
}
