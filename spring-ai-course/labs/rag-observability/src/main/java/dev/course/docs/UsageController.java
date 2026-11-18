package dev.course.docs;

import java.util.Map;

import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/** Reads the token counters Spring AI records, and turns them into a cost. */
@RestController
public class UsageController {

    private final MeterRegistry registry;

    // Ollama is free: these are example prices, to see what a paid model would cost
    @Value("${app.price.input-per-million:0.40}")
    double inputPrice;

    @Value("${app.price.output-per-million:1.60}")
    double outputPrice;

    public UsageController(MeterRegistry registry) {
        this.registry = registry;
    }

    @GetMapping("/usage")
    public Map<String, Object> usage() {
        double input = tokens("chat", "input");
        double output = tokens("chat", "output");
        double cost = (input * inputPrice + output * outputPrice) / 1_000_000;
        return Map.of(
                "chatInputTokens", (long) input,
                "chatOutputTokens", (long) output,
                "embeddingTokens", (long) tokens("embedding", "input"),
                "estimatedCostUsd", "%.6f".formatted(cost));
    }

    private double tokens(String operation, String type) {
        return registry.find("gen_ai.client.token.usage")
                .tag("gen_ai.operation.name", operation)
                .tag("gen_ai.token.type", type)
                .counters().stream()
                .mapToDouble(Counter::count)
                .sum();
    }
}
