package dev.course.tracking;

import java.util.Map;

import dev.course.tracking.Records.Workers;
import io.micrometer.core.instrument.MeterRegistry;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/** The team: a planner, three specialist workers with their own tools, a writer and a reviewer. */
@Configuration
public class TeamConfig {

    @Bean
    ChatClient planner(ChatClient.Builder builder, TokenBudget budget, MeterRegistry meters) {
        return builder.clone()
                .defaultSystem("""
                        You are the incident commander. Plan the investigation of the incident.
                        Workers: "logs" reads the service logs, "metrics" reads the metrics,
                        "deploys" lists the recent deployments.
                        Return one step per worker you need (2 or 3 steps), each with one precise question.""")
                .defaultAdvisors(new BudgetAdvisor("planner", budget, meters))
                .build();
    }

    /** The workers, by name. Each one only has its own tool. */
    @Bean
    Workers workers(ChatClient.Builder builder, TokenBudget budget, MeterRegistry meters,
            LogTools logTools, MetricsTools metricsTools, DeployTools deployTools) {
        return new Workers(Map.of(
                "logs", worker(builder, budget, meters, "logs", "You read the checkout-service logs with searchLogs.", logTools),
                "metrics", worker(builder, budget, meters, "metrics", "You read the metrics with getMetric.", metricsTools),
                "deploys", worker(builder, budget, meters, "deploys", "You list the deployments with listDeploys.", deployTools)));
    }

    private static ChatClient worker(ChatClient.Builder builder, TokenBudget budget, MeterRegistry meters, String name, String role, Object tools) {
        return builder.clone()
                .defaultSystem(role + " Answer the question with facts and times from your tool only. At most 4 sentences.")
                .defaultTools(tools)
                .defaultAdvisors(new BudgetAdvisor(name, budget, meters))
                .build();
    }

    @Bean
    ChatClient writer(ChatClient.Builder builder, TokenBudget budget, MeterRegistry meters) {
        return builder.clone()
                .defaultSystem("""
                        You write incident reports from the findings of the investigation, and nothing else.
                        Sections: Summary, Root cause (with the evidence), Immediate fix, Follow-up.
                        At most 150 words.""")
                .defaultAdvisors(new BudgetAdvisor("writer", budget, meters))
                .build();
    }

    @Bean
    ChatClient reviewer(ChatClient.Builder builder, TokenBudget budget, MeterRegistry meters) {
        return builder.clone()
                .defaultSystem("""
                        You review incident reports. Approve only if:
                        1. the root cause is supported by at least two findings,
                        2. there is an immediate fix,
                        3. nothing is blamed without evidence in the findings.
                        Otherwise give short, precise feedback.""")
                .defaultAdvisors(new BudgetAdvisor("reviewer", budget, meters))
                .build();
    }
}
