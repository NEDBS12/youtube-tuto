package dev.course.toolloop;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class AiConfig {

    @Bean
    ChatClient chatClient(ChatClient.Builder builder, ShopTools shopTools) {
        return builder
                .defaultSystem("You are the assistant of a tech shop. Answer in at most two sentences.")
                .defaultTools(shopTools)
                .defaultAdvisors(new ToolLoopLogger())
                .build();
    }
}
