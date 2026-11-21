# Spring AI senior interview question bank (Spring AI 2.0.x, Spring Boot 4, Java 21).
# Each question: options[0] is the correct answer (the app and the PDF shuffle them).

TOPICS = [
    ("arch", "Architecture & Abstractions"),
    ("client", "ChatClient API"),
    ("prompt", "Prompts & Templates"),
    ("options", "Model Options & Providers"),
    ("stream", "Streaming"),
    ("struct", "Structured Output"),
    ("advisor", "Advisors"),
    ("memory", "Chat Memory"),
    ("tools", "Tool Calling"),
    ("agents", "Agentic Patterns"),
    ("embed", "Embeddings"),
    ("vector", "Vector Stores"),
    ("etl", "ETL Pipeline"),
    ("rag", "RAG"),
    ("mcp", "Model Context Protocol (MCP)"),
    ("multi", "Multimodality"),
    ("eval", "Evaluation & Testing"),
    ("obs", "Observability"),
    ("security", "Security & Guardrails"),
    ("prod", "Production & Performance"),
]

# What to study when a topic comes out weak.
ADVICE = {
    "arch": "Review the ChatModel / StreamingChatModel / EmbeddingModel interfaces, how Boot auto-configuration picks a provider, and why the portable API matters.",
    "client": "Practise the fluent ChatClient chain: prompt() -> system/user -> call()/stream() -> content()/chatResponse()/entity(), plus builder defaults.",
    "prompt": "Study Message types, PromptTemplate, template renderers and custom delimiters, and loading templates from Resources.",
    "options": "Know portable ChatOptions vs provider options, default vs per-request options, spring.ai.model.* selection and running several providers side by side.",
    "stream": "Rebuild a Flux<String> SSE endpoint, learn how advisors behave in streaming and what you lose (structured output, simple usage) when streaming.",
    "struct": "Study BeanOutputConverter, entity(Class) and ParameterizedTypeReference, format instructions, native JSON schema mode and validation/retry.",
    "advisor": "Write a custom CallAdvisor/StreamAdvisor, learn ordering (getOrder), context sharing, and the built-in advisors.",
    "memory": "Know ChatMemory vs ChatMemoryRepository, MessageWindowChatMemory, conversation ids, the three memory advisors and JDBC persistence.",
    "tools": "Practise @Tool/@ToolParam, ToolContext, returnDirect, error handling, and user-controlled tool execution with ToolCallingManager.",
    "agents": "Re-read the agentic patterns (chain, routing, parallelization, orchestrator-workers, evaluator-optimizer) and when a workflow beats an autonomous agent.",
    "embed": "Review what embeddings are, dimensions, cosine similarity, batching, and why the same model must be used for indexing and querying.",
    "vector": "Study the VectorStore API, SearchRequest (topK, threshold, filter), metadata filter expressions, PGVector schema/index settings.",
    "etl": "Review DocumentReader -> DocumentTransformer -> DocumentWriter, chunking strategies, metadata enrichment and idempotent re-ingestion.",
    "rag": "Compare QuestionAnswerAdvisor and RetrievalAugmentationAdvisor, query transformers/expanders, empty-context handling and citing sources.",
    "mcp": "Learn MCP roles, primitives, transports (stdio, SSE, Streamable HTTP), Spring AI client/server starters and the @McpTool family.",
    "multi": "Practise sending Media with a user message, and the ImageModel, TranscriptionModel and TextToSpeechModel APIs.",
    "eval": "Learn Evaluator, EvaluationRequest, RelevancyEvaluator, FactCheckingEvaluator, LLM-as-judge pitfalls and how to test without flakiness.",
    "obs": "Study Micrometer observations in Spring AI, gen_ai.* metrics, tracing advisors/tools, and why prompt logging is off by default.",
    "security": "Review prompt injection (direct and indirect), SafeGuardAdvisor, least-privilege tools, OAuth for MCP, and data leakage controls.",
    "prod": "Study retries/timeouts, rate limits, cost control, caching, model selection, async/virtual threads and graceful degradation.",
}

