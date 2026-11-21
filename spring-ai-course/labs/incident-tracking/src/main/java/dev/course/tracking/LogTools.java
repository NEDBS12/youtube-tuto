package dev.course.tracking;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.annotation.ToolParam;
import org.springframework.stereotype.Component;

/** The logs of the checkout service on the day of the incident. */
@Component
public class LogTools {

    private static final List<String> LOGS = List.of(
            "13:58:12 INFO  checkout-service healthy, p95 205 ms",
            "14:01:58 INFO  Deploy v2.8.0 started",
            "14:02:31 INFO  Deploy v2.8.0 finished (cache keys renamed: product:{id} -> product:v2:{id})",
            "14:03:10 WARN  Cache miss rate high: 87%",
            "14:04:02 WARN  PostgreSQL pool exhausted (50/50), waiting for a connection",
            "14:05:15 ERROR Timeout loading product KB-100 after 2000 ms",
            "14:06:40 ERROR Timeout loading product MS-200 after 2000 ms",
            "14:07:05 INFO  Redis node healthy, 0 errors");

    @Tool(description = "Search the checkout-service logs of today. Returns the matching lines, or all lines if keyword is 'all'")
    public String searchLogs(@ToolParam(description = "A word to search for, e.g. ERROR, Deploy, Redis, or all") String keyword) {
        return LOGS.stream()
                .filter(l -> keyword.equalsIgnoreCase("all") || l.toLowerCase().contains(keyword.toLowerCase()))
                .collect(Collectors.joining("\n", "", "\n(end of logs)"));
    }
}
