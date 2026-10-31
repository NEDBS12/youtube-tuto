package agent;

// The router's answer: which specialist, and why
public record Route(Specialist specialist, String reason) {

    public enum Specialist { SECURITY, CONCURRENCY, TESTS, GENERAL }
}
