package dev.course.advisors;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.ai.chat.client.ChatClientRequest;
import org.springframework.ai.chat.client.ChatClientResponse;
import org.springframework.ai.chat.client.advisor.api.CallAdvisor;
import org.springframework.ai.chat.client.advisor.api.CallAdvisorChain;

public class TimingAdvisor implements CallAdvisor {

    private static final Logger log = LoggerFactory.getLogger(TimingAdvisor.class);

    @Override
    public ChatClientResponse adviseCall(ChatClientRequest request, CallAdvisorChain chain) {
        long start = System.currentTimeMillis();
        ChatClientResponse response = chain.nextCall(request);
        long millis = System.currentTimeMillis() - start;
        var usage = response.chatResponse().getMetadata().getUsage();
        log.info("AI call took {} ms, {} tokens", millis, usage.getTotalTokens());
        return response;
    }

    @Override
    public String getName() {
        return "TimingAdvisor";
    }

    @Override
    public int getOrder() {
        return 0;
    }
}
