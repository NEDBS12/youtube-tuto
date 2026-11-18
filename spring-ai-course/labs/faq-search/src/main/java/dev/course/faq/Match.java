package dev.course.faq;

public record Match(double score, String faq) {

    public Match {
        score = Math.round(score * 100) / 100.0;  // 0.6907... -> 0.69
    }
}
