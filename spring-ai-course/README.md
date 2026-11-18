# Spring AI: Novice to Expert (free course)

Code labs and resources for the free **Spring AI** course on the [Zero Cost AI](https://www.youtube.com/@zerocostai-f1h) YouTube channel.
Every lab runs on a free local model with Ollama, so the whole course costs nothing.

**Stack:** Spring AI 2.0.1 · Spring Boot 4.1.2 · Java 21 · Ollama `gemma3:4b`

## What's here

| Folder | Contents |
|---|---|
| [`labs/`](labs) | One ready-to-run Spring Boot project per lesson |
| [`quiz/`](quiz) | The interactive quiz page (open it at https://nedbs12.github.io/youtube-tuto/spring-ai-course/quiz/) |
| [`quizzes/`](quizzes) | The quiz and section eval questions for each section (JSON) |
| [`curriculum.md`](curriculum.md) | The full course plan: all sections, lessons and labs |

Take the quizzes and section evals online, free, no account needed: [Spring AI course quizzes](https://nedbs12.github.io/youtube-tuto/spring-ai-course/quiz/)

## Lessons

| # | Concept video | Lab video | Lab code |
|---|---|---|---|
| **1** | **Foundations** | | |
| 1.1 | What is Spring AI? | Your first AI app with Ollama | [`labs/hello-spring-ai`](labs/hello-spring-ai) |
| 1.2 | The ChatClient API | ChatClient defaults, token usage and overrides | [`labs/chatclient-explorer`](labs/chatclient-explorer) |
| 1.3 | Prompts, roles and templates | A code explainer API with prompt templates | [`labs/code-explainer`](labs/code-explainer) |
| 1.4 | Model options and switching providers | Temperature live, switch models with profiles | [`labs/model-options`](labs/model-options) |
| **2** | **Building chat applications** | | |
| 2.1 | Streaming with Flux and Server-Sent Events | Streaming chat with SSE | [`labs/streaming-chat`](labs/streaming-chat) |
| 2.2 | Structured output as Java records | CV parser with Java records | [`labs/cv-parser`](labs/cv-parser) |
| 2.3 | Advisors: the interceptor chain | Logger, SafeGuard and a custom advisor | [`labs/advisors-demo`](labs/advisors-demo) |
| 2.4 | Chat memory | Support bot with memory that survives restarts | [`labs/support-bot`](labs/support-bot) |
| **3** | **Tools and agents** | | |
| 3.1 | Tool calling with @Tool and @ToolParam | Order assistant with tool calling | [`labs/order-assistant`](labs/order-assistant) |
| 3.2 | The tool loop: ToolCallingAdvisor and tool search | Watch the tool loop, measure tokens, try tool search | [`labs/tool-loop`](labs/tool-loop) |
| 3.3 | Agents vs workflows: 5 agentic patterns | Ticket-triage agent with routing and a review loop | [`labs/ticket-triage`](labs/ticket-triage) |
| **4** | **RAG: chat with your data** | | |
| 4.1 | Embeddings and cosine similarity | Semantic FAQ search with embeddings | [`labs/faq-search`](labs/faq-search) |
| 4.2 | Vector stores: PGVector, filters, topK | Product search on PGVector with Docker Compose | [`labs/product-store`](labs/product-store) |
| 4.3 | The ETL pipeline: readers, splitters, enrichers | Ingest PDF and Markdown into PGVector | [`labs/doc-ingest`](labs/doc-ingest) |
| 4.4 | RAG advisors compared | Chat with your docs, and debug a wrong answer | [`labs/docs-chat`](labs/docs-chat) |

Watch the videos in order in the **Spring AI** playlist on the [channel](https://www.youtube.com/@zerocostai-f1h).

## Run a lab

You need **Java 21** and **[Ollama](https://ollama.com)**.

```bash
# 1. get the free local model (once)
ollama pull gemma3:4b

# 2. run the lab
cd labs/hello-spring-ai
./mvnw spring-boot:run        # Windows: mvnw.cmd spring-boot:run
```

Each project already includes the Maven wrapper, so you don't need to install Maven.
Endpoints and requests for each lab are shown step by step in its lab video.

Notes:
- `labs/order-assistant` uses `qwen2.5:3b` and `labs/tool-loop` uses `qwen2.5:7b` (models that handle tool calls well):
  `ollama pull qwen2.5:3b` / `ollama pull qwen2.5:7b`.
- `labs/model-options` also uses `llama3.2:1b` (`ollama pull llama3.2:1b`). Its `openai` profile needs an
  `OPENAI_API_KEY` environment variable. Never put a key in a properties file.
- `labs/support-bot` stores conversations in a local H2 database under `data/`, created on first run.
- Section 4 labs use the embedding model `mxbai-embed-large` (`ollama pull mxbai-embed-large`).
  `labs/product-store`, `labs/doc-ingest` and `labs/docs-chat` start PGVector automatically with Docker Compose,
  so you need **Docker** running.

---

Free AI apps and tutorials: subscribe to [Zero Cost AI](https://www.youtube.com/@zerocostai-f1h?sub_confirmation=1).
