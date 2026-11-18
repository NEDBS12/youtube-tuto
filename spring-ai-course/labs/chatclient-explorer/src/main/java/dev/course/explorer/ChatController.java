package dev.course.explorer;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.model.ChatResponse;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ChatController {

    private final ChatClient chatClient;

    public ChatController(ChatClient chatClient) {
        this.chatClient = chatClient;
    }

    @GetMapping("/chat")
    public String chat(@RequestParam String message) {
        return chatClient.prompt().user(message).call().content();
    }

    @GetMapping("/chat/details")
    public ChatDetails details(@RequestParam String message) {
        ChatResponse response = chatClient.prompt().user(message).call().chatResponse();
        var usage = response.getMetadata().getUsage();
        return new ChatDetails(
                response.getResult().getOutput().getText(),
                response.getMetadata().getModel(),
                usage.getPromptTokens(), usage.getCompletionTokens(), usage.getTotalTokens());
    }

    @GetMapping("/chat/pirate")
    public String pirate(@RequestParam String message) {
        return chatClient.prompt()
                .system("You are a friendly pirate. Answer in one sentence, in pirate speak.")
                .user(message)
                .call()
                .content();
    }
}
