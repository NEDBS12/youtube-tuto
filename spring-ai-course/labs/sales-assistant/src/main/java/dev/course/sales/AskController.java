package dev.course.sales;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AskController {

    private final ChatClient salesAgent;

    public AskController(ChatClient salesAgent) {
        this.salesAgent = salesAgent;
    }

    @GetMapping("/ask")
    public String ask(@RequestParam String q) {
        return salesAgent.prompt().user(q).call().content();
    }
}
