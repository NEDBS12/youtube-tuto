package agent;

import agent.Route.Specialist;
import java.util.List;

// Routing: a small, fast model picks the right specialist
public class ReviewRouter {

    // The router: Haiku 5.5, no tools, one job: classify the file
    static final Agent ROUTER = new Agent("Router",
            "claude-haiku-5-5",
            "Pick the best reviewer for a Java file. "
            + "SECURITY: SQL, user input, passwords. "
            + "CONCURRENCY: threads, shared state. "
            + "TESTS: test classes. GENERAL: anything else.",
            List.of(), call -> "Error: no tools");

    // The switch must cover every specialist: the compiler checks it
    static String focusFor(Specialist specialist) {
        return switch (specialist) {
            case SECURITY -> "security";
            case CONCURRENCY -> "concurrency";
            case TESTS -> "testing";
            case GENERAL -> "code quality";
        };
    }

    // A specialist = the same Agent class with a focused prompt
    static Agent specialist(String focus) {
        return new Agent(focus + " reviewer",
                "You are a Java " + focus + " expert. Read the "
                + "file with your tool. Report real " + focus
                + " bugs only.",
                List.of(FileTools.READ_FILE), FileTools::run);
    }

    public static void main(String[] args) {
        String file = args.length > 0 ? args[0] : "UserService.java";

        // Step 1: route. One cheap call, the code is in the task.
        Route route = ROUTER.run("File " + file + ":\n"
                + FileTools.readFile(file), Route.class);
        System.out.println("Route: " + route.specialist()
                + " (" + route.reason() + ")");

        // Step 2: the chosen specialist does the real review
        Agent reviewer = specialist(focusFor(route.specialist()));
        Review review = reviewer.run("Review " + file, Review.class);

        review.bugs().forEach(bug -> System.out.println("  line "
                + bug.line() + " [" + bug.severity() + "] "
                + bug.problem()));
    }
}