Q = [
    # ---------------- Architecture & Abstractions ----------------
    {"t": "arch", "q": "What is the main architectural value of Spring AI's ChatModel abstraction?",
     "o": ["One portable API, so business code does not depend on a provider SDK",
           "It runs the model in-process, so no network calls are needed",
           "It normalises outputs, so every provider returns the same answer",
           "It caches completions, so repeated prompts never reach the provider again"],
     "e": "ChatModel (and StreamingChatModel) define call(Prompt) -> ChatResponse and stream(Prompt) -> Flux<ChatResponse>. "
          "Each provider module (OpenAI, Anthropic, Ollama, Bedrock...) implements them, so you can switch provider by changing a starter "
          "and properties. Models still behave differently: portability is about code, not output."},
    {"t": "arch", "q": "How does Spring AI choose which ChatModel bean to create when several provider starters are on the classpath?",
     "o": ["The spring.ai.model.chat property selects which provider is auto-configured",
           "The provider whose starter is declared first in the pom wins",
           "Startup fails unless every extra provider starter is excluded from the build",
           "All providers are wired and requests are load-balanced between them"],
     "e": "Since 1.0 the spring.ai.model.<type> properties (chat, embedding, image, audio.transcription...) select the active provider. "
          "To use several at once, enable them and inject each ChatModel by type or qualifier, then build one ChatClient per model "
          "(and set spring.ai.chat.client.enabled=false to skip the single auto-configured ChatClient.Builder)."},
    {"t": "arch", "q": "Which statement best describes the relationship between ChatClient and ChatModel?",
     "o": ["ChatClient is a fluent layer over ChatModel adding advisors, tools and defaults",
           "ChatModel is a fluent layer over ChatClient adding retries and metrics",
           "ChatClient is the streaming API, ChatModel the blocking one",
           "ChatClient is the HTTP transport that ChatModel uses to reach providers"],
     "e": "ChatModel is the low-level model port. ChatClient (like WebClient/RestClient) wraps it with a fluent API: prompt building, "
          "default system text, advisors (memory, RAG, logging), tool registration and entity() conversion. Use ChatModel directly only "
          "when you need full control over the raw Prompt and ChatResponse."},
    {"t": "arch", "q": "Which model types does Spring AI abstract besides chat?",
     "o": ["Embedding, image, transcription, text-to-speech and moderation models",
           "Embedding and image models only; audio needs the provider SDK",
           "Embedding models only; other modalities go through ChatModel",
           "Image and audio models only; embeddings are handled by each vector store module"],
     "e": "Spring AI has EmbeddingModel, ImageModel, TranscriptionModel, TextToSpeechModel and ModerationModel, all following the same "
          "request/response pattern (ModelRequest -> ModelResponse) with provider-specific options. Knowing this lets you design "
          "multimodal features without SDK lock-in."},

    # ---------------- ChatClient API ----------------
    {"t": "client", "q": "What does chatClient.prompt().user(q).call().chatResponse() give you that .content() does not?",
     "o": ["The full ChatResponse with generations, finish reason and token usage",
           "A Flux of partial responses that you must aggregate yourself",
           "The reply already parsed into the target record type",
           "The rendered prompt that was sent, for debugging purposes"],
     "e": ".content() returns only the text of the first generation. .chatResponse() returns the ChatResponse, whose getMetadata() "
          "exposes Usage (prompt, completion and total tokens), the model, rate-limit info and provider fields. Use it for cost tracking "
          "and debugging. .responseEntity() returns both the response and a converted entity."},
    {"t": "client", "q": "Where should a shared system prompt, default advisors and default tools be configured for a ChatClient used across a service?",
     "o": ["On the ChatClient.Builder with defaultSystem, defaultAdvisors and defaultTools",
           "On the ChatModel bean through its setDefaultPrompt method",
           "In a @ControllerAdvice that rewrites every outgoing prompt",
           "In application.properties under spring.ai.chat.client.defaults.system and .advisors"],
     "e": "The builder's default* methods set behaviour that applies to every request; per-request calls can still add or override "
          "(e.g. .system(...) or .advisors(...)). The auto-configured ChatClient.Builder is a prototype bean, so each injection point gets "
          "its own builder and you can build several differently configured clients."},
    {"t": "client", "q": "How do you pass a runtime parameter (e.g. a conversation id) to an advisor for a single request?",
     "o": ["advisors(a -> a.param(ChatMemory.CONVERSATION_ID, id)) on the request",
           "A ThreadLocal set by a servlet filter before the call is made",
           "A new advisor instance built with the id for every single request, then discarded",
           "A system message containing the id, which advisors parse back out"],
     "e": "The advisors(Consumer<AdvisorSpec>) overload lets you set parameters that are placed in the advisor context for that request. "
          "Advisors read them from the request context. This keeps advisors stateless and thread-safe, which matters in multi-user apps."},
    {"t": "client", "q": "You need the same ChatClient code to run against both a fast cheap model and a strong expensive model. What is the cleanest design?",
     "o": ["Two ChatClient beans, or a per-request model option, chosen by a router",
           "One ChatClient whose system prompt tells the provider which model to use",
           "A Spring profile per model, switched by restarting the application",
           "A @Primary ChatModel that the provider swaps automatically under load"],
     "e": "Either build separate ChatClients from different ChatModel beans, or keep one provider and set .options(ChatOptions.builder()"
          ".model(\"...\").build()) per request. A router (rule-based or a small classifier model) chooses the tier. This is a common cost "
          "optimisation pattern."},

    # ---------------- Prompts & Templates ----------------
    {"t": "prompt", "q": "What is the role of the SystemMessage compared to the UserMessage?",
     "o": ["It sets rules, role and format; the user message carries the request",
           "It is shown to the end user as the assistant's greeting",
           "It is sent only on the first call and dropped afterwards",
           "It holds the user input, so the model gives the user's words a higher priority"],
     "e": "Spring AI models conversation as Messages: SystemMessage, UserMessage, AssistantMessage and ToolResponseMessage. Providers "
          "give the system message higher priority, so put rules, persona and output format there. Never put untrusted user input in "
          "the system message: that is a prompt-injection risk."},
    {"t": "prompt", "q": "Your prompt template contains JSON examples with curly braces and the rendering fails. What is the right fix?",
     "o": ["Give StTemplateRenderer other delimiters, e.g. < and >, for that template",
           "Escape each brace with a backslash inside the Java text block",
           "Move the JSON examples into the user message, where braces are ignored",
           "Switch to String.format, which does not treat braces as variables"],
     "e": "PromptTemplate uses StringTemplate (ST) with {var} by default, so literal braces collide. You can set custom delimiters on "
          "StTemplateRenderer and pass it with .templateRenderer(...) on the PromptTemplate or ChatClient. Avoid string concatenation of "
          "user input: templates keep structure and inputs separate."},
    {"t": "prompt", "q": "What is a good practice for managing long prompts in a Spring AI codebase?",
     "o": ["Keep them as .st resources on the classpath and version them with the code",
           "Store them in the database so they can be edited live in production without a release",
           "Inline them as Java constants so the compiler checks them",
           "Generate them per request with the model, to keep them up to date"],
     "e": "PromptTemplate and the ChatClient .system(Resource)/.user(Resource) overloads accept Spring Resources. Keeping prompts in files "
          "makes them reviewable, diffable and testable, and lets you evaluate a prompt change with your evaluation suite before release."},
    {"t": "prompt", "q": "What is the difference between few-shot prompting and fine-tuning in practice?",
     "o": ["Few-shot adds examples to the prompt; fine-tuning changes the weights",
           "Few-shot changes the weights a little; fine-tuning only adds examples to the prompt",
           "Both change the weights, but few-shot uses fewer training examples",
           "Both are prompt techniques; fine-tuning just uses more examples"],
     "e": "Few-shot (in-context learning) is cheap and instant but costs tokens on every request. Fine-tuning needs data, time and "
          "provider support, but can reduce prompt size and improve consistency. For knowledge that changes, prefer RAG over both."},

    # ---------------- Model Options & Providers ----------------
    {"t": "options", "q": "What does a low temperature (e.g. 0.0-0.2) do?",
     "o": ["More deterministic, focused output, good for extraction and code",
           "Shorter responses, since fewer tokens are sampled per answer",
           "Lower latency, because sampling is skipped for most tokens",
           "Fully reproducible output, so exact-match tests become safe"],
     "e": "Temperature scales the probability distribution over next tokens. Low values favour the most likely tokens; high values add "
          "variety. Even at 0, many providers are not fully deterministic, so tests must not rely on exact text."},
    {"t": "options", "q": "How are default options and per-request options combined?",
     "o": ["Request options are merged over the defaults and win on conflicts",
           "Defaults from properties always win over request options",
           "Request options replace the defaults entirely; unset fields become null",
           "Options are fixed at startup and cannot change per request"],
     "e": "Spring AI merges runtime ChatOptions with the model's default options (from spring.ai.<provider>.chat.options.* or the "
          "builder). Fields set at runtime override; others keep the defaults. Provider-specific option classes (e.g. OpenAiChatOptions) "
          "expose features the portable ChatOptions do not."},
    {"t": "options", "q": "Why would you set maxTokens on a request?",
     "o": ["To cap output length, cost and latency; check for a 'length' finish",
           "To enlarge the context window so that longer prompts and documents are accepted",
           "To limit how much of the prompt the model is allowed to read",
           "To guarantee the answer is complete and never truncated"],
     "e": "maxTokens limits generated tokens, not the input. Always check the finish reason in ChatResponse metadata: a truncated answer "
          "can break JSON parsing in structured output. Context window size is a property of the model, not an option."},
    {"t": "options", "q": "Which Spring AI feature handles transient provider errors (HTTP 429/5xx) automatically?",
     "o": ["Spring AI retry support, tuned with spring.ai.retry.* properties",
           "The ChatMemory advisor, which replays the last request automatically on error",
           "Reactor's retry operator, which call() applies automatically",
           "Nothing built in; every provider error surfaces immediately"],
     "e": "Provider clients use a RetryTemplate from Spring AI's retry auto-configuration. Tune max-attempts and exponential backoff, "
          "and decide which status codes are retryable. Combine with timeouts and a circuit breaker (e.g. Resilience4j) for production."},

    # ---------------- Streaming ----------------
    {"t": "stream", "q": "How do you stream an answer to a browser with Spring AI?",
     "o": ["Return stream().content() as Flux<String> with text/event-stream",
           "Return call().content() and let Tomcat chunk the response",
           "Return stream().chatResponse() as a List after collecting it",
           "Open a WebSocket, since SSE is not supported by Spring AI"],
     "e": "stream() returns a reactive Flux. Returning it from a controller with text/event-stream sends Server-Sent Events as tokens "
          "arrive, which improves perceived latency. It works in Spring MVC too (async support), not only WebFlux."},
    {"t": "stream", "q": "What is a common limitation when streaming compared with call()?",
     "o": ["entity() needs the full JSON, so typed output requires aggregating first",
           "System prompts are ignored by most providers when streaming is enabled on the request",
           "Advisors are never applied when a request is streamed",
           "Tool calling is disabled for every provider when streaming"],
     "e": "entity() needs complete JSON, so it is a call() feature; with streams you aggregate first. Advisors must implement "
          "StreamAdvisor to take part in streaming, and token usage arrives only in the final chunk (and only if the provider sends it)."},
    {"t": "stream", "q": "In a custom StreamAdvisor, how should you log the complete answer without breaking streaming?",
     "o": ["Use a message aggregator that passes chunks on and logs on completion",
           "Call block() on the Flux inside the advisor, then log the full result before returning",
           "Switch the request to call() inside the advisor before logging",
           "Subscribe to the Flux a second time in the advisor to read it"],
     "e": "Blocking a reactive stream defeats streaming and can deadlock event-loop threads. Spring AI provides an aggregator that "
          "passes chunks through unchanged while assembling the final response for logging, metrics or memory storage."},
    {"t": "stream", "q": "A user closes the browser tab in the middle of a long streamed answer. What should happen in a well designed app?",
     "o": ["Cancellation propagates upstream and stops the provider stream",
           "The model finishes generating; the tokens are billed anyway",
           "Spring AI buffers the answer and resends it on reconnect",
           "The Flux errors and the retry template restarts the call"],
     "e": "Reactive cancellation propagates upstream: when the client disconnects, the subscription is disposed and the provider HTTP "
          "stream is closed, saving tokens. Make sure you do not subscribe a second time or buffer the whole Flux elsewhere."},

    # ---------------- Structured Output ----------------
    {"t": "struct", "q": "How does chatClient.prompt().user(q).call().entity(Person.class) work internally?",
     "o": ["A BeanOutputConverter adds schema instructions, then parses the reply",
           "The provider compiles the record class and returns an instance",
           "Spring AI asks the model for YAML and maps it with SnakeYAML",
           "Jackson parses the free text using heuristics based on the record's field names"],
     "e": "StructuredOutputConverter implementations (BeanOutputConverter, ListOutputConverter, MapOutputConverter) supply format "
          "instructions and convert the text. Because it relies on the model following instructions, validate results; where supported, "
          "use the provider's native structured output / JSON schema mode for stronger guarantees."},
    {"t": "struct", "q": "How do you get a List<Product> (a generic type) as structured output?",
     "o": ["entity(new ParameterizedTypeReference<List<Product>>() {})",
           "entity(List.class) and an unchecked cast to List<Product>",
           "entity(Product[].class), since lists are not supported",
           "entity(Product.class), called once for each element you expect in the list"],
     "e": "Java erases generics, so a ParameterizedTypeReference keeps the full type for schema generation and Jackson parsing. "
          "Wrapping the list in a record (record Products(List<Product> items)) is another robust option."},
    {"t": "struct", "q": "The model sometimes returns invalid JSON for entity(). What is a robust production approach?",
     "o": ["Native schema mode if available, low temperature, validate, bounded retry",
           "Raise the temperature so the model explores other JSON layouts",
           "Catch the exception and return null, so the calling service can decide what to do",
           "Switch to streaming so partial JSON can be repaired chunk by chunk"],
     "e": "Structured output is a contract the model may break. Defence in depth: provider structured-output features, clear field "
          "descriptions (@JsonPropertyDescription), Bean Validation on the result, a bounded retry (possibly with the error fed back), "
          "and a check that the finish reason is not 'length'."},
    {"t": "struct", "q": "Why use a Java record rather than Map<String,Object> as an output target?",
     "o": ["A record gives a precise schema, type safety and validation",
           "Maps cannot be deserialised by Jackson from model output",
           "Records make the model generate fewer output tokens",
           "Records are required because MapOutputConverter was removed"],
     "e": "The converter derives the schema from the target type, so a record with well named, documented fields tells the model "
          "exactly what to produce. MapOutputConverter exists for dynamic shapes, but typed records are easier to test and evolve."},

    # ---------------- Advisors ----------------
    {"t": "advisor", "q": "What is an Advisor in Spring AI?",
     "o": ["An interceptor around the call that can change request and response",
           "A small model that reviews each answer before it is returned to the user",
           "A Boot health indicator that reports provider availability",
           "A configuration bean that picks the model for each request"],
     "e": "Advisors implement CallAdvisor and/or StreamAdvisor. Each receives a ChatClientRequest and a chain, may change the prompt "
          "or context, call chain.nextCall(...) and post-process the ChatClientResponse. Memory, RAG, logging, safeguards and the tool "
          "loop are all built as advisors."},
    {"t": "advisor", "q": "How is the execution order of advisors determined?",
     "o": ["getOrder(): lower values see the request first and the response last",
           "getOrder(): lower values see the request last and the response first, like a stack",
           "Registration order only; getOrder() is used for logging",
           "Alphabetical order of bean names, unless @Primary is set"],
     "e": "Advisors form a stack. The one with the lowest order sees the request first and the response last. This matters: e.g. a "
          "memory advisor should add history before a RAG advisor augments the question, and a logger placed last sees the final prompt."},
    {"t": "advisor", "q": "Which built-in advisor logs requests and responses for debugging?",
     "o": ["SimpleLoggerAdvisor, logging at DEBUG level",
           "QuestionAnswerAdvisor, with its trace flag on",
           "SafeGuardAdvisor, which logs blocked requests",
           "MessageChatMemoryAdvisor, which logs history"],
     "e": "SimpleLoggerAdvisor logs at DEBUG, and you can customise what is printed with request/response formatter functions. In "
          "production, prefer observability (metrics and traces) and be careful not to log personal data."},
    {"t": "advisor", "q": "Advisors need to share data during one request (e.g. retrieved documents for a later advisor). How?",
     "o": ["Through the advisor context map carried by the request and response",
           "Through request-scoped beans injected into each advisor",
           "Through static fields guarded by a synchronized block",
           "Through extra system messages that later advisors in the chain parse back out"],
     "e": "The context map travels with the request through the chain and back with the response. QuestionAnswerAdvisor, for example, "
          "puts the retrieved documents in the response context, so callers can read them to show sources."},

    # ---------------- Chat Memory ----------------
    {"t": "memory", "q": "Why does a chatbot need ChatMemory at all?",
     "o": ["LLM APIs are stateless; history must be resent with each request",
           "Providers keep only one turn of history unless memory is enabled",
           "It is required for the model to reuse its KV cache across turns of a conversation",
           "It lowers cost, because remembered tokens are not billed again"],
     "e": "Each call is independent. ChatMemory stores messages per conversation id and a memory advisor adds them to the prompt. "
          "This costs tokens, so you need a window or summarisation strategy."},
    {"t": "memory", "q": "What is the difference between ChatMemory and ChatMemoryRepository?",
     "o": ["ChatMemory applies the policy (e.g. last N); the repository just stores",
           "The repository applies the window policy; ChatMemory just stores and loads messages",
           "They are aliases kept for backward compatibility",
           "ChatMemory is in-memory; the repository is always JDBC"],
     "e": "MessageWindowChatMemory (default window 20 messages, keeping system messages) applies the policy; the storage is pluggable: "
          "InMemoryChatMemoryRepository, JdbcChatMemoryRepository, Cassandra, Neo4j and others. Use a persistent repository for "
          "multi-instance deployments."},
    {"t": "memory", "q": "MessageChatMemoryAdvisor vs PromptChatMemoryAdvisor: what is the difference?",
     "o": ["The first adds history as messages; the second as text in the system prompt",
           "The first stores the history in a vector store; the second keeps it in a plain list",
           "The first works only for streaming; the second only for call()",
           "The first keeps user messages only; the second keeps both roles"],
     "e": "MessageChatMemoryAdvisor keeps the role structure (user/assistant messages), which most models handle best. "
          "PromptChatMemoryAdvisor injects the history as text, useful for models without multi-message support. "
          "VectorStoreChatMemoryAdvisor retrieves only the relevant past messages from a vector store, good for very long histories."},
    {"t": "memory", "q": "In a multi-user app, how do you prevent one user's memory leaking into another's conversation?",
     "o": ["A per-user conversation id set server-side from the authenticated user",
           "A conversation id sent by the browser in a custom header, read by an interceptor",
           "A separate ChatClient bean created for each logged-in user",
           "Clearing the shared memory at the start of every request"],
     "e": "Memory is keyed by conversation id. Derive it server-side from the authenticated user (never trust a raw id from the client), "
          "and apply retention and deletion policies for privacy (GDPR)."},

    # ---------------- Tool Calling ----------------
    {"t": "tools", "q": "In tool calling, who actually executes the tool?",
     "o": ["Your application: the model only returns the tool name and arguments",
           "The provider, which runs the method in a sandbox on its own servers and returns output",
           "The model, which calls your REST endpoint directly over HTTP",
           "The MCP server, which is required for any tool calling"],
     "e": "The model decides to call a tool and produces arguments. Spring AI's ToolCallingManager invokes the matching ToolCallback, "
          "adds a ToolResponseMessage and calls the model again, looping until it returns a final answer. Your code keeps control of "
          "side effects and security."},
    {"t": "tools", "q": "Why are the description attributes of @Tool and @ToolParam so important?",
     "o": ["The model sees only the name, description and schema to pick a tool",
           "They become the Javadoc used by Spring's API documentation",
           "They are used as metric tags, not sent to the model",
           "They define the HTTP route that the provider calls"],
     "e": "Descriptions are part of the prompt. Clear, specific descriptions (what it does, when to use it, units and formats of "
          "parameters) strongly improve tool selection and argument quality. Ambiguous names cause wrong or missing calls."},
    {"t": "tools", "q": "How do you pass a tenant id to a tool without letting the model see or invent it?",
     "o": ["ToolContext: set it on the request and add a ToolContext parameter",
           "A @ToolParam marked required, so the model must supply it",
           "A line in the system prompt that asks the model to always pass the tenant id along",
           "A static field set before the call and cleared after it"],
     "e": "ToolContext data is passed to the method by the framework and is never sent to the model. This is the right channel for "
          "security-sensitive values like user id, tenant id or auth tokens, so the model cannot spoof them."},
    {"t": "tools", "q": "When would you disable internal tool execution (internalToolExecutionEnabled=false)?",
     "o": ["To run the loop yourself, e.g. human approval before risky actions",
           "To let the provider execute the tools on its side, which lowers latency",
           "To enable streaming, which needs tool execution turned off",
           "To force the model to call every registered tool once"],
     "e": "With user-controlled execution, the ChatResponse contains tool calls; you call ToolCallingManager.executeToolCalls(...) when "
          "you decide and send the results back. This enables human-in-the-loop approval, auditing and custom iteration limits."},

    # ---------------- Agentic Patterns ----------------
    {"t": "agents", "q": "What does the 'routing' agentic pattern do?",
     "o": ["Classify the input first, then send it to a specialised handler",
           "Retry the same prompt on another model until one succeeds",
           "Send the input to every handler and keep the longest answer",
           "Split the input into sentences and route each to a tool"],
     "e": "Routing (from the 'Building effective agents' patterns that Spring AI documents) uses a cheap classification step to pick a "
          "specialised path, e.g. billing vs technical support, or a small vs large model. It improves quality and cost."},
    {"t": "agents", "q": "What is the evaluator-optimizer pattern?",
     "o": ["One call generates, another evaluates and gives feedback, in a loop",
           "Several models answer at once and the cheapest answer is kept",
           "A model rewrites its own prompt until token usage is minimal",
           "An evaluator ranks the providers and routes the traffic to the best one each hour"],
     "e": "It works when there are clear evaluation criteria (code that must compile, a translation that must keep meaning). Always cap "
          "iterations to bound cost and latency."},
    {"t": "agents", "q": "When should you prefer a fixed workflow (chain/routing) over an autonomous agent loop?",
     "o": ["When the steps are known: workflows are cheaper and easier to test",
           "Only when no tools are needed, since fixed workflows cannot call any tools",
           "When latency is unimportant, since workflows are always slower",
           "Never; autonomous agents are more reliable for known steps"],
     "e": "Autonomous agents are flexible but less predictable, more expensive and harder to debug. Start with the simplest workflow that "
          "meets the requirement and add autonomy only where open-ended decisions are needed."},
    {"t": "agents", "q": "What is the purpose of the parallelization pattern (sectioning / voting)?",
     "o": ["Run independent subtasks concurrently, or vote over repeated runs",
           "Split one prompt across several GPUs to generate faster",
           "Store conversation memory in several databases at once",
           "Send the same request to all providers to compare prices"],
     "e": "Sectioning splits work (e.g. analyse each document section) and runs calls concurrently, e.g. with virtual threads or "
          "CompletableFuture. Voting runs the same prompt several times and takes the majority, improving reliability for classification."},

    # ---------------- Embeddings ----------------
    {"t": "embed", "q": "What is an embedding?",
     "o": ["A fixed-length vector that encodes meaning; similar texts are close",
           "A compressed form of the text that can be decoded back to the original words",
           "A list of token ids produced by the model's tokenizer",
           "A hash of the text used to detect duplicate documents"],
     "e": "EmbeddingModel.embed(text) returns float[] of the model's dimension (e.g. 768, 1024, 1536). Distance between vectors "
          "(often cosine similarity) approximates semantic similarity, which powers semantic search and RAG."},
    {"t": "embed", "q": "You switch embedding model from 768 to 1024 dimensions. What must you do?",
     "o": ["Re-embed every document and rebuild the table and index",
           "Nothing: vectors from both models are directly comparable",
           "Pad the old 768-dim vectors with zeros to reach 1024",
           "Re-embed queries only; stored vectors can stay as they are"],
     "e": "Vectors from different models live in different spaces and are not comparable even with the same size. Indexing and querying "
          "must use the same model. Plan migrations: dual-write or rebuild a new index then switch."},
    {"t": "embed", "q": "Which similarity measure is most commonly used for text embeddings?",
     "o": ["Cosine similarity, comparing vector direction",
           "Hamming distance on the binary vector form",
           "Levenshtein distance on the source texts",
           "Jaccard index on the token sets"],
     "e": "Cosine similarity compares vector direction, not magnitude. Many models produce normalised vectors so dot product equals cosine. "
          "Vector stores let you pick the distance type (e.g. PGVector COSINE_DISTANCE, EUCLIDEAN_DISTANCE, NEGATIVE_INNER_PRODUCT)."},
    {"t": "embed", "q": "How do you reduce cost and time when embedding thousands of chunks?",
     "o": ["Batch requests and skip unchanged content using a content hash",
           "Embed one sentence per request to stay under rate limits",
           "Use the chat model instead, which produces embeddings more cheaply in batches",
           "Lower the embedding dimension per request with an option"],
     "e": "Vector stores use a BatchingStrategy to group documents within the model's token limits. Store a content hash in metadata so "
          "re-ingestion skips unchanged documents."},

    # ---------------- Vector Stores ----------------
    {"t": "vector", "q": "Which call performs a semantic search with a limit and minimum score?",
     "o": ["similaritySearch(SearchRequest...query(q).topK(5).similarityThreshold(0.7))",
           "embeddingModel.search(q, 5, 0.7) on the injected EmbeddingModel",
           "vectorStore.findAll() followed by sorting the documents on their score field",
           "vectorStore.query(\"SELECT ... ORDER BY score LIMIT 5\")"],
     "e": "SearchRequest sets the query text, topK, similarityThreshold and an optional filterExpression. The store embeds the query with "
          "the configured EmbeddingModel and returns Documents with a score."},
    {"t": "vector", "q": "How do you restrict a search to documents of one department and year?",
     "o": ["A metadata filter expression in the SearchRequest",
           "Adding the department and year words to the query text",
           "Filtering the topK results in Java after the search",
           "Creating a separate vector store bean per department"],
     "e": "Spring AI has a portable filter language (string or FilterExpressionBuilder) translated to each store's native filter. "
          "Filtering in the store happens before topK, while post-filtering can return too few results. It is also key for multi-tenancy."},
    {"t": "vector", "q": "What does an HNSW index in PGVector provide?",
     "o": ["Approximate nearest neighbour search: fast, at a small accuracy cost",
           "Exact nearest neighbour search with no accuracy trade-off and constant query time",
           "Full-text keyword search over the document content",
           "Compression of vectors to cut storage in half"],
     "e": "HNSW builds a graph for approximate nearest neighbour search. PGVector in Spring AI supports index types (HNSW, IVFFLAT, NONE), "
          "distance types and dimensions, set with spring.ai.vectorstore.pgvector.* properties. initialize-schema creates the table in dev; "
          "use migrations in production."},
    {"t": "vector", "q": "When is SimpleVectorStore appropriate?",
     "o": ["Prototypes, tests and small data sets, kept in memory",
           "Production clusters, since it replicates between nodes",
           "Very large corpora, thanks to its HNSW index",
           "Multi-tenant apps, since it isolates data per tenant"],
     "e": "SimpleVectorStore does a brute-force scan in memory. For production use a real store (PGVector, Redis, Elasticsearch, Milvus, "
          "Qdrant, Chroma, MongoDB Atlas...) with persistence, indexing and filtering."},

    # ---------------- ETL ----------------
    {"t": "etl", "q": "What are the three stages of the Spring AI ETL pipeline?",
     "o": ["DocumentReader -> DocumentTransformer -> DocumentWriter",
           "DocumentLoader -> EmbeddingModel -> ChatModel",
           "DocumentParser -> DocumentSplitter -> DocumentIndexer",
           "ResourceReader -> TextSplitter -> VectorIndexer"],
     "e": "Readers (TikaDocumentReader, PagePdfDocumentReader, MarkdownDocumentReader, JsonReader, TextReader) produce Documents; "
          "transformers (TokenTextSplitter, KeywordMetadataEnricher, SummaryMetadataEnricher) change them; a writer such as a VectorStore "
          "stores them. They are Supplier/Function/Consumer so they compose."},
    {"t": "etl", "q": "Why split documents into chunks before embedding?",
     "o": ["Models have input limits and small chunks give precise retrieval",
           "Vector stores reject any document longer than 512 characters",
           "Chunks are needed so that each one can be encrypted separately with its own key",
           "Splitting is only needed for PDFs, which mix pages together"],
     "e": "TokenTextSplitter splits by tokens with configurable chunk size. Too small loses context; too big dilutes meaning and wastes "
          "prompt tokens. Use structure-aware splitting (headings, paragraphs) when possible and keep source metadata on every chunk."},
    {"t": "etl", "q": "How do you make re-ingestion idempotent so updated files do not create duplicates?",
     "o": ["Stable ids or a source key, delete the old chunks, then write new ones",
           "Re-ingest everything nightly; the vector store merges duplicate chunks by itself",
           "Rely on a high similarity threshold to hide duplicate chunks",
           "Rely on the model to ignore repeated passages in the context"],
     "e": "Store source path, version or content hash in metadata. On change, delete the source's chunks with a filter expression and add "
          "the new ones. Without this, stale and duplicate chunks degrade answers."},
    {"t": "etl", "q": "Which reader would you use for many formats (DOCX, PPTX, HTML, PDF) with one API?",
     "o": ["TikaDocumentReader",
           "TextReader",
           "JsonReader",
           "MarkdownDocumentReader"],
     "e": "Tika detects and extracts text from many formats. For PDFs where page layout matters, PagePdfDocumentReader or "
          "ParagraphPdfDocumentReader give page or paragraph level documents with page metadata, useful for citations."},

    # ---------------- RAG ----------------
    {"t": "rag", "q": "What problem does RAG solve?",
     "o": ["It grounds answers in your current data by adding retrieved documents",
           "It fine-tunes the model on your documents at application startup, then reloads it",
           "It shrinks the model by removing knowledge you do not need",
           "It stores past answers and replays them for similar questions"],
     "e": "Retrieval Augmented Generation reduces hallucinations and gives access to private and fresh knowledge without fine-tuning. "
          "Quality depends mostly on retrieval: chunking, embeddings, filters and topK."},
    {"t": "rag", "q": "QuestionAnswerAdvisor vs RetrievalAugmentationAdvisor?",
     "o": ["QuestionAnswerAdvisor is simple; RetrievalAugmentationAdvisor is modular",
           "RetrievalAugmentationAdvisor is simple; QuestionAnswerAdvisor is modular",
           "QuestionAnswerAdvisor is for PDFs; RetrievalAugmentationAdvisor for web",
           "They are the same; one name is kept for backward compatibility"],
     "e": "RetrievalAugmentationAdvisor composes modules: RewriteQueryTransformer, CompressionQueryTransformer, TranslationQueryTransformer, "
          "MultiQueryExpander, VectorStoreDocumentRetriever, ConcatenationDocumentJoiner and ContextualQueryAugmenter. Use it when you "
          "need advanced or 'modular RAG' behaviour."},
    {"t": "rag", "q": "In a conversation, the user asks 'and what about the second one?'. Retrieval returns nothing useful. Which module helps?",
     "o": ["CompressionQueryTransformer, which builds a standalone query from history",
           "TranslationQueryTransformer, which translates the query to English",
           "ConcatenationDocumentJoiner, which merges the results of several queries into one list",
           "KeywordMetadataEnricher, which adds keywords to the stored chunks"],
     "e": "Follow-up questions lack context for vector search. Compression uses history to build a self-contained query; RewriteQueryTransformer "
          "cleans verbose queries; MultiQueryExpander creates variants to improve recall."},
    {"t": "rag", "q": "What should the assistant do when no relevant documents are found?",
     "o": ["Say it does not know, e.g. ContextualQueryAugmenter with allowEmptyContext=false",
           "Answer from general knowledge, since the model is usually right",
           "Retry the search with a similarity threshold of zero",
           "Return the closest document even if it is not relevant"],
     "e": "For enterprise assistants, refusing is better than hallucinating. The augmenter can be configured with an empty-context prompt. "
          "Also return the source documents (from the response context) so users can verify the answer."},

    # ---------------- MCP ----------------
    {"t": "mcp", "q": "What is the Model Context Protocol (MCP)?",
     "o": ["An open JSON-RPC protocol for apps to use tools, resources and prompts",
           "A Spring protocol for sending prompts between microservices",
           "A binary protocol for streaming tokens from model providers to Java applications",
           "A standard for packaging and versioning fine-tuned models"],
     "e": "MCP decouples tools from apps: one server can serve any MCP host (Claude Desktop, IDEs, Spring AI apps). Roles: host (the app), "
          "client (one connection per server) and server. Spring AI provides client and server Boot starters built on the MCP Java SDK."},
    {"t": "mcp", "q": "Which MCP transports exist?",
     "o": ["stdio, SSE (legacy) and Streamable HTTP",
           "gRPC, WebSocket and stdio",
           "HTTP/2 push, SSE and AMQP",
           "Streamable HTTP and WebSocket only; stdio was removed"],
     "e": "stdio is used to launch local servers as subprocesses (e.g. npx filesystem server). Remote servers use HTTP: Streamable HTTP "
          "replaces the older SSE transport. In Spring AI you choose it on the server, e.g. spring.ai.mcp.server.protocol=STREAMABLE."},
    {"t": "mcp", "q": "How does a Spring AI app make MCP server tools available to the ChatClient?",
     "o": ["The MCP client starter exposes server tools as ToolCallbacks",
           "The server's tools must be re-declared as @Tool methods in the app",
           "The model connects to the MCP server itself and calls the tools",
           "The tools are listed in application.yml and called over REST"],
     "e": "With spring.ai.mcp.client.* connections configured, Spring AI discovers each server's tools and wraps them (e.g. "
          "SyncMcpToolCallbackProvider). The model then calls them like local @Tool methods; the client forwards calls over MCP."},
    {"t": "mcp", "q": "Which annotations does Spring AI offer to build an MCP server?",
     "o": ["@McpTool, @McpResource and @McpPrompt",
           "@Tool, @Resource and @Prompt from spring-ai-core",
           "@EnableMcpServer, @McpEndpoint and @McpMethod",
           "@RestController methods annotated with @McpExposed"],
     "e": "The annotations map to MCP primitives: tools (model-controlled actions), resources (app-controlled data identified by URI) and "
          "prompts (user-selected templates). Secure remote servers with OAuth 2.0 (the server is a resource server validating tokens)."},

    # ---------------- Multimodality ----------------
    {"t": "multi", "q": "How do you send an image with a question to a vision model through ChatClient?",
     "o": [".user(u -> u.text(...).media(MimeTypeUtils.IMAGE_PNG, image))",
           ".system(s -> s.media(MimeTypeUtils.IMAGE_PNG, image)) then .user(text)",
           "Base64-encode the image into the user text and set a flag option",
           "Add the image to the vector store and ask about its document id"],
     "e": "UserMessage carries a list of Media (MIME type + data or URL). The provider module converts it to the provider's format. "
          "Combine with entity() to turn an image into a record, e.g. a receipt reader."},
    {"t": "multi", "q": "Which Spring AI interface generates images from text?",
     "o": ["ImageModel with an ImagePrompt and ImageOptions",
           "ChatModel with a responseFormat option set to image",
           "EmbeddingModel decoded through an image converter",
           "MediaModel with a GenerationRequest"],
     "e": "ImageModel.call(new ImagePrompt(text, options)) returns an ImageResponse with URLs or base64 data. Providers include OpenAI, "
          "Stability AI and others."},
    {"t": "multi", "q": "How would you build a 'voice note to summary' pipeline?",
     "o": ["TranscriptionModel -> ChatClient summary -> optional TextToSpeechModel",
           "TextToSpeechModel -> ChatClient summary -> TranscriptionModel",
           "EmbeddingModel on the raw audio bytes -> vector search -> ChatClient summary",
           "ChatClient with the audio as text Media -> ImageModel"],
     "e": "Spring AI abstracts audio with TranscriptionModel (e.g. Whisper) and TextToSpeechModel. Chaining models is a typical "
          "multimodal workflow; consider async processing for long audio."},
    {"t": "multi", "q": "What is a key cost consideration for vision requests?",
     "o": ["Images become many input tokens; resize, crop and set the detail level",
           "Images are free; only the text part of the prompt is counted and billed by providers",
           "Images are billed as output tokens, so cap maxTokens",
           "Images are billed per request, whatever their size"],
     "e": "Providers bill images by size/tiles. Downscale before sending, send only the relevant region, and track usage in ChatResponse "
          "metadata like any other request."},

    # ---------------- Evaluation & Testing ----------------
    {"t": "eval", "q": "Why can't you test AI answers with assertEquals on the text?",
     "o": ["Wording varies between runs and models; test the meaning instead",
           "JUnit cannot call reactive or HTTP-based clients",
           "Answers always differ in letter case, which breaks equals",
           "Spring AI hides the answer text from test code"],
     "e": "LLM output is non-deterministic. Use structural assertions (valid JSON, required fields), keyword checks for facts, and "
          "LLM-as-judge evaluators for relevancy and faithfulness."},
    {"t": "eval", "q": "What does RelevancyEvaluator check?",
     "o": ["Whether the answer is relevant to the question and its context",
           "Whether every claim in the answer appears word for word in the retrieved documents",
           "Whether the answer stays under the configured token budget",
           "Whether retrieval returned at least topK documents"],
     "e": "RelevancyEvaluator uses a judge ChatClient with an EvaluationRequest(question, documents, answer) and returns an "
          "EvaluationResponse with isPass(). FactCheckingEvaluator checks whether a claim is supported by the documents (hallucination check)."},
    {"t": "eval", "q": "What is a known risk of LLM-as-a-judge?",
     "o": ["The judge can be biased or inconsistent; calibrate it on labelled data",
           "The judge always agrees with the model it is grading",
           "The judge cannot run inside JUnit, only in production",
           "The judge needs a vector store to work"],
     "e": "Judges may favour long answers, their own style or fail on parsing (e.g. replying 'Yes, because...' when a bare 'yes' is "
          "expected). Keep a golden dataset, measure judge agreement with humans, and track pass rates over time rather than single runs."},
    {"t": "eval", "q": "How do you write fast, reliable unit tests for code that uses ChatClient?",
     "o": ["Stub the ChatModel in unit tests; keep real-model evals in a separate suite",
           "Call the real model in every unit test with temperature 0",
           "Record one real answer from the model and assertEquals against it in every test",
           "Skip tests for AI code; review answers manually instead"],
     "e": "Unit tests should be deterministic: stub the model to test prompt building, parsing, tool wiring and error handling. Run "
          "evaluation tests against a real model (e.g. Testcontainers with Ollama) in CI on a schedule or before release."},

    # ---------------- Observability ----------------
    {"t": "obs", "q": "How does Spring AI provide observability?",
     "o": ["Micrometer observations: metrics and traces for clients, models and tools",
           "A built-in admin UI that stores every prompt in H2",
           "Plain System.out logging of prompts and answers",
           "A proprietary agent that must be added to the JVM"],
     "e": "With Actuator and Micrometer, Spring AI emits observations following the OpenTelemetry GenAI semantic conventions. You can "
          "export metrics to Prometheus and traces to Zipkin/Jaeger/OTLP to see each model call, advisor and tool span."},
    {"t": "obs", "q": "Which metric would you use to build a token cost dashboard?",
     "o": ["gen_ai.client.token.usage, tagged by token type and model",
           "http.server.requests, multiplied by an average token count",
           "spring.ai.chat.cost, which is computed from list prices",
           "jvm.memory.used, since tokens are held in memory"],
     "e": "Multiply input and output token counts by the model's price to estimate cost per endpoint, user or tenant. Add alerts on "
          "spikes, and use gen_ai.client.operation timers for latency."},
    {"t": "obs", "q": "Why is logging of prompt and completion content disabled by default in observations?",
     "o": ["Prompts and answers can hold personal or confidential data",
           "Logging text adds seconds of latency to every request",
           "Micrometer tags cannot contain strings longer than 64 chars",
           "Providers forbid storing prompts in their terms of use"],
     "e": "Properties such as spring.ai.chat.observations.log-prompt / log-completion turn it on. Treat traces as sensitive data, apply "
          "masking, retention limits and access control."},
    {"t": "obs", "q": "Users report the assistant is slow. What do traces typically reveal?",
     "o": ["Which span dominates: retrieval, tool calls or the model, and loop counts",
           "The model's internal attention weights for each token",
           "Only the client's network speed, since trace spans start and end at the browser",
           "Only the total time, since model calls are not traced"],
     "e": "With tracing, a request shows nested spans for advisors, vector search, tool executions and model calls. You often find "
          "too many tool iterations, slow external APIs or an oversized prompt (high input tokens)."},

    # ---------------- Security & Guardrails ----------------
    {"t": "security", "q": "What is indirect prompt injection?",
     "o": ["Malicious instructions hidden in retrieved data or tool results",
           "An attacker editing the system prompt file on the server through a path traversal",
           "SQL injection through the vector store filter expression",
           "A user sending many requests to exhaust the token quota"],
     "e": "In RAG and tool use, untrusted content enters the prompt. Mitigate: treat retrieved text as data (clear delimiters, instructions "
          "to ignore embedded commands), least-privilege tools, human approval for sensitive actions, and output validation."},
    {"t": "security", "q": "What does SafeGuardAdvisor do?",
     "o": ["Blocks requests containing configured sensitive words before the model",
           "Encrypts prompts before they are sent to the provider",
           "Authenticates users with OAuth 2.0 before the model is called and blocks the rest",
           "Scans the model's answers with a moderation model"],
     "e": "SafeGuardAdvisor is a simple keyword guardrail. Production systems layer it with moderation models (ModerationModel), "
          "input/output validation, rate limiting and policy prompts. Keyword lists alone are easy to bypass."},
    {"t": "security", "q": "What is the most important rule when exposing tools that change data (e.g. cancelOrder)?",
     "o": ["Check authorisation in the tool code for the real user; never trust arguments",
           "Tell the model in the system prompt to call the tool only when it is safe to do so",
           "Hide the tool from the model until the user asks for it",
           "Lower the temperature so the model does not misuse the tool"],
     "e": "The model can be manipulated. Every tool must check permissions and validate inputs as if called by an untrusted client. "
          "Add confirmation steps for irreversible actions and audit every call."},
    {"t": "security", "q": "How do you secure a remote MCP server built with Spring AI?",
     "o": ["An OAuth 2.0 resource server validating tokens, scopes and audience",
           "A shared API key written in each tool's description",
           "A non-standard port that only the client knows",
           "The MCP handshake, which authenticates clients by itself"],
     "e": "The MCP authorization spec builds on OAuth 2.1. With Spring Security the server validates JWTs; the client obtains tokens "
          "(e.g. client credentials or authorization code). Use HTTPS and least-privilege scopes per tool."},

    # ---------------- Production & Performance ----------------
    {"t": "prod", "q": "Which technique reduces cost most for repeated identical questions?",
     "o": ["Exact or semantic response caching plus provider prompt caching",
           "Raising the temperature so fewer tokens are generated",
           "Adding advisors, since they cache the request context",
           "Streaming, since streamed tokens are billed at a lower rate than blocking calls"],
     "e": "An application cache (exact-match key, or a semantic cache via a vector store) avoids calls. Provider prompt caching (e.g. "
          "Anthropic, OpenAI) cuts the cost of repeated system prompts and documents. Also choose the smallest model that passes your evals."},
    {"t": "prod", "q": "Blocking ChatClient calls take seconds. How do you keep a Spring MVC app scalable on Java 21?",
     "o": ["Enable virtual threads or stream reactively, and set timeouts",
           "Raise the Tomcat thread pool to tens of thousands of platform threads",
           "Run each call in parallelStream() on the common pool",
           "Use @Async on the controller with the default executor"],
     "e": "LLM calls are I/O bound. Virtual threads let blocking code scale cheaply. Always configure HTTP client timeouts and limits "
          "(bulkheads) so a slow provider does not exhaust resources."},
    {"t": "prod", "q": "Your provider has an outage. What is a good resilience strategy?",
     "o": ["Circuit breaker plus fallback to another ChatModel, and a clear message",
           "Retry with no limit until the provider comes back",
           "Queue every request in memory until the outage ends",
           "Return cached answers to unrelated questions"],
     "e": "Thanks to the portable abstraction you can fail over to another ChatModel bean. Combine Resilience4j circuit breakers, bounded "
          "retries and degraded features (e.g. search results without generation)."},
    {"t": "prod", "q": "How do you protect your budget from a single user abusing an AI endpoint?",
     "o": ["Per-user rate limits and token quotas, size caps and usage alerts",
           "A secret URL for the endpoint, shared only with real users",
           "Streaming for all endpoints, since it is cheaper per token",
           "A higher maxTokens, so that users get everything they need in a single call"],
     "e": "Track token usage per user/tenant from ChatResponse metadata or metrics, enforce quotas (e.g. Bucket4j), cap input length and "
          "output tokens, and limit tool-loop iterations."},
]



def level(pct):
    if pct >= 85:
        return "Expert-ready"
    if pct >= 70:
        return "Practitioner"
    if pct >= 50:
        return "Apprentice"
    return "Novice"
