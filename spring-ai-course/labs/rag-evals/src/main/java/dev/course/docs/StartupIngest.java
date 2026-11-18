package dev.course.docs;

import org.springframework.boot.CommandLineRunner;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;

@Component
public class StartupIngest implements CommandLineRunner {

    private final IngestService ingestService;
    private final JdbcTemplate jdbc;

    public StartupIngest(IngestService ingestService, JdbcTemplate jdbc) {
        this.ingestService = ingestService;
        this.jdbc = jdbc;
    }

    @Override
    public void run(String... args) {
        Integer count = jdbc.queryForObject("SELECT count(*) FROM vector_store", Integer.class);
        if (count == 0) {
            ingestService.ingest();
        }
    }
}
