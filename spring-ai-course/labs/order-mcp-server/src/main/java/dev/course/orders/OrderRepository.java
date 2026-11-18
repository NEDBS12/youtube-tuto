package dev.course.orders;

import java.time.LocalDate;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;

import org.springframework.stereotype.Repository;

@Repository
public class OrderRepository {

    // In a real app, this is your database
    private final Map<String, Order> orders = new ConcurrentHashMap<>(Map.of(
            "A-1001", new Order("A-1001", "Wireless headphones", "SHIPPED", LocalDate.of(2026, 11, 20)),
            "A-1002", new Order("A-1002", "4K monitor", "PROCESSING", LocalDate.of(2026, 11, 27)),
            "A-1003", new Order("A-1003", "Mechanical keyboard", "DELIVERED", LocalDate.of(2026, 11, 12))));

    public Optional<Order> find(String id) {
        return Optional.ofNullable(orders.get(id));
    }

    public void save(Order order) {
        orders.put(order.id(), order);
    }
}
