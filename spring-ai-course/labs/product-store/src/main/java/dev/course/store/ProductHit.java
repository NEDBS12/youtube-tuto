package dev.course.store;

public record ProductHit(String product, Object category, Object price, double score) {

    public ProductHit {
        score = Math.round(score * 100) / 100.0;
    }
}
