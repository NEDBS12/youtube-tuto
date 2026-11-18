package dev.course.faq;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class FaqController {

    private final FaqService faqService;

    public FaqController(FaqService faqService) {
        this.faqService = faqService;
    }

    @GetMapping("/search")
    public List<Match> search(@RequestParam String q) {
        return faqService.search(q);
    }

    @GetMapping("/similarity")
    public double similarity(@RequestParam String a, @RequestParam String b) {
        return faqService.similarity(a, b);
    }
}
