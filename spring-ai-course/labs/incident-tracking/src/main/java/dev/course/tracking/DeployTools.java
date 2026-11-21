package dev.course.tracking;

import org.springframework.ai.tool.annotation.Tool;
import org.springframework.stereotype.Component;

/** The deployment history. */
@Component
public class DeployTools {

    @Tool(description = "List the recent deployments of the checkout service, newest first")
    public String listDeploys() {
        return """
                v2.8.0  today 14:02  by Sam   "Rename the product cache keys to product:v2:{id}"
                v2.7.3  2026-11-12   by Lena  "Add jitter to the cache TTL"
                v2.7.2  2026-10-17   by Sam   "Evict prices on price-changed events"
                """;
    }
}
