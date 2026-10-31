package agent;

import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.ContentBlock;
import com.anthropic.models.messages.ContentBlockParam;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.StopReason;
import com.anthropic.models.messages.TextBlock;
import com.anthropic.models.messages.Tool;
import com.anthropic.models.messages.ToolResultBlockParam;
import com.anthropic.models.messages.ToolUseBlock;
import java.util.ArrayList;
import java.util.List;
import java.util.function.Function;
import java.util.stream.Collectors;

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

    // The agent loop from episode 1, wrapped in one method
    public String run(String task) {
        System.out.println("[" + name + "] working...");

        // A fresh conversation: this agent sees only its own task
        MessageCreateParams.Builder chat =
            MessageCreateParams.builder()
                .model("claude-opus-5-5")
                .maxTokens(16000L)
                .system(systemPrompt)
                .addUserMessage(task);
        tools.forEach(chat::addTool);

        for (int turn = 0; turn < 10; turn++) {
            Message reply = CLIENT.messages().create(chat.build());
            chat.addMessage(reply);

            // No tool requested? Return the agent's answer.
            StopReason why = reply.stopReason().orElse(null);
            if (why != StopReason.TOOL_USE) {
                return reply.content().stream()
                        .flatMap(block -> block.text().stream())
                        .map(TextBlock::text)
                        .collect(Collectors.joining("\n"));
            }

            // Run every tool it asked for, send all results back
            List<ContentBlockParam> results = new ArrayList<>();
            for (ContentBlock block : reply.content()) {
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
        return "Stopped: too many turns";
    }
}
