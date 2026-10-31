import org.junit.jupiter.api.Test;

// Sample code to review (it has bugs on purpose)
class PriceCalculatorTest {

    @Test
    void totalCents() {
        long total = PriceCalculator.totalCents(250, 4);
        System.out.println(total);
    }

    @Test
    void negativeQuantity() {
        PriceCalculator.totalCents(250, -1);
    }
}
