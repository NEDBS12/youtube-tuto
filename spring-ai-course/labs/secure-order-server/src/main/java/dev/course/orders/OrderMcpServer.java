package dev.course.orders;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.ai.mcp.annotation.McpArg;
import org.springframework.ai.mcp.annotation.McpPrompt;
import org.springframework.ai.mcp.annotation.McpResource;
import org.springframework.ai.mcp.annotation.McpTool;
import org.springframework.ai.mcp.annotation.McpToolParam;
import org.springframework.stereotype.Component;

import io.modelcontextprotocol.spec.McpSchema.PromptMessage;
import io.modelcontextprotocol.spec.McpSchema.Role;
import io.modelcontextprotocol.spec.McpSchema.TextContent;

@Component
public class OrderMcpServer {

    private static final Logger log = LoggerFactory.getLogger(OrderMcpServer.class);

    private final OrderRepository repository;

    public OrderMcpServer(OrderRepository repository) {
        this.repository = repository;
    }

    // TOOL: an action the model can call
    @McpTool(name = "find_order", description = "Find an order by its id. Returns null if it doesn't exist.",
            annotations = @McpTool.McpAnnotations(readOnlyHint = true, destructiveHint = false))
    public Order findOrder(@McpToolParam(description = "The order id, like A-1001") String id) {
        log.info("TOOL find_order({})", id);
        return repository.find(id).orElse(null);
    }

    @McpTool(name = "cancel_order", description = "Cancel an order. Only orders in PROCESSING can be cancelled.")
    public String cancelOrder(@McpToolParam(description = "The order id") String id) {
        log.info("TOOL cancel_order({})", id);
        Order order = repository.find(id).orElse(null);
        if (order == null) {
            return "No order " + id;
        }
        if (!order.status().equals("PROCESSING")) {   // the rule is checked in Java, not by the model
            return "Order " + id + " is " + order.status() + " and can't be cancelled";
        }
        repository.save(new Order(id, order.product(), "CANCELLED", order.deliveryDate()));
        return "Order " + id + " is cancelled";
    }

    // RESOURCE: data the client application can read
    @McpResource(uri = "orders://policies/returns", name = "return-policy",
            description = "The shop's return policy", mimeType = "text/markdown")
    public String returnPolicy() {
        return """
                # Return policy
                - Return any item within 30 days for a full refund.
                - Opened headphones can't be returned, for hygiene reasons.
                """;
    }

    // PROMPT: a reusable prompt template the user can pick
    @McpPrompt(name = "order-update-email", description = "Write an email to a customer about their order")
    public PromptMessage orderUpdateEmail(@McpArg(name = "orderId", description = "The order id", required = true) String orderId) {
        return new PromptMessage(Role.USER, new TextContent("Use find_order to look up order " + orderId
                + ", then write a short, friendly email to the customer about its status and delivery date."));
    }
}
