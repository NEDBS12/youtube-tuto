# Multi-Agent Systems in Java: your first two-agent team

Files from the Zero Cost AI video **"Multi-Agent Systems in Java: What, Why and When NOT To (Ep. 1)"**.

Episode 1 of the *Multi-agent systems in Java* series. It turns the agent loop from
[Build Your First AI Agent in Java](../java-first-agent) into a reusable `Agent` class. Then it uses that class to build a
small code-review team: a **Reviewer** that reads a Java file with a tool and lists the bugs, and a
**Writer** that has no tools, never sees the code, and turns the notes into a friendly report.
Plain Java and the official Anthropic Java SDK (3.3.0). No framework.

## Use it in your project

| File | What it does |
|---|---|
| [`Agent.java`](example-files/java-multi-agent-intro/src/main/java/agent/Agent.java) | One agent: its own system prompt, tools and context, and the agent loop in `run(task)` (max 10 turns) |
| [`FileTools.java`](example-files/java-multi-agent-intro/src/main/java/agent/FileTools.java) | The Reviewer's `read_file` tool (only reads files inside `sample/`) |
| [`ReviewTeam.java`](example-files/java-multi-agent-intro/src/main/java/agent/ReviewTeam.java) | Creates the two agents and passes the Reviewer's notes to the Writer |
| [`ToolsCheck.java`](example-files/java-multi-agent-intro/src/main/java/agent/ToolsCheck.java) | Tests the tool offline, no API key needed |
| [`sample/UserService.java`](example-files/java-multi-agent-intro/sample/UserService.java) | The code to review (it has bugs on purpose) |
| [`episode-1/MyFirstAgent.java`](example-files/java-multi-agent-intro/episode-1/MyFirstAgent.java) | The agent from episode 1, for comparison (not compiled) |

Requirements: Java 17+ and Maven. Run these commands from `example-files/java-multi-agent-intro`.

1. Test the tool offline (no API key needed):
   ```
   mvn -q compile exec:java -Dexec.mainClass=agent.ToolsCheck
   ```
2. Set your API key (never put it in the code):
   ```
   $env:ANTHROPIC_API_KEY="sk-ant-..."      # Windows PowerShell
   export ANTHROPIC_API_KEY="sk-ant-..."    # macOS / Linux
   ```
3. Run the team:
   ```
   mvn -q compile exec:java
   ```

- The report in the video is an example: Claude's wording will differ on each run.
- Review your own code: put a `.java` file in `sample/` and change `"Review UserService.java"` in `ReviewTeam.java`.
- Add an agent: create another `new Agent(...)` with its own role and tools, and pass it the previous agent's output.

## Files in this folder

- `java-multi-agent-intro.mp4`: the video
- `java-multi-agent-intro.srt`: subtitles
- `script.json`: the video script (made with the claude-expert-video skill)
- `example-files/java-multi-agent-intro/`: the Maven project (no secrets)

## Learn more

- [How Anthropic built its multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) (where the "about 15× more tokens" figure comes from)
- [Tool use with Claude (official docs)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
- [Anthropic Java SDK](https://github.com/anthropics/anthropic-sdk-java)
