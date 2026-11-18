package dev.course.store;

import java.util.List;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.ai.document.Document;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.boot.CommandLineRunner;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;

@Component
public class CatalogLoader implements CommandLineRunner {

    private static final Logger log = LoggerFactory.getLogger(CatalogLoader.class);

    private final VectorStore vectorStore;
    private final JdbcTemplate jdbc;

    public CatalogLoader(VectorStore vectorStore, JdbcTemplate jdbc) {
        this.vectorStore = vectorStore;
        this.jdbc = jdbc;
    }

    @Override
    public void run(String... args) {
        Integer count = jdbc.queryForObject("SELECT count(*) FROM vector_store", Integer.class);
        if (count > 0) {
            log.info("Store already has {} products, nothing to load", count);
            return;
        }
        List<Document> products = List.of(
                product("Wireless noise-cancelling headphones, 30 hours of battery", "audio", 199),
                product("Compact Bluetooth earbuds with a charging case", "audio", 59),
                product("Waterproof portable speaker for the beach and the pool", "audio", 79),
                product("Ergonomic mechanical keyboard with quiet switches", "computer", 129),
                product("Vertical mouse that reduces wrist pain", "computer", 45),
                product("27-inch 4K monitor for photo editing", "computer", 349),
                product("Trail running shoes with extra grip", "sport", 119),
                product("Yoga mat, non-slip and easy to clean", "sport", 35),
                product("Insulated steel water bottle, keeps drinks cold for 24 hours", "sport", 25),
                product("Smart watch with heart-rate and sleep tracking", "sport", 249));
        vectorStore.add(products);
        log.info("Added {} products to the vector store", products.size());
    }

    private static Document product(String text, String category, int price) {
        return new Document(text, Map.of("category", category, "price", price));
    }
}
