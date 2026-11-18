package dev.course.orders;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AssistantController {

    private final ChatClient chatClient;
    private final OrderTools orderTools;

    public AssistantController(ChatClient.Builder builder, OrderTools orderTools) {
        this.chatClient = builder
                .defaultSystem("You are the customer assistant of a tech shop. Answer in at most two sentences.")
                .build();
        this.orderTools = orderTools;
    }

    @GetMapping("/ask")
    public String ask(@RequestParam String question) {
        return chatClient.prompt()
                .user(question)
                .tools(orderTools)
                .call()
                .content();
    }

    @GetMapping("/ask-no-tools")
    public String askWithoutTools(@RequestParam String question) {
        return chatClient.prompt()
                .user(question)
                .call()
                .content();
    }
}
