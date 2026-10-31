// From episode 1 (Multi-Agent Systems in Java), kept here for comparison.
// It is not compiled: Maven only builds src/main/java.
package agent;

import java.util.List;

// Two agents, two jobs: one finds the bugs, one explains them
public class ReviewTeam {

    public static void main(String[] args) {
        // Agent 1: can read files. Its only job is to find real bugs.
        Agent reviewer = new Agent("Reviewer",
                "You are a senior Java reviewer. Read the file "
                + "with your tool. List real bugs only: "
                + "line, problem, fix.",
                List.of(FileTools.READ_FILE), FileTools::run);

        // Agent 2: no tools. It never sees the code, only the notes.
        Agent writer = new Agent("Writer",
                "You turn code review notes into a short, friendly "
                + "report for a junior developer. Max 8 lines.",
                List.of(), call -> "Error: no tools");

        String notes = reviewer.run("Review UserService.java");
        String report = writer.run("Write the report:\n" + notes);

        System.out.println("\n=== REPORT ===\n" + report);
    }
}
