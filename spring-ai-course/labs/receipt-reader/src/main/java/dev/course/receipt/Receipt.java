package dev.course.receipt;

import java.util.List;

public record Receipt(String shop, String date, List<Item> items, double tax, double total, String currency) {

    public record Item(String name, int quantity, double lineTotal) {
    }

    /** A vision model can misread a digit: check that the lines plus tax add up to the total. */
    public boolean addsUp() {
        double sum = items.stream().mapToDouble(Item::lineTotal).sum() + tax;
        return Math.abs(sum - total) < 0.01;
    }

}
