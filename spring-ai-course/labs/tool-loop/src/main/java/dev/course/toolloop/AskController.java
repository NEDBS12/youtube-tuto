package dev.course.toolloop;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.memory.ChatMemory;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AskController {

    private final ChatClient chatClient;

    public AskController(ChatClient chatClient) {
        this.chatClient = chatClient;
    }

    @GetMapping("/ask")
    public String ask(@RequestParam String question, @RequestParam String session) {
        return chatClient.prompt()
                .user(question)
                .advisors(a -> a.param(ChatMemory.CONVERSATION_ID, session))
                .call()
                .content();
    }
}
