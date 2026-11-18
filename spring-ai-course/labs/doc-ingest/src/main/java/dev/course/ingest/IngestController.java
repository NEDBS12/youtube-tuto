package dev.course.ingest;

import java.util.List;
import java.util.Map;

import org.springframework.ai.vectorstore.SearchRequest;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class IngestController {

    private final IngestService ingestService;
    private final VectorStore vectorStore;

    public IngestController(IngestService ingestService, VectorStore vectorStore) {
        this.ingestService = ingestService;
        this.vectorStore = vectorStore;
    }

    @PostMapping("/ingest")
    public IngestReport ingest() {
        return ingestService.ingest();
    }

    @GetMapping("/search")
    public List<Map<String, Object>> search(@RequestParam String q) {
        return vectorStore.similaritySearch(SearchRequest.builder().query(q).topK(2).build()).stream()
                .map(d -> Map.<String, Object>of("text", d.getText(), "source", d.getMetadata().get("file_name")))
                .toList();
    }
}
