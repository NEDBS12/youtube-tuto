package dev.course.inventory;

import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.annotation.ToolParam;
import org.springframework.stereotype.Component;

/** The warehouse system. Only this agent can read it. */
@Component
public class StockTools {

    private static final Logger log = LoggerFactory.getLogger(StockTools.class);

    record Stock(String name, int lyon, int berlin, String restockDate) {
    }

    private static final Map<String, Stock> STOCK = Map.of(
            "KB-100", new Stock("MX-100 mechanical keyboard", 0, 0, "2026-12-03"),
            "MS-200", new Stock("Glide wireless mouse", 42, 7, null),
            "HS-300", new Stock("Studio headset", 0, 3, null));

    @Tool(description = "Get the stock of a product in each warehouse, and its restock date if it is sold out")
    public String checkStock(@ToolParam(description = "The product SKU, e.g. KB-100") String sku) {
        log.info("TOOL checkStock({})", sku);
        Stock s = STOCK.get(sku.trim().toUpperCase());
        if (s == null) {
            return "Unknown SKU " + sku;
        }
        return "%s: Lyon %d, Berlin %d units.%s".formatted(s.name(), s.lyon(), s.berlin(),
                s.restockDate() == null ? "" : " Restock expected on " + s.restockDate() + ".");
    }
}
