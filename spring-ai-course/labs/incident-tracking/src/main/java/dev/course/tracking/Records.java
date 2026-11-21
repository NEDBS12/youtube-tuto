package dev.course.tracking;

import java.util.List;
import java.util.Map;

import org.springframework.ai.chat.client.ChatClient;

/** The typed messages between the agents of the team. */
public final class Records {

    private Records() {
    }

    /** The worker agents, by name (a record, so Spring doesn't inject every ChatClient bean as a Map). */
    public record Workers(Map<String, ChatClient> byName) {
    }

    /** One job for one worker agent. */
    public record Step(String worker, String question) {
    }

    /** The planner's output: which workers to ask, and what. */
    public record Plan(List<Step> steps) {
    }

    /** A worker's answer, or why it failed. */
    public record Finding(String worker, String answer, boolean ok) {
    }

    /** The reviewer's verdict. */
    public record Review(boolean approved, String feedback) {
    }

    public record IncidentReport(String status, List<Step> plan, List<Finding> findings, String report,
            int drafts, int tokensUsed, long seconds) {
    }
}
