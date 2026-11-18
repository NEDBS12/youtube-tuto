package dev.course.docs;

import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.client.ChatClientResponse;
import org.springframework.ai.chat.client.advisor.api.Advisor;
import org.springframework.ai.chat.client.advisor.vectorstore.QuestionAnswerAdvisor;
import org.springframework.ai.document.Document;
import org.springframework.ai.rag.advisor.RetrievalAugmentationAdvisor;
import org.springframework.ai.rag.generation.augmentation.ContextualQueryAugmenter;
import org.springframework.ai.rag.retrieval.search.VectorStoreDocumentRetriever;
import org.springframework.ai.vectorstore.SearchRequest;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ChatController {

    private static final Logger log = LoggerFactory.getLogger(ChatController.class);

    private final ChatClient chatClient;
    private final Advisor qaAdvisor;
    private final Advisor ragAdvisor;

    public ChatController(ChatClient.Builder builder, VectorStore vectorStore) {
        this.chatClient = builder.build();

        // Simple RAG: search, then add the documents to the prompt
        this.qaAdvisor = QuestionAnswerAdvisor.builder(vectorStore)
                .searchRequest(SearchRequest.builder().topK(5).similarityThreshold(0.5).build())
                .build();

        // Modular RAG: every step is a building block you can swap
        this.ragAdvisor = RetrievalAugmentationAdvisor.builder()
                .documentRetriever(VectorStoreDocumentRetriever.builder()
                        .vectorStore(vectorStore)
                        .topK(5)
                        .similarityThreshold(0.5)
                        .build())
                .queryAugmenter(ContextualQueryAugmenter.builder()
                        .allowEmptyContext(false)
                        .build())
                .build();
    }

    @GetMapping("/ask/plain")
    public String plain(@RequestParam String q) {
        return chatClient.prompt().user(q).call().content();
    }

    @GetMapping("/ask/qa")
    public Answer qa(@RequestParam String q) {
        return ask(q, qaAdvisor, QuestionAnswerAdvisor.RETRIEVED_DOCUMENTS);
    }

    @GetMapping("/ask/rag")
    public Answer rag(@RequestParam String q) {
        return ask(q, ragAdvisor, RetrievalAugmentationAdvisor.DOCUMENT_CONTEXT);
    }

    @SuppressWarnings("unchecked")
    private Answer ask(String question, Advisor advisor, String documentsKey) {
        ChatClientResponse response = chatClient.prompt()
                .user(question)
                .advisors(advisor)
                .call()
                .chatClientResponse();
        List<Document> documents = (List<Document>) response.context().getOrDefault(documentsKey, List.of());
        documents.forEach(d -> log.info("RETRIEVED {} {}...", "%.2f".formatted(d.getScore()), "%.40s".formatted(d.getText())));
        List<String> sources = documents.stream()
                .map(d -> d.getMetadata().get("file_name") + " " + d.getMetadata().getOrDefault("page_number", ""))
                .map(String::strip)
                .toList();
        return new Answer(response.chatResponse().getResult().getOutput().getText(), sources);
    }
}
