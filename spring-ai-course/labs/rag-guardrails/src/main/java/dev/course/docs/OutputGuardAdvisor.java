package dev.course.docs;

import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.ai.chat.client.ChatClientRequest;
import org.springframework.ai.chat.client.ChatClientResponse;
import org.springframework.ai.chat.client.advisor.api.CallAdvisor;
import org.springframework.ai.chat.client.advisor.api.CallAdvisorChain;
import org.springframework.ai.chat.messages.AssistantMessage;
import org.springframework.ai.chat.model.ChatResponse;
import org.springframework.ai.chat.model.Generation;
import org.springframework.core.Ordered;

/** Checks every answer before it leaves the app. */
public class OutputGuardAdvisor implements CallAdvisor {

    private static final Logger log = LoggerFactory.getLogger(OutputGuardAdvisor.class);

    private static final Pattern EMAIL = Pattern.compile("[\\w.+-]+@([\\w-]+\\.)+[\\w-]+");
    private static final String ALLOWED_DOMAIN = "@brightwave.example";
    private static final String BLOCKED = "Sorry, I can't give that answer. Please contact people@brightwave.example.";

    @Override
    public ChatClientResponse adviseCall(ChatClientRequest request, CallAdvisorChain chain) {
        ChatClientResponse response = chain.nextCall(request);
        String answer = response.chatResponse().getResult().getOutput().getText();
        String problem = check(answer);
        if (problem == null) {
            return response;
        }
        log.warn("BLOCKED answer ({}): {}", problem, answer);
        ChatResponse blocked = ChatResponse.builder()
                .from(response.chatResponse())
                .generations(List.of(new Generation(new AssistantMessage(BLOCKED))))
                .build();
        return response.mutate().chatResponse(blocked).build();
    }

    private static String check(String answer) {
        Matcher email = EMAIL.matcher(answer);
        while (email.find()) {
            if (!email.group().endsWith(ALLOWED_DOMAIN)) {
                return "unknown email " + email.group();
            }
        }
        String text = answer.toLowerCase();
        if (text.contains("password") && text.contains("send")) {
            return "asks for a password";
        }
        return null;
    }

    @Override
    public String getName() {
        return "OutputGuardAdvisor";
    }

    @Override
    public int getOrder() {
        return Ordered.HIGHEST_PRECEDENCE; // first in, last out: it sees the final answer
    }
}
