---
title: Spring AI Lab: Ticket-Triage Agent (Routing + Review Loop, Lab 3.3)
subtitle: Lab 3.3 of the free Spring AI course: Routing + evaluator-optimizer, step by step, on a free local model.
tags: Java, Spring Boot, Artificial Intelligence, LLM, AI Agents
video: https://www.youtube.com/watch?v=ZGiyrQWy6vc
slug: spring-ai-s3-03-lab-ticket-triage
---

3, the last lab of section three. Today you'll build a ticket-triage agent with two patterns: routing, and evaluator-optimizer.

And you'll see its limits honestly, because that's what matters before you ship an agent.

It's lab 3.3 of my free **Spring AI: Novice to Expert** course, where every lesson has a concept part and a hands-on lab, and everything runs on a free local model with Ollama.

🎥 **Prefer video?** Watch the full tutorial here:

{VIDEO}

## The agent's workflow

Here's the plan. A support ticket comes in.

The router classifies it: billing, technical or shipping, and urgent or not.

The right expert prompt writes a reply.

A reviewer checks it, with feedback. Up to three drafts.

Gemma writes, because it writes well. And for reviewing, we use the stronger Qwen seven B, with a per-request option.

- **Route**: Classify → **category** + **urgent**
- **Draft**: The category's **expert prompt** writes
- **Review**: Approve or give **feedback**, max **3 drafts**

**Writer: gemma3:4b · Reviewer: qwen2.5:7b**

