package dev.course.inventory;

import java.util.List;

import org.a2aproject.sdk.server.agentexecution.AgentExecutor;
import org.a2aproject.sdk.spec.AgentCapabilities;
import org.a2aproject.sdk.spec.AgentCard;
import org.a2aproject.sdk.spec.AgentInterface;
import org.a2aproject.sdk.spec.AgentSkill;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springaicommunity.a2a.server.executor.DefaultAgentExecutor;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class A2AConfig {

    private static final Logger log = LoggerFactory.getLogger(A2AConfig.class);

    /** The agent card: what this agent can do, and where to reach it. Served at /.well-known/agent-card.json */
    @Bean
    AgentCard agentCard(@Value("${server.port}") int port) {
        return AgentCard.builder()
                .name("Inventory Agent")
                .description("Knows the stock of every Brightwave product in the Lyon and Berlin warehouses.")
                .version("1.0.0")
                .capabilities(AgentCapabilities.builder().streaming(false).build())
                .defaultInputModes(List.of("text"))
                .defaultOutputModes(List.of("text"))
                .skills(List.of(AgentSkill.builder()
                        .id("check-stock")
                        .name("Check stock")
                        .description("Stock per warehouse and restock date for a product SKU")
                        .tags(List.of("inventory", "stock"))
                        .examples(List.of("Is KB-100 in stock?", "When is HS-300 back in Lyon?"))
                        .build()))
                .supportedInterfaces(List.of(new AgentInterface("JSONRPC", "http://localhost:" + port)))
                .build();
    }

    /** What happens when a message arrives: a normal Spring AI ChatClient, with the warehouse tool. */
    @Bean
    AgentExecutor agentExecutor(ChatClient.Builder builder, StockTools stockTools) {
        ChatClient chatClient = builder
                .defaultSystem("""
                        You are the inventory agent of Brightwave. Use the checkStock tool for every product.
                        Answer with the stock per warehouse and the restock date. Be short.""")
                .defaultTools(stockTools)
                .build();

        return new DefaultAgentExecutor(chatClient, (chat, context) -> {
            String question = DefaultAgentExecutor.extractTextFromMessage(context.getMessage());
            log.info("A2A task {} received: {}", context.getTaskId(), question);
            return chat.prompt().user(question).call().content();
        });
    }
}
