package dev.course.research;

import java.nio.file.Path;
import java.util.Arrays;
import java.util.List;
import java.util.Set;

import org.springaicommunity.agent.tools.FileSystemTools;
import org.springaicommunity.agent.tools.GlobTool;
import org.springaicommunity.agent.tools.task.TaskTool;
import org.springaicommunity.agent.tools.task.claude.ClaudeSubagentReferences;
import org.springaicommunity.agent.tools.task.claude.ClaudeSubagentType;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.tool.ToolCallback;
import org.springframework.ai.tool.method.MethodToolCallbackProvider;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class AgentConfig {

    /** Baseline: one agent reads every file itself, so all the text lands in its own context. */
    @Bean
    ChatClient soloAgent(ChatClient.Builder builder, TokenLedger ledger, @Value("${research.docs-dir}") String docsDir) {
        Path docs = Path.of(docsDir).toAbsolutePath();
        List<ToolCallback> readOnly = Arrays.stream(MethodToolCallbackProvider.builder()
                        .toolObjects(FileSystemTools.builder().allowedDirectory(docs).build(), GlobTool.builder().build())
                        .build().getToolCallbacks())
                .filter(t -> Set.of("Read", "Glob").contains(t.getToolDefinition().name()))
                .toList();

        return builder.clone()
                .defaultSystem("""
                        You are the research assistant of the checkout team.
                        The project documents are in the folder %s.
                        1. Call Glob with that folder and the pattern **/*.md to list the documents.
                        2. Call Read on every file, using its absolute path.
                        3. Answer in at most 5 bullet points, with the source file name of each fact in brackets.
                        """.formatted(docs))
                .defaultToolCallbacks(readOnly)
                .defaultAdvisors(new TokenMeter("solo", ledger))
                .build();
    }

    /** Main agent: no file tools. It delegates the reading to the doc-researcher subagent. */
    @Bean
    ChatClient mainAgent(ChatClient.Builder builder, TokenLedger ledger,
            @Value("${research.docs-dir}") String docsDir, @Value("${research.agents-dir}") String agentsDir) {

        ToolCallback taskTool = TaskTool.builder()
                .subagentTypes(ClaudeSubagentType.builder()
                        .chatClientBuilder("default", builder.clone()
                                .defaultAdvisors(new TokenMeter("subagent", ledger)))
                        .build())
                .subagentReferences(ClaudeSubagentReferences.fromRootDirectory(agentsDir))
                .build();

        return builder.clone()
                .defaultSystem("""
                        You are the research assistant of the checkout team.
                        The project documents are in the folder %s.
                        You cannot read files yourself. For every question about the project, call the Task tool
                        with subagent_type "doc-researcher". In its prompt, give the folder path and the full question.
                        Then answer the user from its findings, in at most 5 bullet points, keeping the file names.
                        """.formatted(Path.of(docsDir).toAbsolutePath()))
                .defaultToolCallbacks(taskTool)
                .defaultAdvisors(new TokenMeter("main", ledger))
                .build();
    }
}
