package dev.course.incident;

import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.ai.chat.client.ChatClientRequest;
import org.springframework.ai.chat.client.ChatClientResponse;
import org.springframework.ai.chat.client.advisor.ToolCallingAdvisor;
import org.springframework.ai.chat.client.advisor.api.CallAdvisor;
import org.springframework.ai.chat.client.advisor.api.CallAdvisorChain;
import org.springframework.ai.chat.messages.AssistantMessage;

/** Inside each agent's tool loop: checks the shared budget before a call, and charges it after. */
public class BudgetAdvisor implements CallAdvisor {

    private static final Logger log = LoggerFactory.getLogger(BudgetAdvisor.class);

    private final String agent;
    private final TokenBudget budget;

    public BudgetAdvisor(String agent, TokenBudget budget) {
        this.agent = agent;
        this.budget = budget;
    }

    @Override
    public ChatClientResponse adviseCall(ChatClientRequest request, CallAdvisorChain chain) {
        budget.check();
        ChatClientResponse response = chain.nextCall(request);
        int tokens = response.chatResponse().getMetadata().getUsage().getTotalTokens();
        int total = budget.add(tokens);
        List<String> calls = response.chatResponse().getResult().getOutput().getToolCalls().stream()
                .map(AssistantMessage.ToolCall::name).toList();
        log.info("[{}] +{} tokens (team: {}/{}) -> {}", agent, tokens, total, budget.limit(),
                calls.isEmpty() ? "answer" : calls);
        return response;
    }

    @Override
    public String getName() {
        return "Budget-" + agent;
    }

    @Override
    public int getOrder() {
        return ToolCallingAdvisor.DEFAULT_ORDER + 100;
    }
}
