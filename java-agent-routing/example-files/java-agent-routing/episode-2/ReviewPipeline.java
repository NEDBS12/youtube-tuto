// From episode 2 (Agent Pipelines in Java), kept here for comparison.
// It is not compiled: Maven only builds src/main/java.
package agent;

import agent.Review.Bug;
import agent.Review.Severity;
import java.util.List;

// A pipeline: Reviewer -> gate (plain Java) -> Writer
public class ReviewPipeline {

    // The gate: plain Java, no LLM. Keep only the serious bugs.
    static List<Bug> seriousBugs(Review review) {
        return review.bugs().stream()
                .filter(bug -> bug.severity() != Severity.LOW)
                .toList();
    }

    public static void main(String[] args) {
        String file = args.length > 0 ? args[0] : "UserService.java";

        Agent reviewer = new Agent("Reviewer",
                "You are a senior Java reviewer. Read the file "
                + "with your tool. Report real bugs only.",
                List.of(FileTools.READ_FILE), FileTools::run);

        Agent writer = new Agent("Writer",
                "You turn bug lists into a short, friendly report "
                + "for a junior developer. Max 8 lines.",
                List.of(), call -> "Error: no tools");

        // Step 1: a typed review
        Review review = reviewer.run("Review " + file, Review.class);
        System.out.println("Summary: " + review.summary());

        // Step 2: the gate decides if the pipeline continues
        List<Bug> serious = seriousBugs(review);
        if (serious.isEmpty()) {
            System.out.println("No serious bugs: Writer skipped.");
            return;
        }

        // Step 3: the Writer gets only the serious bugs
        String report = writer.run("Write the report:\n" + serious);
        System.out.println("\n=== REPORT ===\n" + report);
    }
}
