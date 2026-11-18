package dev.course.triage;

public record TicketResult(Category category, boolean urgent, String reply, int drafts) {
}
