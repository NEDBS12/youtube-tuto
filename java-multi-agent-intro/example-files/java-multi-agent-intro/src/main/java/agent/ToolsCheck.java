package agent;

// Tests the tool offline (no API key needed): mvn compile exec:java -Dexec.mainClass=agent.ToolsCheck
public class ToolsCheck {

    public static void main(String[] args) {
        String code = FileTools.readFile("UserService.java");
        System.out.println("read:    " + code.lines().count() + " lines");
        System.out.println("missing: " + FileTools.readFile("Nope.java"));
        System.out.println("escape:  " + FileTools.readFile("../pom.xml"));
        System.out.println("name:    " + FileTools.READ_FILE.name());
    }
}
