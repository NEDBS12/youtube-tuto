package dev.course.sales;

import org.springaicommunity.agent.common.task.subagent.SubagentReference;
import org.springaicommunity.agent.common.task.subagent.SubagentType;
import org.springaicommunity.agent.subagent.a2a.A2ASubagentDefinition;
import org.springaicommunity.agent.subagent.a2a.A2ASubagentExecutor;
import org.springaicommunity.agent.subagent.a2a.A2ASubagentResolver;
import org.springaicommunity.agent.tools.task.TaskTool;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.tool.ToolCallback;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class AgentConfig {

    @Bean
    ChatClient salesAgent(ChatClient.Builder builder, @Value("${sales.inventory-agent-url}") String inventoryUrl) {

        // A remote agent, used like a subagent: the resolver reads its agent card at startup,
        // the executor sends it A2A messages over JSON-RPC.
        ToolCallback taskTool = TaskTool.builder()
                .subagentTypes(new SubagentType(new A2ASubagentResolver(), new A2ASubagentExecutor()))
                .subagentReferences(new SubagentReference(inventoryUrl, A2ASubagentDefinition.KIND))
                // a short description instead of the long built-in one: small models follow it better
                .taskDescriptionTemplate("""
                        Send a task to a remote agent and get its answer. Use it before you answer,
                        whenever the question needs what an agent knows. Available agents:
                        %s""")
                .build();

        return builder
                .defaultSystem("""
                        You are the sales assistant of the Brightwave shop. Products:
                        KB-100 MX-100 mechanical keyboard, 89 EUR. MS-200 Glide wireless mouse, 39 EUR.
                        HS-300 Studio headset, 129 EUR.
                        You don't know the stock. For any question about stock, availability or delivery,
                        FIRST call the Task tool with subagent_type "Inventory Agent" and ask about the SKU.
                        Never ask the customer whether you should check: check, then answer.
                        Answer the customer in at most two sentences.""")
                .defaultToolCallbacks(taskTool)
                .defaultAdvisors(new AgentLog())
                .build();
    }
}
