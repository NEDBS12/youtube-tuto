package dev.course.docs;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.evaluation.FactCheckingEvaluator;
import org.springframework.ai.chat.evaluation.RelevancyEvaluator;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.chat.prompt.ChatOptions;
import org.springframework.ai.evaluation.EvaluationRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

// Starts the real app: PGVector (Docker Compose), the ingestion and Ollama
@SpringBootTest(properties = "spring.docker.compose.skip.in-tests=false")
class DocsAssistantEvaluationTest {

    private static final Logger log = LoggerFactory.getLogger(DocsAssistantEvaluationTest.class);

    // The judge is a different, bigger model than the one that answers (gemma3:4b)
    private static final String JUDGE_MODEL = "qwen2.5:7b";

    // The default prompt lets the judge explain itself ("Yes. The document states...").
    // The evaluator only passes on a bare "yes", so we ask for one word.
    private static final String FACT_CHECK_PROMPT = """
            Evaluate whether or not the following claim is supported by the provided document.
            Respond with one word only: "yes" if the claim is supported, or "no" if it is not.

            Document:
            {document}

            Claim:
            {claim}
            """;

    @Autowired
    DocsAssistant assistant;

    @Autowired
    ChatModel chatModel;

    RelevancyEvaluator relevancy;
    FactCheckingEvaluator factChecking;

    @BeforeEach
    void createJudges() {
        ChatClient.Builder judge = ChatClient.builder(chatModel)
                .defaultOptions(ChatOptions.builder().model(JUDGE_MODEL).temperature(0.0));
        relevancy = RelevancyEvaluator.builder().chatClientBuilder(judge).build();
        factChecking = FactCheckingEvaluator.builder(judge).evaluationPrompt(FACT_CHECK_PROMPT).build();
    }

    @ParameterizedTest
    @CsvSource(delimiter = '|', value = {
            "How many vacation days do full-time employees get? | 27",
            "How much is the home office budget?                | 500",
            "Which day must everyone come to the office?        | Tuesday",
            "How many characters does a new password need?      | 14",
            "I lost my laptop. Which extension do I call?       | 4400",
            "How much is a meal covered on a business trip?     | 25"
    })
    void answersFromTheDocuments(String question, String expected) {
        Reply reply = assistant.ask(question);
        log.info("Q: {} | A: {} | sources: {}", question, reply.answer(), reply.sources());

        // 1. A plain assertion: cheap, and deterministic
        assertThat(reply.answer()).contains(expected);

        // 2. LLM as a judge: is the answer relevant, and supported by the documents?
        EvaluationRequest request = new EvaluationRequest(question, reply.documents(), reply.answer());
        assertThat(relevancy.evaluate(request).isPass()).as("relevancy").isTrue();
        assertThat(factChecking.evaluate(request).isPass()).as("fact checking").isTrue();
    }

    @Test
    void declinesQuestionsOutsideTheDocuments() {
        Reply reply = assistant.ask("What is the capital of Australia?");
        log.info("Out of scope | A: {}", reply.answer());

        assertThat(reply.documents()).isEmpty();
        assertThat(reply.answer()).doesNotContain("Canberra");
    }

    @Test
    void judgeCatchesAHallucination() {
        String question = "How many vacation days do full-time employees get?";
        Reply reply = assistant.ask(question);

        // Same documents, but a made-up answer: the judge must say no
        EvaluationRequest wrong = new EvaluationRequest(question, reply.documents(),
                "Full-time employees get 35 vacation days per year.");
        assertThat(factChecking.evaluate(wrong).isPass()).isFalse();
    }
}
