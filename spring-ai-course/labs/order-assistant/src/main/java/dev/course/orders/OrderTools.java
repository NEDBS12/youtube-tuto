package dev.course.orders;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.annotation.ToolParam;
import org.springframework.stereotype.Component;

@Component
public class OrderTools {

    private static final Logger log = LoggerFactory.getLogger(OrderTools.class);

    private final Map<String, Order> orders = Map.of(
            "A-1001", new Order("A-1001", "Mechanical keyboard", "SHIPPED", LocalDate.of(2026, 11, 20)),
            "A-1002", new Order("A-1002", "4K monitor", "PROCESSING", LocalDate.of(2026, 11, 27)));

    @Tool(description = "Find an order by its id, for example A-1001")
    public Order findOrder(@ToolParam(description = "The order id") String orderId) {
        log.info("TOOL findOrder({})", orderId);
        return orders.get(orderId);
    }

    @Tool(description = "Count the days from today until a date given in ISO format, for example 2026-11-20")
    public long daysUntil(@ToolParam(description = "The date, in ISO format") String date) {
        long days = ChronoUnit.DAYS.between(LocalDate.now(), LocalDate.parse(date));
        log.info("TOOL daysUntil({}) = {}", date, days);
        return days;
    }
}
