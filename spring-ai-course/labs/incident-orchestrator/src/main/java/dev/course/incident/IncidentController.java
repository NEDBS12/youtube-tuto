package dev.course.incident;

import dev.course.incident.Records.IncidentReport;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class IncidentController {

    private final Orchestrator orchestrator;

    public IncidentController(Orchestrator orchestrator) {
        this.orchestrator = orchestrator;
    }

    @PostMapping("/incidents")
    public IncidentReport investigate(@RequestBody String incident) {
        return orchestrator.handle(incident);
    }
}
