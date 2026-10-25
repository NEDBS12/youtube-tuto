# Your First AI Agent in Java: LLM + tools + a loop

Files from the Zero Cost AI video **"Build Your First AI Agent in Java with Claude (Step by Step)"**.

A beginner-friendly agent built with the official Anthropic Java SDK, no framework. Claude gets two tools,
`get_current_time` and `calculate`, and a small loop runs them whenever Claude asks, until it has the answer.

## Use it in your project

| File | What it does |
|---|---|
| [`pom.xml`](example-files/java-first-agent/pom.xml) | Maven project with the `anthropic-java` SDK and the exec plugin |
| [`Tools.java`](example-files/java-first-agent/src/main/java/agent/Tools.java) | The tools: Java methods, their descriptions for Claude, and `run()` which routes a tool call to the right method |
| [`MyFirstAgent.java`](example-files/java-first-agent/src/main/java/agent/MyFirstAgent.java) | The agent loop: call Claude, run the tools it asks for, send the results back, repeat |
| [`NoTools.java`](example-files/java-first-agent/src/main/java/agent/NoTools.java) | A plain chatbot with no tools, for comparison |
| [`ToolsCheck.java`](example-files/java-first-agent/src/main/java/agent/ToolsCheck.java) | Tests the tools offline, no API key needed |

1. Install Java 17+ and Maven, then open `example-files/java-first-agent`.
2. Test the tools offline: `mvn -q compile exec:java -Dexec.mainClass=agent.ToolsCheck`
3. Set your API key (from https://platform.claude.com):
   - Windows PowerShell: `$env:ANTHROPIC_API_KEY="sk-ant-..."`
   - macOS / Linux: `export ANTHROPIC_API_KEY="sk-ant-..."`
4. Run the agent: `mvn -q compile exec:java`, then ask *"What time is it, and what is 1234 times 5678?"*

- Each run calls the Claude API, which needs credits on your Anthropic account.
- To add your own tool: write the method and a `Tool` description in `Tools.java`, add a `case` in `run()`,
  then `.addTool(...)` it in `MyFirstAgent.java`.
- In a real app, also cap the number of loop turns so the agent can never run forever.

## Files in this folder

- `java-first-agent.mp4`: the video
- `java-first-agent.srt`: subtitles
- `script.json`: the video script (made with the claude-expert-video skill)
- `example-files/java-first-agent/`: the demo project (no secrets; it reads your key from the environment)

## Learn more

- [Tool use with Claude](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
- [Anthropic Java SDK](https://github.com/anthropics/anthropic-sdk-java)
