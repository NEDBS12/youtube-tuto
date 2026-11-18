package dev.course.docs;

import java.util.List;
import java.util.regex.Pattern;

import org.springframework.stereotype.Component;

/** Finds text that talks to the AI instead of informing people: a sign of prompt injection. */
@Component
public class InjectionScanner {

    private static final List<Pattern> PATTERNS = List.of(
            Pattern.compile("ignore (all |any |your |the )?(previous |prior |above )?instructions", Pattern.CASE_INSENSITIVE),
            Pattern.compile("note to the (ai|assistant|model)", Pattern.CASE_INSENSITIVE),
            Pattern.compile("you are now", Pattern.CASE_INSENSITIVE),
            Pattern.compile("system prompt", Pattern.CASE_INSENSITIVE));

    public boolean isSuspicious(String text) {
        return PATTERNS.stream().anyMatch(p -> p.matcher(text).find());
    }
}
