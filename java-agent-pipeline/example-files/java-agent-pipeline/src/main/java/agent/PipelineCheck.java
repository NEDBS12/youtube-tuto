package agent;

import agent.Review.Bug;
import agent.Review.Severity;
import com.anthropic.models.messages.MessageCreateParams;
import java.util.List;

// Tests the pipeline offline (no API key needed): mvn compile exec:java -Dexec.mainClass=agent.PipelineCheck
public class PipelineCheck {

    public static void main(String[] args) {
        // 1. The tool reads the samples
        System.out.println("read:   UserService "
                + FileTools.readFile("UserService.java").lines().count() + " lines, PriceCalculator "
                + FileTools.readFile("PriceCalculator.java").lines().count() + " lines");

        // 2. The SDK turns the Review record into a JSON schema (checked locally)
        MessageCreateParams.builder()
                .model("claude-opus-5-5").maxTokens(1000L)
                .addUserMessage("test").outputConfig(Review.class).build();
        MessageCreateParams.builder()
                .model("claude-opus-5-5").maxTokens(1000L)
                .addUserMessage("test").outputConfig(Agent.Answer.class).build();
        System.out.println("schema: Review and Answer records OK");

        // 3. The gate, with fake reviews
        Review buggy = new Review("Checks if a user is an admin.", List.of(
                new Bug(18, Severity.HIGH, "SQL injection", "Use a PreparedStatement"),
                new Bug(6, Severity.LOW, "Comment style", "Optional")));
        Review clean = new Review("Computes a total price.", List.of(
                new Bug(3, Severity.LOW, "Could add Javadoc", "Optional")));
        System.out.println("gate:   buggy -> " + ReviewPipeline.seriousBugs(buggy).size()
                + " serious bug(s), clean -> " + ReviewPipeline.seriousBugs(clean).size());
    }
}
