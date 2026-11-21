package dev.course.research;

import java.util.Map;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AskController {

    public record Answer(String answer, Map<String, TokenLedger.Usage> tokens) {
    }

    private final ChatClient mainAgent;
    private final ChatClient soloAgent;
    private final TokenLedger ledger;

    public AskController(@Qualifier("mainAgent") ChatClient mainAgent, @Qualifier("soloAgent") ChatClient soloAgent,
            TokenLedger ledger) {
        this.mainAgent = mainAgent;
        this.soloAgent = soloAgent;
        this.ledger = ledger;
    }

    /** With a subagent: the main agent delegates the reading. */
    @GetMapping("/ask")
    public Answer ask(@RequestParam String q) {
        ledger.snapshotAndReset();
        String answer = mainAgent.prompt().user(q).call().content();
        return new Answer(answer, ledger.snapshotAndReset());
    }

    /** Without a subagent: one agent reads everything itself. */
    @GetMapping("/ask/solo")
    public Answer askSolo(@RequestParam String q) {
        ledger.snapshotAndReset();
        String answer = soloAgent.prompt().user(q).call().content();
        return new Answer(answer, ledger.snapshotAndReset());
    }
}
