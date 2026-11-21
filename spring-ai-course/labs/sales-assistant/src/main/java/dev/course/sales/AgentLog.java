package dev.course.sales;

import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.ai.chat.client.ChatClientRequest;
import org.springframework.ai.chat.client.ChatClientResponse;
import org.springframework.ai.chat.client.advisor.ToolCallingAdvisor;
import org.springframework.ai.chat.client.advisor.api.CallAdvisor;
import org.springframework.ai.chat.client.advisor.api.CallAdvisorChain;
import org.springframework.ai.chat.messages.AssistantMessage;

/** Logs each step of the tool loop: which tool the model calls, with which arguments. */
public class AgentLog implements CallAdvisor {

    private static final Logger log = LoggerFactory.getLogger(AgentLog.class);

    @Override
    public ChatClientResponse adviseCall(ChatClientRequest request, CallAdvisorChain chain) {
        ChatClientResponse response = chain.nextCall(request);
        List<AssistantMessage.ToolCall> calls = response.chatResponse().getResult().getOutput().getToolCalls();
        if (calls.isEmpty()) {
            log.info("[sales] final answer");
        }
        calls.forEach(c -> log.info("[sales] calls {} {}", c.name(), c.arguments()));
        return response;
    }

    @Override
    public String getName() {
        return "AgentLog";
    }

    @Override
    public int getOrder() {
        return ToolCallingAdvisor.DEFAULT_ORDER + 100;
    }
}
