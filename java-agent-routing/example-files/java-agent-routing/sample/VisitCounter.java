import java.util.HashMap;
import java.util.Map;

// Sample code to review (it has bugs on purpose)
public class VisitCounter {

    private final Map<String, Integer> visits = new HashMap<>();
    private int total = 0;

    // Called by many web request threads at the same time
    public void record(String page) {
        total++;
        visits.put(page, visits.getOrDefault(page, 0) + 1);
    }

    public int total() {
        return total;
    }
}
