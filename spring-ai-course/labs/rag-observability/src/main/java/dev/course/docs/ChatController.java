package dev.course.docs;

import java.util.Map;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ChatController {

    private final DocsAssistant assistant;

    public ChatController(DocsAssistant assistant) {
        this.assistant = assistant;
    }

    @GetMapping("/ask")
    public Map<String, Object> ask(@RequestParam String q) {
        Reply reply = assistant.ask(q);
        return Map.of("answer", reply.answer(), "sources", reply.sources(),
                "tokens", Map.of("input", reply.usage().getPromptTokens(), "output", reply.usage().getCompletionTokens()));
    }
}
