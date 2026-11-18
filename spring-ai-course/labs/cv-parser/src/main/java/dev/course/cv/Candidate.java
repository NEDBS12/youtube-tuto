package dev.course.cv;

import java.util.List;

public record Candidate(String name, String email, List<String> skills, List<Job> jobs) {
}
