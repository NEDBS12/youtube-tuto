package dev.course.explainer;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.Resource;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ExplainController {

    private final ChatClient chatClient;

    @Value("classpath:/prompts/system.st")
    private Resource systemPrompt;

    @Value("classpath:/prompts/explain.st")
    private Resource explainPrompt;

    public ExplainController(ChatClient.Builder builder) {
        this.chatClient = builder.build();
    }

    @PostMapping("/explain")
    public String explain(@RequestBody ExplainRequest request) {
        return chatClient.prompt()
                .system(s -> s.text(systemPrompt).param("level", request.level()))
                .user(u -> u.text(explainPrompt).param("code", request.code()))
                .call()
                .content();
    }
}
