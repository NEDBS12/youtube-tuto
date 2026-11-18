package dev.course.triage;

import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.prompt.ChatOptions;
import org.springframework.stereotype.Service;

@Service
public class TriageAgent {

    private static final Logger log = LoggerFactory.getLogger(TriageAgent.class);
    private static final int MAX_DRAFTS = 3;
    private static final int MAX_WORDS = 120;
    private static final String REVIEWER_MODEL = "qwen2.5:7b";

    private static final Map<Category, String> EXPERTS = Map.of(
            Category.BILLING, "You are a billing specialist. Explain charges and refunds clearly.",
            Category.TECHNICAL, "You are a technical support engineer. Give clear numbered steps.",
            Category.SHIPPING, "You are a shipping specialist. Give delivery facts and next steps.");

    private final ChatClient chatClient;

    public TriageAgent(ChatClient.Builder builder) {
        this.chatClient = builder.build();
    }

    public TicketResult handle(String ticket) {
        // 1. Routing: classify the ticket, then pick the expert
        Triage triage = chatClient.prompt()
                .system("Classify the customer support ticket.")
                .user(ticket)
                .call()
                .entity(Triage.class, spec -> spec.useProviderStructuredOutput());
        log.info("ROUTE {} (urgent: {})", triage.category(), triage.urgent());

        // 2. Evaluator-optimizer: the expert drafts, the reviewer checks, up to 3 drafts
        String reply = null;
        String feedback = "none yet";
        int drafts = 0;
        while (drafts < MAX_DRAFTS) {
            drafts++;
            reply = draft(triage.category(), ticket, feedback);
            Review review = review(ticket, reply);
            log.info("DRAFT {} approved: {} - {}", drafts, review.approved(), review.feedback());
            if (review.approved()) {
                break;
            }
            feedback = review.feedback();
        }
        return new TicketResult(triage.category(), triage.urgent(), reply, drafts);
    }

    private String draft(Category category, String ticket, String feedback) {
        return chatClient.prompt()
                .system(EXPERTS.get(category) + " Write a short, polite reply to the customer. "
                        + "Return only the reply text: no subject line, no notes, no placeholders. "
                        + "Never say you already did something (like a refund): you cannot take actions.")
                .user(u -> u.text("Ticket: {ticket}\nReviewer feedback on your last draft: {feedback}")
                        .params(Map.of("ticket", ticket, "feedback", feedback)))
                .call()
                .content();
    }

    private Review review(String ticket, String reply) {
        // Code checks what code can check: the model is bad at counting words
        int words = reply.split("\\s+").length;
        if (words > MAX_WORDS) {
            return new Review(false, "Too long: " + words + " words. Use at most " + MAX_WORDS + " words.");
        }
        return chatClient.prompt()
                .system("You review support replies. Approve only if the reply answers the ticket, "
                        + "is polite, and does not claim that an action was already done (refund, fix, shipment). "
                        + "Reject replies that talk about drafts or reviewers.")
                .user(u -> u.text("Ticket: {ticket}\nReply: {reply}")
                        .params(Map.of("ticket", ticket, "reply", reply)))
                .options(ChatOptions.builder().model(REVIEWER_MODEL).temperature(0.0))
                .call()
                .entity(Review.class, spec -> spec.useProviderStructuredOutput());
    }
}
