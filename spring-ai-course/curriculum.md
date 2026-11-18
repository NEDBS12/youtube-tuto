# Spring AI: From Novice to Expert (YouTube playlist)

**Audience:** Java developers who already know Spring Boot.
**Stack:** Spring AI 2.0.x · Spring Boot 4.1 · Java 21 · Ollama (free, local), so every lab costs nothing to run.
Each lab notes where to swap in OpenAI or Anthropic with a one-line dependency and property change.

**Format for each concept (Udemy style):**
- 🎬 **Concept video** (5-7 min): why it exists, how it works, when to use it, with slides and diagrams
- 🧪 **Lab video** (6-9 min): build it step by step in a real project, then run it
- ❓ **Quiz** (5 questions) at the end of each concept
- 🏁 **Section eval** (10-12 questions plus a coding challenge) at the end of each section, scored with a level

| # | Section | Concept | Lab (what students build) |
|---|---|---|---|
| 0.0 | Welcome | Course tour, setup, how to use the quizzes | Install Java 21, Ollama, pull `gemma3:4b` |
| **1** | **Foundations** | | |
| 1.1 | | What is Spring AI? LLMs, tokens, the provider abstraction | First Spring AI app: `/chat` endpoint with Ollama |
| 1.2 | | The ChatClient API (call, content, chatResponse, metadata) | Inspect token usage and model metadata |
| 1.3 | | Prompts: system/user messages, PromptTemplate | Prompt-templated "Code explainer" API |
| 1.4 | | Model options: temperature, max tokens, switching providers | Same app on Ollama and OpenAI via profiles |
| 🏁 | **Eval 1** | Foundations | Challenge: a "commit message writer" endpoint |
| **2** | **Building chat applications** | | |
| 2.1 | | Streaming responses (Flux, SSE) | Streaming chat endpoint and a minimal web page |
| 2.2 | | Structured output (`entity()`, records, lists) | CV parser that returns a Java record |
| 2.3 | | Advisors: the interceptor chain | Logger advisor plus a custom "safe-words" advisor |
| 2.4 | | Chat memory (`ChatMemory`, conversation id, repositories) | Multi-user support bot that remembers |
| 🏁 | **Eval 2** | Chat applications | Challenge: a streaming, memory-aware tutor bot |
| **3** | **Tools and agents** | | |
| 3.1 | | Tool calling (`@Tool`, `@ToolParam`) | Assistant that reads the clock and an order DB |
| 3.2 | | The tool loop as an advisor (`ToolCallingAdvisor`), tool search | Many tools with progressive disclosure |
| 3.3 | | Agentic patterns: chain, routing, parallel, evaluator-optimizer | Ticket-triage agent with routing |
| 🏁 | **Eval 3** | Tools and agents | Challenge: a travel-planner agent with 3 tools |
| **4** | **RAG (Retrieval Augmented Generation)** | | |
| 4.1 | | Embeddings and similarity | Semantic search over FAQs with an `EmbeddingModel` |
| 4.2 | | Vector stores (Simple, PGVector), metadata filters | PGVector with Docker Compose |
| 4.3 | | ETL pipeline: readers, splitters, enrichers | Ingest PDFs and Markdown into the store |
| 4.4 | | RAG advisors (`QuestionAnswerAdvisor`, `RetrievalAugmentationAdvisor`) | "Chat with your docs" app |
| 🏁 | **Eval 4** | RAG | Challenge: an HR-policy assistant that cites its sources |
| **5** | **Model Context Protocol (MCP)** | | |
| 5.1 | | MCP: hosts, clients, servers, transports | Connect an existing MCP server to a Spring AI app |
| 5.2 | | Build an MCP server (`@McpTool`, `@McpResource`, `@McpPrompt`) | Expose the order DB as an MCP server (Streamable HTTP) |
| 5.3 | | MCP clients and security (OAuth 2.0) | Secure client/server pair |
| 🏁 | **Eval 5** | MCP | Challenge: an MCP server for a library catalogue |
| **6** | **Multimodality** | | |
| 6.1 | | Vision: images as input (`Media`) | Receipt reader: image to record |
| 6.2 | | Image generation, speech to text, text to speech | Voice note to summary pipeline |
| 🏁 | **Eval 6** | Multimodality | Challenge: a product-photo cataloguer |
| **7** | **Production-ready AI** | | |
| 7.1 | | Evaluating AI (`RelevancyEvaluator`, `FactCheckingEvaluator`, LLM as judge) | JUnit tests that grade the RAG app |
| 7.2 | | Observability: metrics, tracing, token cost | Token metrics and a cost report (Actuator, Prometheus) |
| 7.3 | | Guardrails, security, prompt injection, cost control | Harden the "chat with your docs" app |
| 🏁 | **Eval 7** | Production | Challenge: add evals and metrics to your own app |
| 🎓 | **Final exam and capstone** | Expert level | Capstone: support agent = RAG + tools + memory + MCP + evals |

**Levels (shown after every eval):** 0-49% Novice · 50-69% Apprentice · 70-84% Practitioner · 85-100% Expert-ready.

**Totals:** 1 welcome video + 24 concepts × 2 videos = 49 videos, 24 quizzes, 7 section evals, 1 final exam.

Folder layout:
```
course/curriculum.md          this plan
course/quizzes/               quiz + eval question banks (JSON)
labs/<lab>/                   tested lab projects (the code shown in the lab videos)
videos/<id>/script.json       video scripts → build/ → <id>.mp4
```
