package dev.course.faq;

import java.util.Comparator;
import java.util.List;
import java.util.stream.IntStream;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.ai.embedding.EmbeddingModel;
import org.springframework.stereotype.Service;

@Service
public class FaqService {

    private static final Logger log = LoggerFactory.getLogger(FaqService.class);

    private static final List<String> FAQS = List.of(
            "How do I reset my password? Click 'Forgot password' on the login page.",
            "What is your refund policy? You can return any item within 30 days for a full refund.",
            "How long does shipping take? Standard delivery takes 3 to 5 business days.",
            "Do you ship abroad? Yes, we ship to 40 countries in Europe and North America.",
            "How do I change my delivery address? Edit it in your account before the order ships.",
            "Which payment methods do you accept? Visa, Mastercard, PayPal and Apple Pay.",
            "How do I contact support? Use the chat on our website, from 9am to 6pm.",
            "Can I cancel my subscription? Yes, anytime, from the billing page of your account.");

    private final EmbeddingModel embeddingModel;
    private final List<float[]> vectors;

    public FaqService(EmbeddingModel embeddingModel) {
        this.embeddingModel = embeddingModel;
        this.vectors = embeddingModel.embed(FAQS);
        log.info("Embedded {} FAQs, {} dimensions each", vectors.size(), vectors.get(0).length);
    }

    public List<Match> search(String query) {
        float[] q = embeddingModel.embed(query);
        return IntStream.range(0, FAQS.size())
                .mapToObj(i -> new Match(Similarity.cosine(q, vectors.get(i)), FAQS.get(i)))
                .sorted(Comparator.comparingDouble(Match::score).reversed())
                .limit(3)
                .toList();
    }

    public double similarity(String a, String b) {
        double score = Similarity.cosine(embeddingModel.embed(a), embeddingModel.embed(b));
        return Math.round(score * 100) / 100.0;
    }
}
