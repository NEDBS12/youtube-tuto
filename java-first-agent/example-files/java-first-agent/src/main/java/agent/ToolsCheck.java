package agent;

// Tests the tools offline (no API key needed): mvn compile exec:java -Dexec.mainClass=agent.ToolsCheck
public class ToolsCheck {

    public static void main(String[] args) {
        System.out.println("time:     " + Tools.getCurrentTime());
        System.out.println("multiply: " + Tools.calculate("multiply", 1234, 5678));
        System.out.println("divide:   " + Tools.calculate("divide", 10, 0));
        System.out.println("tools:    " + Tools.TIME.name() + ", " + Tools.CALCULATOR.name());
    }
}
