package agent;

import com.anthropic.core.JsonValue;
import com.anthropic.models.messages.Tool;
import com.anthropic.models.messages.ToolUseBlock;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Map;

// The Reviewer's only tool: read a file from the sample folder
public class FileTools {

    static final Tool READ_FILE = Tool.builder()
            .name("read_file")
            .description("Reads a Java file from the sample folder. "
                    + "Use it to see the code before reviewing it.")
            .inputSchema(Tool.InputSchema.builder()
                .properties(Tool.InputSchema.Properties.builder()
                    .putAdditionalProperty("name", JsonValue.from(
                        Map.of("type", "string")))
                    .build())
                .required(List.of("name"))
                .build())
            .build();

    // Plain Java: the real work, safe to test without an API key
    static String readFile(String name) {
        try {
            Path file = Path.of("sample", name).normalize();
            if (!file.startsWith("sample")) {
                return "Error: only files in the sample folder";
            }
            return Files.readString(file);
        } catch (Exception e) {
            return "Error: cannot read " + name;
        }
    }

    // Run the tool call the agent asked for
    @SuppressWarnings("unchecked")
    static String run(ToolUseBlock call) {
        Map<String, Object> in = call._input().convert(Map.class);
        return readFile((String) in.get("name"));
    }
}
