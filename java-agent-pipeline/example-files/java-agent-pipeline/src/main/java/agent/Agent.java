package agent;

import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.ContentBlockParam;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.StopReason;
import com.anthropic.models.messages.StructuredContentBlock;
import com.anthropic.models.messages.StructuredMessage;
import com.anthropic.models.messages.StructuredMessageCreateParams;
import com.anthropic.models.messages.Tool;
import com.anthropic.models.messages.ToolResultBlockParam;
import com.anthropic.models.messages.ToolUseBlock;
import java.util.ArrayList;
import java.util.List;
import java.util.function.Function;

// One agent = its own system prompt, its own tools, its own context
public class Agent {

    // Reads your key from the ANTHROPIC_API_KEY variable
    private static final AnthropicClient CLIENT =
            AnthropicOkHttpClient.fromEnv();

    private final String name;
    private final String systemPrompt;
    private final List<Tool> tools;
    private final Function<ToolUseBlock, String> toolRunner;

    public Agent(String name, String systemPrompt, List<Tool> tools,
                 Function<ToolUseBlock, String> toolRunner) {
        this.name = name;
        this.systemPrompt = systemPrompt;
        this.tools = tools;
        this.toolRunner = toolRunner;
    }

    // A plain-text answer, for agents that write for humans
    record Answer(String text) {}

    public String run(String task) {
        return run(task, Answer.class).text();
    }

    // NEW: the agent loop, with a typed answer (a Java record)
    public <T> T run(String task, Class<T> type) {
        System.out.println("[" + name + "] working...");

        // The answer must match the record: the SDK builds the schema
        StructuredMessageCreateParams.Builder<T> chat =
            MessageCreateParams.builder()
                .model("claude-opus-5-5")
                .maxTokens(16000L)
                .system(systemPrompt)
                .addUserMessage(task)
                .outputConfig(type);
        tools.forEach(chat::addTool);

        for (int turn = 0; turn < 10; turn++) {
            StructuredMessage<T> reply =
                    CLIENT.messages().create(chat.build());
            chat.addMessage(reply.rawMessage());

            // No tool requested? Return the typed answer.
            StopReason why = reply.stopReason().orElse(null);
            if (why != StopReason.TOOL_USE) {
                return reply.content().stream()
                        .flatMap(block -> block.text().stream())
                        .findFirst().orElseThrow()
                        .text();
            }

            // Run every tool it asked for, send all results back
            List<ContentBlockParam> results = new ArrayList<>();
            for (StructuredContentBlock<T> block : reply.content()) {
                block.toolUse().ifPresent(call -> {
                    System.out.println("  [" + name + "] tool: "
                            + call.name());
                    results.add(ContentBlockParam.ofToolResult(
                            ToolResultBlockParam.builder()
                                    .toolUseId(call.id())
                                    .content(toolRunner.apply(call))
                                    .build()));
                });
            }
            chat.addUserMessageOfContentBlockParams(results);
        }
        throw new IllegalStateException(name + ": too many turns");
    }
}
