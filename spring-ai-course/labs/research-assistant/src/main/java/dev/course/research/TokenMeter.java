package dev.course.research;

import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.ai.chat.client.ChatClientRequest;
import org.springframework.ai.chat.client.ChatClientResponse;
import org.springframework.ai.chat.client.advisor.ToolCallingAdvisor;
import org.springframework.ai.chat.client.advisor.api.CallAdvisor;
import org.springframework.ai.chat.client.advisor.api.CallAdvisorChain;
import org.springframework.ai.chat.messages.AssistantMessage;
import org.springframework.ai.chat.metadata.Usage;

/** Runs inside the tool loop, so it sees every model call of one agent. */
public class TokenMeter implements CallAdvisor {

    private static final Logger log = LoggerFactory.getLogger(TokenMeter.class);

    private final String agent;
    private final TokenLedger ledger;

    public TokenMeter(String agent, TokenLedger ledger) {
        this.agent = agent;
        this.ledger = ledger;
    }

    @Override
    public ChatClientResponse adviseCall(ChatClientRequest request, CallAdvisorChain chain) {
        ChatClientResponse response = chain.nextCall(request);
        Usage usage = response.chatResponse().getMetadata().getUsage();
        List<String> calls = response.chatResponse().getResult().getOutput().getToolCalls().stream()
                .map(AssistantMessage.ToolCall::name).toList();
        ledger.add(agent, usage.getPromptTokens(), usage.getCompletionTokens());
        log.info("[{}] prompt tokens: {}, next: {}", agent, usage.getPromptTokens(),
                calls.isEmpty() ? "final answer" : calls);
        return response;
    }

    @Override
    public String getName() {
        return "TokenMeter-" + agent;
    }

    @Override
    public int getOrder() {
        return ToolCallingAdvisor.DEFAULT_ORDER + 100;
    }
}
