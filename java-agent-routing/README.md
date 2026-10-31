# Agent Routing in Java: send each job to the right specialist

Files from the Zero Cost AI video **"Agent Routing in Java: A Small Model Picks the Right Expert (Ep. 3)"**.

Episode 3 of the *Multi-agent systems in Java* series ([episode 1](../java-multi-agent-intro), [episode 2](../java-agent-pipeline)).
A **router** agent running on Claude Haiku 5.5 (small, fast, cheap) reads a Java file and returns a typed `Route`. The file then goes to one of four
**specialist** reviewers: security, concurrency, testing or code quality. The specialists run on Opus 5.5.
An exhaustive `switch` over the `Specialist` enum means the compiler checks every route.
Plain Java and the official Anthropic Java SDK (3.3.0). No framework.

## Use it in your project

| File | What it does |
|---|---|
| [`Agent.java`](example-files/java-agent-routing/src/main/java/agent/Agent.java) | The agent from episode 2, plus a per-agent `model` (the old constructor still defaults to Opus 5.5) |
| [`Route.java`](example-files/java-agent-routing/src/main/java/agent/Route.java) | The router's typed answer: a `Specialist` enum and a reason |
| [`ReviewRouter.java`](example-files/java-agent-routing/src/main/java/agent/ReviewRouter.java) | The Haiku router, the `focusFor` switch, the specialists and `main` |
| [`Review.java`](example-files/java-agent-routing/src/main/java/agent/Review.java), [`FileTools.java`](example-files/java-agent-routing/src/main/java/agent/FileTools.java) | The specialists' typed answer and their `read_file` tool, from episode 2 |
| [`RoutingCheck.java`](example-files/java-agent-routing/src/main/java/agent/RoutingCheck.java) | Offline check, no API key needed: samples, the `Route` schema and every route |
| [`sample/`](example-files/java-agent-routing/sample) | One file per specialist: `UserService.java` (SQL), `VisitCounter.java` (threads), `PriceCalculatorTest.java` (tests) |
| [`episode-2/ReviewPipeline.java`](example-files/java-agent-routing/episode-2/ReviewPipeline.java) | The pipeline from episode 2, for comparison (not compiled) |

Requirements: Java 17+ and Maven. Run these commands from `example-files/java-agent-routing`.

1. Check everything offline (no API key needed):
   ```
   mvn -q compile exec:java -Dexec.mainClass=agent.RoutingCheck
   ```
2. Set your API key (never put it in the code):
   ```
   $env:ANTHROPIC_API_KEY="sk-ant-..."      # Windows PowerShell
   export ANTHROPIC_API_KEY="sk-ant-..."    # macOS / Linux
   ```
3. Route the three sample files:
   ```
   mvn -q compile exec:java
   mvn -q compile exec:java -Dexec.args=VisitCounter.java
   mvn -q compile exec:java -Dexec.args=PriceCalculatorTest.java
   ```

- The output in the video is an example: the router's reasons and the bugs found will vary between runs.
- You may see three `SLF4J(W): No SLF4J providers were found` lines. They're harmless.
- Add a specialist: add a value to `Specialist` in `Route.java`, describe it in the router's prompt, and add its case in `focusFor`. Until you add the case, the code won't compile.
- The sample files are only read, never compiled (they live outside `src/`).

## Files in this folder

- `java-agent-routing.mp4`: the video
- `java-agent-routing.srt`: subtitles
- `script.json`: the video script (made with the claude-expert-video skill)
- `example-files/java-agent-routing/`: the Maven project (no secrets)

## Learn more

- [Building effective agents (Anthropic)](https://www.anthropic.com/engineering/building-effective-agents): the routing workflow
- [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview): Haiku 5.5 and the model IDs and prices
- [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
- [Anthropic Java SDK](https://github.com/anthropics/anthropic-sdk-java)
