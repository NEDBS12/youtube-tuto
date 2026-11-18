package dev.course.files;

import java.util.Arrays;
import java.util.List;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class NotesController {

    private final ChatClient chatClient;
    private final ToolCallbackProvider mcpTools;

    public NotesController(ChatClient.Builder builder, ToolCallbackProvider mcpTools) {
        this.mcpTools = mcpTools;
        this.chatClient = builder
                .defaultSystem("""
                        You help the user with their notes. The notes are in the allowed directory:
                        call list_allowed_directories first, and always use full paths.
                        Never guess a file name: call list_directory to find it, then read it.""")
                .defaultToolCallbacks(mcpTools)
                .build();
    }

    @GetMapping("/tools")
    public List<String> tools() {
        return Arrays.stream(mcpTools.getToolCallbacks())
                .map(tool -> tool.getToolDefinition().name())
                .toList();
    }

    @GetMapping("/ask")
    public String ask(@RequestParam String q) {
        return chatClient.prompt().user(q).call().content();
    }
}
