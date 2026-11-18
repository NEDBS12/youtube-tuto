package dev.course.explorer;

public record ChatDetails(String answer, String model,
                          Integer promptTokens, Integer completionTokens, Integer totalTokens) {
}
