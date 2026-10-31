package agent;

import java.util.List;

// The Reviewer's answer: typed data, not free text
public record Review(String summary, List<Bug> bugs) {

    public record Bug(int line, Severity severity,
                      String problem, String fix) {}

    public enum Severity { LOW, MEDIUM, HIGH }
}
