# Agent Pipelines in Java: typed outputs and gates

Files from the Zero Cost AI video **"Agent Pipelines in Java: Chain AI Agents with Typed Outputs (Ep. 2)"**.

Episode 2 of the *Multi-agent systems in Java* series ([episode 1](../java-multi-agent-intro)). It turns
the two-agent code-review team into a real pipeline: **Reviewer → gate → Writer**.
- The Reviewer returns a typed `Review` record, using structured outputs.
- A gate in plain Java drops the low-severity bugs and stops the pipeline if nothing serious is left.
- The Writer runs only when it's needed, and gets only the serious bugs.

Plain Java and the official Anthropic Java SDK (3.3.0). No framework.

## Use it in your project

| File | What it does |
|---|---|
| [`Agent.java`](example-files/java-agent-pipeline/src/main/java/agent/Agent.java) | The agent from episode 1, upgraded: `run(task, Type.class)` returns a typed record (`outputConfig(type)`); `run(task)` still returns text |
| [`Review.java`](example-files/java-agent-pipeline/src/main/java/agent/Review.java) | The typed handoff: a summary and a list of bugs (line, severity, problem, fix) |
| [`ReviewPipeline.java`](example-files/java-agent-pipeline/src/main/java/agent/ReviewPipeline.java) | The pipeline, with the `seriousBugs` gate in plain Java |
| [`FileTools.java`](example-files/java-agent-pipeline/src/main/java/agent/FileTools.java) | The Reviewer's `read_file` tool (only reads files inside `sample/`) |
| [`PipelineCheck.java`](example-files/java-agent-pipeline/src/main/java/agent/PipelineCheck.java) | Offline check, no API key needed: the tool, the record schemas and the gate |
| [`sample/`](example-files/java-agent-pipeline/sample) | `UserService.java` (buggy on purpose) and `PriceCalculator.java` (clean) |
| [`episode-1/ReviewTeam.java`](example-files/java-agent-pipeline/episode-1/ReviewTeam.java) | The team from episode 1, for comparison (not compiled) |

Requirements: Java 17+ and Maven. Run these commands from `example-files/java-agent-pipeline`.

1. Check everything offline (no API key needed):
   ```
   mvn -q compile exec:java -Dexec.mainClass=agent.PipelineCheck
   ```
2. Set your API key (never put it in the code):
   ```
   $env:ANTHROPIC_API_KEY="sk-ant-..."      # Windows PowerShell
   export ANTHROPIC_API_KEY="sk-ant-..."    # macOS / Linux
   ```
3. Run the pipeline on the buggy file, then on the clean one (the gate stops it before the Writer):
   ```
   mvn -q compile exec:java
   mvn -q compile exec:java -Dexec.args=PriceCalculator.java
   ```

- The output in the video is an example: Claude's wording, and the bugs it rates LOW, will vary between runs.
- You may see three `SLF4J(W): No SLF4J providers were found` lines. They're harmless: add an SLF4J logger (for example `slf4j-simple`) to the pom if you want logs.
- Change the gate: edit `seriousBugs` in `ReviewPipeline.java` (for example, keep only `HIGH`).
- Add a field to the handoff: add it to the `Bug` record. The SDK updates the schema for you.

## Files in this folder

- `java-agent-pipeline.mp4`: the video
- `java-agent-pipeline.srt`: subtitles
- `script.json`: the video script (made with the claude-expert-video skill)
- `example-files/java-agent-pipeline/`: the Maven project (no secrets)

## Learn more

- [Structured outputs (official docs)](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
- [Anthropic Java SDK](https://github.com/anthropics/anthropic-sdk-java)
- [Building effective agents (Anthropic)](https://www.anthropic.com/engineering/building-effective-agents): prompt chaining and gates
