package dev.course.docs;

import java.util.Map;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

@RestController
public class ChatController {

    private static final int MAX_QUESTION_LENGTH = 300;

    private final DocsAssistant assistant;
    private final TokenBudget budget;

    public ChatController(DocsAssistant assistant, TokenBudget budget) {
        this.assistant = assistant;
        this.budget = budget;
    }

    @GetMapping("/ask")
    public Map<String, Object> ask(@RequestParam String q,
            @RequestHeader(name = "X-User", defaultValue = "anonymous") String user) {
        // Guardrail: limit the input before it reaches the model
        if (q.length() > MAX_QUESTION_LENGTH) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST,
                    "Question too long (max " + MAX_QUESTION_LENGTH + " characters)");
        }
        // Cost control: a token budget per user
        if (budget.exhausted(user)) {
            throw new ResponseStatusException(HttpStatus.TOO_MANY_REQUESTS, "Token budget used up for " + user);
        }
        Reply reply = assistant.ask(q);
        long used = budget.record(user, reply.tokens());
        return Map.of("answer", reply.answer(), "sources", reply.sources(), "tokensUsed", used);
    }
}
