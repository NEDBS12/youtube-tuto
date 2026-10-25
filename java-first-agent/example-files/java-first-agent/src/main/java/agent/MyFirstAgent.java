package agent;

import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.ContentBlock;
import com.anthropic.models.messages.ContentBlockParam;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.StopReason;
import com.anthropic.models.messages.ToolResultBlockParam;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class MyFirstAgent {

    public static void main(String[] args) {
        // Reads your key from the ANTHROPIC_API_KEY variable
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        System.out.print("Ask your agent: ");
        String question = new Scanner(System.in).nextLine();

        // The conversation: model, tools, and the user's question
        MessageCreateParams.Builder chat =
            MessageCreateParams.builder()
                .model("claude-opus-5-5")
                .maxTokens(16000L)
                .addTool(Tools.TIME)
                .addTool(Tools.CALCULATOR)
                .addUserMessage(question);

        // The agent loop
        while (true) {
            Message reply = client.messages().create(chat.build());
            chat.addMessage(reply); // no memory: keep the history

            for (ContentBlock block : reply.content()) {
                block.text().ifPresent(t ->
                        System.out.println("Claude: " + t.text()));
            }

            // No tool requested? Then Claude is done.
            StopReason why = reply.stopReason().orElse(null);
            if (why != StopReason.TOOL_USE) {
                break;
            }

            // Run every tool Claude asked for, send all results back
            List<ContentBlockParam> results = new ArrayList<>();
            for (ContentBlock block : reply.content()) {
                block.toolUse().ifPresent(call -> {
                    String result = Tools.run(call);
                    System.out.println("  [tool] " + call.name()
                            + " -> " + result);
                    results.add(ContentBlockParam.ofToolResult(
                            ToolResultBlockParam.builder()
                                    .toolUseId(call.id())
                                    .content(result)
                                    .build()));
                });
            }
            chat.addUserMessageOfBlockParams(results);
        }
    }
}
