package agent;

import com.anthropic.core.JsonValue;
import com.anthropic.models.messages.Tool;
import com.anthropic.models.messages.ToolUseBlock;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

public class Tools {

    // 1. Plain Java methods that do the real work
    static String getCurrentTime() {
        return LocalDateTime.now().withNano(0).toString();
    }

    static String calculate(String op, double a, double b) {
        return switch (op) {
            case "add" -> String.valueOf(a + b);
            case "subtract" -> String.valueOf(a - b);
            case "multiply" -> String.valueOf(a * b);
            case "divide" -> b == 0 ? "Error: divide by zero"
                                    : String.valueOf(a / b);
            default -> "Error: unknown operation " + op;
        };
    }

    // 2. Descriptions Claude reads to decide WHEN to use a tool
    static final Tool TIME = Tool.builder()
            .name("get_current_time")
            .description("Returns the current local date and time. "
                    + "Use it for any question about now or today.")
            .inputSchema(Tool.InputSchema.builder()
                .properties(Tool.InputSchema.Properties.builder()
                    .build())
                .build())
            .build();

    static final Tool CALCULATOR = Tool.builder()
            .name("calculate")
            .description("Does exact math on two numbers. "
                    + "Use it for any arithmetic.")
            .inputSchema(Tool.InputSchema.builder()
                .properties(Tool.InputSchema.Properties.builder()
                    .putAdditionalProperty("op", JsonValue.from(Map.of(
                        "type", "string",
                        "enum", List.of("add", "subtract",
                                        "multiply", "divide"))))
                    .putAdditionalProperty("a", JsonValue.from(
                        Map.of("type", "number")))
                    .putAdditionalProperty("b", JsonValue.from(
                        Map.of("type", "number")))
                    .build())
                .required(List.of("op", "a", "b"))
                .build())
            .build();

    // 3. Run the tool Claude asked for, return the result as text
    @SuppressWarnings("unchecked")
    static String run(ToolUseBlock call) {
        Map<String, Object> in = call._input().convert(Map.class);
        return switch (call.name()) {
            case "get_current_time" -> getCurrentTime();
            case "calculate" -> calculate((String) in.get("op"),
                    ((Number) in.get("a")).doubleValue(),
                    ((Number) in.get("b")).doubleValue());
            default -> "Error: unknown tool " + call.name();
        };
    }
}
