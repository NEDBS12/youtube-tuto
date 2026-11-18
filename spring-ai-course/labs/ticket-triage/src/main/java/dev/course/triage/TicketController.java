package dev.course.triage;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TicketController {

    private final TriageAgent agent;

    public TicketController(TriageAgent agent) {
        this.agent = agent;
    }

    @PostMapping("/tickets")
    public TicketResult handle(@RequestBody String ticket) {
        return agent.handle(ticket);
    }
}
