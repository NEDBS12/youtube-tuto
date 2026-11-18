package dev.course.options;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.model.ChatResponse;
import org.springframework.ai.chat.prompt.ChatOptions;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TaglineController {

    private final ChatClient chatClient;

    public TaglineController(ChatClient.Builder builder) {
        this.chatClient = builder.build();
    }

    @GetMapping("/tagline")
    public Tagline tagline(@RequestParam String product,
                           @RequestParam(defaultValue = "0.7") double temperature) {
        ChatResponse response = chatClient.prompt()
                .user("Write one short marketing tagline for: " + product + ". Reply with the tagline only.")
                .options(ChatOptions.builder()
                        .temperature(temperature)
                        .maxTokens(30))
                .call()
                .chatResponse();
        return new Tagline(response.getMetadata().getModel(), temperature,
                response.getResult().getOutput().getText());
    }
}