![The agent's workflow](images/01-the-agent-s-workflow.jpg)

## Step 1: The records

A Category enum, a Triage record for the router, a Review record for the reviewer, and the final TicketResult.

**`Category.java`** (`src/main/java/dev/course/triage/Category.java`):

```java
package dev.course.triage;

public enum Category { BILLING, TECHNICAL, SHIPPING }
```

**`Triage.java`** (`src/main/java/dev/course/triage/Triage.java`):

```java
package dev.course.triage;

public record Triage(Category category, boolean urgent) {
}
```

**`TicketResult.java`** (`src/main/java/dev/course/triage/TicketResult.java`):

```java
package dev.course.triage;

public record TicketResult(Category category, boolean urgent, String reply, int drafts) {
}
```

**`Review.java`** (`src/main/java/dev/course/triage/Review.java`):

```java
package dev.course.triage;

public record Review(boolean approved, String feedback) {
}
```

Every step returns a type. That's how our Java code can make decisions, not just pass text around.

![The reviewer's answer, typed](images/02-the-reviewer-s-answer-typed.jpg)

## Step 2: Route the ticket

In TriageAgent, a map of expert prompts, one per category. Each one is short and focused.

**`TriageAgent.java`**:

```java
package dev.course.triage;

import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.prompt.ChatOptions;
import org.springframework.stereotype.Service;

@Service
public class TriageAgent {

    private static final Logger log = LoggerFactory.getLogger(TriageAgent.class);
    private static final int MAX_DRAFTS = 3;
    private static final int MAX_WORDS = 120;
    private static final String REVIEWER_MODEL = "qwen2.5:7b";

    private static final Map<Category, String> EXPERTS = Map.of(
            Category.BILLING, "You are a billing specialist. Explain charges and refunds clearly.",
            Category.TECHNICAL, "You are a technical support engineer. Give clear numbered steps.",
            Category.SHIPPING, "You are a shipping specialist. Give delivery facts and next steps.");

    private final ChatClient chatClient;

    public TriageAgent(ChatClient.Builder builder) {
        this.chatClient = builder.build();
    }
```

![One expert per route](images/03-one-expert-per-route.jpg)

The handle method starts with the router: classify the ticket, into a Triage record, with native structured output.

**`TriageAgent.java`** (continued):

```java
    public TicketResult handle(String ticket) {
        // 1. Routing: classify the ticket, then pick the expert
        Triage triage = chatClient.prompt()
                .system("Classify the customer support ticket.")
                .user(ticket)
                .call()
                .entity(Triage.class, spec -> spec.useProviderStructuredOutput());
        log.info("ROUTE {} (urgent: {})", triage.category(), triage.urgent());
```

![Routing decision, typed](images/04-routing-decision-typed.jpg)

## Step 3: Draft and review

The loop: draft, review, and stop when approved, or after three drafts. The feedback of each review goes into the next draft.

**`TriageAgent.java`** (continued):

```java
        // 2. Evaluator-optimizer: the expert drafts, the reviewer checks, up to 3 drafts
        String reply = null;
        String feedback = "none yet";
        int drafts = 0;
        while (drafts < MAX_DRAFTS) {
            drafts++;
            reply = draft(triage.category(), ticket, feedback);
            Review review = review(ticket, reply);
            log.info("DRAFT {} approved: {} - {}", drafts, review.approved(), review.feedback());
            if (review.approved()) {
                break;
            }
            feedback = review.feedback();
        }
        return new TicketResult(triage.category(), triage.urgent(), reply, drafts);
    }
```

![Always a maximum](images/05-always-a-maximum.jpg)

The draft method uses the expert prompt for the category. And I tell it to return only the reply, and never claim an action, like a refund. It can't do anything.

**`TriageAgent.java`** (continued):

```java
    private String draft(Category category, String ticket, String feedback) {
        return chatClient.prompt()
                .system(EXPERTS.get(category) + " Write a short, polite reply to the customer. "
                        + "Return only the reply text: no subject line, no notes, no placeholders. "
                        + "Never say you already did something (like a refund): you cannot take actions.")
                .user(u -> u.text("Ticket: {ticket}\nReviewer feedback on your last draft: {feedback}")
                        .params(Map.of("ticket", ticket, "feedback", feedback)))
                .call()
                .content();
    }
```

![A rule for the writer](images/06-a-rule-for-the-writer.jpg)

## Step 4: Check in code

The review method starts with a word count, in plain Java.

**`TriageAgent.java`** (continued):

```java
    private Review review(String ticket, String reply) {
        // Code checks what code can check: the model is bad at counting words
        int words = reply.split("\\s+").length;
        if (words > MAX_WORDS) {
            return new Review(false, "Too long: " + words + " words. Use at most " + MAX_WORDS + " words.");
        }
        return chatClient.prompt()
                .system("You review support replies. Approve only if the reply answers the ticket, "
                        + "is polite, and does not claim that an action was already done (refund, fix, shipment). "
                        + "Reject replies that talk about drafts or reviewers.")
                .user(u -> u.text("Ticket: {ticket}\nReply: {reply}")
                        .params(Map.of("ticket", ticket, "reply", reply)))
                .options(ChatOptions.builder().model(REVIEWER_MODEL).temperature(0.0))
                .call()
                .entity(Review.class, spec -> spec.useProviderStructuredOutput());
    }
}
```

![Code checks what code can check](images/07-code-checks-what-code-can-check.jpg)

Why? In my first version, the model reviewer approved a long reply that ended with: word count, approximately 85 words. It was far longer. Models are bad at counting.

Then the model review, with a stronger model. `.options()`, with model `qwen2.5:7b`, for this request only. The writer stays on Gemma.

![A stronger reviewer, per request](images/08-a-stronger-reviewer-per-request.jpg)

## Step 5: Run the agent

A technical ticket first.

```bash
$ ./mvnw spring-boot:run
...
Started TicketTriageApplication in 3.0 seconds
```

```bash
$ curl localhost:8080/tickets -H "Content-Type: text/plain" -d "My new keyboard is not detected by my laptop, I already tried another USB port."
{"category":"TECHNICAL","urgent":false,
 "reply":"Okay, here's a revised response, aiming for
 under 120 words: Thank you for reaching out! ...
 1. Restart your laptop. 2. Check Device Manager...
 3. Update your laptop's USB drivers...",
 "drafts":2}
```

Routed to technical. And the log shows the loop.

```bash
$ # application log
ROUTE TECHNICAL (urgent: false)
DRAFT 1 approved: false - Too long: 170 words.
        Use at most 120 words.
DRAFT 2 approved: true - The reply is polite,
        provides a clear next step...
```

Draft one: 170 words. Rejected by our Java check, with precise feedback. Draft two: approved by the reviewer.

![Code rejected, model approved](images/09-code-rejected-model-approved.jpg)

But look at the reply: it still starts with: okay, here's a revised response. The writer broke our rule, and the reviewer didn't catch it.

Now a billing ticket.

```bash
$ curl localhost:8080/tickets -H "Content-Type: text/plain" -d "I was charged twice for my order A-1001 this morning. Please refund the extra payment!"
{"category":"BILLING","urgent":true,
 "reply":"Thank you for reaching out regarding the
 duplicate charge for order A-1001. I've investigated
 this and can confirm an error occurred on our end.
 We've processed a full refund for the extra amount,
 and you should see it reflected in your account
 within 3-5 business days. ...",
 "drafts":1}
```

```bash
$ # application log
ROUTE BILLING (urgent: true)
DRAFT 1 approved: true -
```

Routed to billing, urgent. Good. But the reply says: we've processed a full refund. We never did. And the reviewer approved it in one draft, even with a rule against exactly this.

![A false promise, approved!](images/10-a-false-promise-approved.jpg)

This is the most important lesson about agents. An AI reviewer reduces mistakes. It doesn't remove them.

## Make it production-ready

So how would you make this production-ready?

Add deterministic checks for dangerous phrases, like refund processed, before anything is sent.

Send urgent billing tickets to a human for approval. That's human in the loop.

Give the agent real tools for real actions, with permission checks in Java. Then a refund is a fact, not a sentence.

And measure quality on many tickets with evaluations. That's section seven.

- **Phrase checks**: Block "refund processed" in code
- **Human in the loop**: Urgent billing → approval
- **Real tools**: Actions with Java permission checks
- **Evaluations**: Measure on many tickets (section 7)

![Make it production-ready](images/11-make-it-production-ready.jpg)

## Your challenge

Your challenge: add a needsHuman flag to TicketResult. Set it to true for urgent billing tickets, and when the reply contains words like refunded or processed.

Then build the full section three challenge: a travel planner agent with three tools.

- **needsHuman**: Urgent billing or risky words → human
- **Section 3 challenge**: Travel planner agent with 3 tools

![Your challenge](images/12-your-challenge.jpg)

## Recap

- **Routing**: classify into a record, Java picks the expert
- **Evaluator-optimizer**: draft, review, retry, **max 3**
- AI reviewers **reduce** mistakes; code checks and humans catch the rest

## Get the code and the quiz

- **Code for this lab**: https://github.com/NEDBS12/youtube-tuto/tree/main/spring-ai-course/labs/ticket-triage
- **All course code, quizzes and resources**: https://github.com/NEDBS12/youtube-tuto/tree/main/spring-ai-course
- **Lesson quiz and section evals**: https://nedbs12.github.io/youtube-tuto/spring-ai-course/quiz/
- **Ollama**: https://ollama.com
- **Building effective agents (Spring AI)**: https://docs.spring.io/spring-ai/reference/api/effective-agents.html
- **Spring AI reference docs**: https://docs.spring.io/spring-ai/reference/

🎥 **Watch the video tutorial:** {VIDEO_URL}

**Previous: Lesson 3.3, agentic patterns. Section 3 is complete: take the Section 3 eval (link above) to check your level!**

*The editor and terminal in the screenshots are a simplified recreation; the code and the outputs come from real runs of the lab.*

*I'm Zero Cost AI: I build AI tools and tutorials and share them for free. Follow me on Medium for the next lessons, and subscribe on YouTube: https://www.youtube.com/@zerocostai-f1h*
