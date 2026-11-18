package dev.course.cv;

import java.time.Year;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CvController {

    private final ChatClient chatClient;

    public CvController(ChatClient.Builder builder) {
        this.chatClient = builder
                .defaultSystem("You extract data from CVs. Use only facts written in the CV.")
                .build();
    }

    @PostMapping("/parse")
    public CvResult parse(@RequestBody String cv) {
        Candidate candidate = chatClient.prompt()
                .user(u -> u.text("Extract the candidate from this CV:\n{cv}").param("cv", cv))
                .call()
                .entity(Candidate.class, spec -> spec
                        .useProviderStructuredOutput()
                        .validateSchema());
        return new CvResult(candidate, yearsOfExperience(candidate));
    }

    private int yearsOfExperience(Candidate candidate) {
        int thisYear = Year.now().getValue();
        int first = candidate.jobs().stream().mapToInt(Job::startYear).min().orElse(thisYear);
        return thisYear - first;
    }
}
