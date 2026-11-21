package dev.course.incident;

import java.util.Map;

import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.annotation.ToolParam;
import org.springframework.stereotype.Component;

/** The metrics of the checkout service, around the incident. */
@Component
public class MetricsTools {

    private static final Map<String, String> METRICS = Map.of(
            "p95_latency", "13:50-14:02: 210 ms. 14:03: 900 ms. 14:05-14:10: 2,400 ms.",
            "cache_hit_rate", "13:50-14:02: 93%. 14:03: 12%. 14:10: 15%.",
            "db_connections", "13:50-14:02: 18 of 50. 14:04-14:10: 50 of 50 (pool full).",
            "redis_cpu", "13:50-14:10: between 8% and 11%, stable.");

    @Tool(description = "Get one metric of the checkout service around the incident. Names: p95_latency, cache_hit_rate, db_connections, redis_cpu")
    public String getMetric(@ToolParam(description = "The metric name") String name) {
        return METRICS.getOrDefault(name.trim(), "Unknown metric. Known: " + METRICS.keySet());
    }
}
