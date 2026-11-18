package dev.course.store;

import java.util.List;

import org.springframework.ai.vectorstore.SearchRequest;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ProductController {

    private final VectorStore vectorStore;

    public ProductController(VectorStore vectorStore) {
        this.vectorStore = vectorStore;
    }

    @GetMapping("/products/search")
    public List<ProductHit> search(@RequestParam String q,
                                   @RequestParam(required = false) String filter) {
        SearchRequest.Builder request = SearchRequest.builder()
                .query(q)
                .topK(3)
                .similarityThreshold(0.5);
        if (filter != null) {
            request.filterExpression(filter);  // e.g. "category == 'audio' && price < 100"
        }
        return vectorStore.similaritySearch(request.build()).stream()
                .map(d -> new ProductHit(d.getText(), d.getMetadata().get("category"),
                        d.getMetadata().get("price"), d.getScore()))
                .toList();
    }
}
