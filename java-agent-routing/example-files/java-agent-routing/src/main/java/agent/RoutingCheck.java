package agent;

import agent.Route.Specialist;
import com.anthropic.models.messages.MessageCreateParams;

// Tests the router setup offline (no API key needed): mvn compile exec:java -Dexec.mainClass=agent.RoutingCheck
public class RoutingCheck {

    public static void main(String[] args) {
        // 1. The samples are readable by the tool
        for (String f : new String[] {"UserService.java", "VisitCounter.java", "PriceCalculatorTest.java"}) {
            System.out.println("read:   " + f + " " + FileTools.readFile(f).lines().count() + " lines");
        }

        // 2. The SDK turns the Route record into a JSON schema (checked locally)
        MessageCreateParams.builder().model("claude-haiku-5-5").maxTokens(1000L)
                .addUserMessage("test").outputConfig(Route.class).build();
        System.out.println("schema: Route record OK");

        // 3. Every specialist has a focus
        for (Specialist s : Specialist.values()) {
            System.out.println("route:  " + s + " -> " + ReviewRouter.focusFor(s));
        }
    }
}
