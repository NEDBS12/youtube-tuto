package dev.course.toolloop;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;

import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.annotation.ToolParam;
import org.springframework.stereotype.Component;

@Component
public class ShopTools {

    @Tool(description = "Find an order by its id and return its status and delivery date")
    public String findOrder(@ToolParam(description = "The order id, e.g. A-1001") String orderId) {
        return "A-1001".equals(orderId) ? "SHIPPED, delivery 2026-11-20" : "Order not found";
    }

    @Tool(description = "Count the days from today until a date in ISO format")
    public long daysUntil(@ToolParam(description = "ISO date, e.g. 2026-11-20") String date) {
        return ChronoUnit.DAYS.between(LocalDate.now(), LocalDate.parse(date));
    }

    @Tool(description = "Get the store opening hours")
    public String getStoreHours() {
        return "Monday to Saturday, 9:00 to 19:00";
    }

    @Tool(description = "Get the return policy")
    public String getReturnPolicy() {
        return "Returns accepted within 30 days, in the original packaging";
    }

    @Tool(description = "Get the shipping cost to a country")
    public String getShippingCost(@ToolParam(description = "Country name") String country) {
        return "France".equalsIgnoreCase(country) ? "4.90 EUR" : "14.90 EUR";
    }

    @Tool(description = "Check if a product is in stock")
    public String checkStock(@ToolParam(description = "Product name") String product) {
        return product + ": 12 units in stock";
    }

    @Tool(description = "Get the warranty period of a product")
    public String getWarranty(@ToolParam(description = "Product name") String product) {
        return product + ": 2 years warranty";
    }

    @Tool(description = "List the product categories of the shop")
    public String listCategories() {
        return "Keyboards, Monitors, Laptops, Audio";
    }

    @Tool(description = "Get the loyalty points of a customer")
    public int getLoyaltyPoints(@ToolParam(description = "Customer id") String customerId) {
        return 1250;
    }

    @Tool(description = "List the active promo codes")
    public String getPromoCodes() {
        return "WINTER10: 10% off monitors";
    }
}
