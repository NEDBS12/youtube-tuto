package dev.course.incident;

import java.util.List;
import java.util.Map;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import dev.course.incident.Records.Finding;
import dev.course.incident.Records.IncidentReport;
import dev.course.incident.Records.Plan;
import dev.course.incident.Records.Review;
import dev.course.incident.Records.Step;
import dev.course.incident.Records.Workers;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

/** Orchestrator-workers: the planner decides WHO works on WHAT; Java runs the plan, in parallel, with limits. */
@Service
public class Orchestrator {

    private static final Logger log = LoggerFactory.getLogger(Orchestrator.class);

    private final ChatClient planner, writer, reviewer;
    private final Map<String, ChatClient> workers;
    private final TokenBudget budget;
    private final int timeoutSeconds, maxDrafts;

    public Orchestrator(@Qualifier("planner") ChatClient planner, @Qualifier("writer") ChatClient writer,
            @Qualifier("reviewer") ChatClient reviewer, Workers workers, TokenBudget budget,
            @Value("${incident.worker-timeout-seconds}") int timeoutSeconds, @Value("${incident.max-drafts}") int maxDrafts) {
        this.planner = planner;
        this.writer = writer;
        this.reviewer = reviewer;
        this.workers = workers.byName();
        this.budget = budget;
        this.timeoutSeconds = timeoutSeconds;
        this.maxDrafts = maxDrafts;
    }

    public IncidentReport handle(String incident) {
        long start = System.currentTimeMillis();
        budget.reset();
        List<Step> plan = List.of();
        List<Finding> findings = List.of();
        String report = "";
        int drafts = 0;
        try {
            // 1. Plan: the model decides which workers to ask. Java checks the plan.
            plan = planner.prompt().user(incident).call().entity(Plan.class).steps().stream()
                    .filter(s -> workers.containsKey(s.worker()))
                    .limit(3)
                    .toList();
            // A rule from the runbook, enforced in code: always check what changed.
            if (plan.stream().noneMatch(s -> s.worker().equals("deploys"))) {
                plan = Stream.concat(plan.stream(),
                        Stream.of(new Step("deploys", "Which deployments happened today, and what did they change?"))).toList();
            }
            log.info("PLAN {}", plan.stream().map(Step::worker).toList());

            // 2. Workers: in parallel, each with a timeout. A failure becomes a finding, not a crash.
            findings = runInParallel(plan, incident);

            // 3. Write and review: evaluator-optimizer, with a maximum number of drafts.
            String feedback = "";
            while (drafts < maxDrafts) {
                drafts++;
                report = write(incident, findings, report, feedback);
                Review review = review(findings, report);
                log.info("DRAFT {} approved: {} - {}", drafts, review.approved(), review.feedback());
                if (review.approved()) {
                    return new IncidentReport("APPROVED", plan, findings, report, drafts, budget.used(), seconds(start));
                }
                feedback = review.feedback();
            }
            return new IncidentReport("NOT APPROVED after " + drafts + " drafts: needs a human", plan, findings, report,
                    drafts, budget.used(), seconds(start));
        }
        catch (TokenBudget.ExceededException ex) {
            log.warn("STOP {}", ex.getMessage());
            return new IncidentReport("STOPPED: " + ex.getMessage(), plan, findings, report, drafts, budget.used(),
                    seconds(start));
        }
    }

    private List<Finding> runInParallel(List<Step> plan, String incident) {
        try (ExecutorService pool = Executors.newVirtualThreadPerTaskExecutor()) {
            List<CompletableFuture<Finding>> futures = plan.stream()
                    .map(step -> CompletableFuture
                            .supplyAsync(() -> ask(step, incident), pool)
                            .orTimeout(timeoutSeconds, TimeUnit.SECONDS)
                            .exceptionally(ex -> new Finding(step.worker(), "FAILED: " + ex.getMessage(), false)))
                    .toList();
            return futures.stream().map(CompletableFuture::join).toList();
        }
    }

    private Finding ask(Step step, String incident) {
        log.info("WORKER {} <- {}", step.worker(), step.question());
        String answer = workers.get(step.worker()).prompt()
                .user("Incident: " + incident + "\nYour question: " + step.question())
                .call().content();
        return new Finding(step.worker(), answer, true);
    }

    private String write(String incident, List<Finding> findings, String previous, String feedback) {
        String prompt = "Incident: " + incident + "\n\nFindings:\n" + format(findings)
                + (feedback.isBlank() ? "" : "\n\nPrevious draft:\n" + previous + "\n\nReviewer feedback: " + feedback);
        return writer.prompt().user(prompt).call().content();
    }

    private Review review(List<Finding> findings, String report) {
        // Code checks what code can check: a report that names no version can't point to the deploy.
        if (findings.stream().anyMatch(f -> f.answer().contains("v2.8.0")) && !report.contains("v2.8.0")) {
            return new Review(false, "The findings point to deploy v2.8.0, but the report does not mention it.");
        }
        return reviewer.prompt()
                .user("Findings:\n" + format(findings) + "\n\nReport:\n" + report)
                .call().entity(Review.class);
    }

    private static String format(List<Finding> findings) {
        return findings.stream().map(f -> "- [" + f.worker() + "] " + f.answer()).collect(Collectors.joining("\n"));
    }

    private static long seconds(long start) {
        return (System.currentTimeMillis() - start) / 1000;
    }
}
