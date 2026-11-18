package dev.course.docs;

import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class StartupIngest implements CommandLineRunner {

    private final IngestService ingestService;

    public StartupIngest(IngestService ingestService) {
        this.ingestService = ingestService;
    }

    @Override
    public void run(String... args) {
        // Ingest on every start: the guardrail settings change what gets stored
        ingestService.ingest();
    }
}
