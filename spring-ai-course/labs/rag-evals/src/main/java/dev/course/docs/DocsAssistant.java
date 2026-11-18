package dev.course.docs;

import java.util.List;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.client.ChatClientResponse;
import org.springframework.ai.document.Document;
import org.springframework.ai.rag.advisor.RetrievalAugmentationAdvisor;
import org.springframework.ai.rag.generation.augmentation.ContextualQueryAugmenter;
import org.springframework.ai.rag.retrieval.search.VectorStoreDocumentRetriever;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.stereotype.Service;

/** The RAG app from lab 4.4, as a service we can test. */
@Service
public class DocsAssistant {

    private final ChatClient chatClient;

    public DocsAssistant(ChatClient.Builder builder, VectorStore vectorStore) {
        this.chatClient = builder
                .defaultSystem("Answer in one complete sentence that repeats the subject of the question.")
                .defaultAdvisors(RetrievalAugmentationAdvisor.builder()
                        .documentRetriever(VectorStoreDocumentRetriever.builder()
                                .vectorStore(vectorStore)
                                .topK(5)
                                .similarityThreshold(0.5)
                                .build())
                        .queryAugmenter(ContextualQueryAugmenter.builder().allowEmptyContext(false).build())
                        .build())
                .build();
    }

    @SuppressWarnings("unchecked")
    public Reply ask(String question) {
        ChatClientResponse response = chatClient.prompt().user(question).call().chatClientResponse();
        List<Document> documents = (List<Document>) response.context()
                .getOrDefault(RetrievalAugmentationAdvisor.DOCUMENT_CONTEXT, List.of());
        return new Reply(response.chatResponse().getResult().getOutput().getText(), documents);
    }
}
