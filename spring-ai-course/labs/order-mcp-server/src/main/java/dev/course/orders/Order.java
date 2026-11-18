package dev.course.orders;

import java.time.LocalDate;

public record Order(String id, String product, String status, LocalDate deliveryDate) {
}
