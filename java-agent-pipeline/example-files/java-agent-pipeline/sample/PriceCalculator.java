// Sample code to review (this one is clean)
public class PriceCalculator {

    public static long totalCents(long unitCents, int quantity) {
        if (quantity < 0) {
            throw new IllegalArgumentException("quantity < 0");
        }
        return Math.multiplyExact(unitCents, quantity);
    }
}
