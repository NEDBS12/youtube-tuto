package dev.course.docs;

import java.util.List;

import org.springframework.ai.document.Document;

public record Reply(String answer, List<Document> documents, long tokens) {

    public List<String> sources() {
        return documents.stream()
                .map(d -> (d.getMetadata().get("file_name") + " " + d.getMetadata().getOrDefault("page_number", "")).strip())
                .distinct()
                .toList();
    }
}
