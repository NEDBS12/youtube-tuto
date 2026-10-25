package agent;

import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;

// A plain chatbot: one question, one answer, no tools
public class NoTools {

    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        Message reply = client.messages().create(
            MessageCreateParams.builder()
                .model("claude-opus-5-5")
                .maxTokens(16000L)
                .addUserMessage("What time is it right now?")
                .build());

        reply.content().forEach(block -> block.text().ifPresent(t ->
                System.out.println("Claude: " + t.text())));
    }
}
