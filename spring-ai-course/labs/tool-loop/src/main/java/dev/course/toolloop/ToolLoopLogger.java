package dev.course.toolloop;

import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.ai.chat.client.ChatClientRequest;
import org.springframework.ai.chat.client.ChatClientResponse;
import org.springframework.ai.chat.client.advisor.ToolCallingAdvisor;
import org.springframework.ai.chat.client.advisor.api.CallAdvisor;
import org.springframework.ai.chat.client.advisor.api.CallAdvisorChain;
import org.springframework.ai.chat.messages.AssistantMessage;
import org.springframework.ai.model.tool.ToolCallingChatOptions;

public class ToolLoopLogger implements CallAdvisor {

    private static final Logger log = LoggerFactory.getLogger(ToolLoopLogger.class);

    @Override
    public ChatClientResponse adviseCall(ChatClientRequest request, CallAdvisorChain chain) {
        int offered = request.prompt().getOptions() instanceof ToolCallingChatOptions options
                ? options.getToolCallbacks().size() : 0;
        ChatClientResponse response = chain.nextCall(request);
        List<String> calls = response.chatResponse().getResult().getOutput().getToolCalls().stream()
                .map(AssistantMessage.ToolCall::name).toList();
        int promptTokens = response.chatResponse().getMetadata().getUsage().getPromptTokens();
        log.info("LOOP tools offered: {}, prompt tokens: {}, model asked for: {}",
                offered, promptTokens, calls.isEmpty() ? "final answer" : calls);
        return response;
    }

    @Override
    public String getName() {
        return "ToolLoopLogger";
    }

    @Override
    public int getOrder() {
        return ToolCallingAdvisor.DEFAULT_ORDER + 100;
    }
}
