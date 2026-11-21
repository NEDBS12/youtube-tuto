"""Writes script.json for the Spring AI senior interview prep kit video (app .exe, Q&A PDF, score report PDF)."""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent


def L(say, do=None, tts=None, hold=None):
    d = {"say": say}
    if tts:
        d["tts"] = tts
    if do:
        d["do"] = do
    if hold:
        d["hold"] = hold
    return d


def show(el, at=None):
    return {"k": "show", "el": el} if at is None else {"k": "show", "el": el, "at": at}


scenes = [
 {"type": "title", "chapter": "Introduction",
  "kicker": "Spring AI · Interview prep kit",
  "title": "Spring AI [[senior interview]]\nprep kit",
  "subtitle": "80 questions · Practice app (.exe) · Q&A PDF · Score report",
  "lines": [
    L("Do you have a Spring AI interview coming up, for a senior role?"),
    L("Interviewers won't just ask what ChatClient is. They'll ask how advisors are ordered, how you secure tools, and how you test answers that change every time."),
    L("In this video, I'm sharing a free kit to prepare: eighty senior-level questions, a Windows practice app that scores you, and a PDF with every answer explained.", hold=0.5)]},
 {"type": "cards", "chapter": "What's in the kit",
  "kicker": "**01** · What you get",
  "heading": "The [[kit]]",
  "cards": [{"title": "Practice app (.exe)", "text": "Interview simulator · no install · offline"},
            {"title": "Score report (PDF)", "text": "Score, level, strong and weak points"},
            {"title": "Q&A study guide (PDF)", "text": "80 questions · answers · explanations"}],
  "lines": [
    L("Here's what you get.", [show("heading")]),
    L("A practice app for Windows. It's one file: you double-click it, and that's it.", [show("card1")]),
    L("At the end of each interview, it gives you a report with your score, your level, and your strong and weak points. You can save it as a PDF.", [show("card2")]),
    L("And a study guide PDF with all eighty questions, the answers, and the explanations.", [show("card3")], hold=0.5)]},
 {"type": "rows", "chapter": "The 20 topics covered",
  "kicker": "**02** · Coverage",
  "heading": "20 topics, [[4 questions]] each",
  "rows": [{"label": "Core", "text": "Architecture · ChatClient · prompts · model options · streaming"},
           {"label": "Building blocks", "text": "Structured output · advisors · chat memory · tools · agentic patterns"},
           {"label": "Your data", "text": "Embeddings · vector stores · ETL pipeline · RAG"},
           {"label": "Production", "text": "MCP · multimodality · evaluation · observability · security · performance"}],
  "banner": "Spring AI 2.0 · Spring Boot 4 · Java 21",
  "lines": [
    L("The questions cover the whole of Spring AI, in twenty topics, with four questions each.", [show("heading")]),
    L("The core: the architecture, the ChatClient API, prompts, model options and streaming.", [show("row1")]),
    L("The building blocks: structured output, advisors, chat memory, tool calling and agentic patterns.", [show("row2")]),
    L("Working with your own data: embeddings, vector stores, the ETL pipeline and RAG.", [show("row3")]),
    L("And production topics: MCP, multimodality, evaluation, observability, security and performance.", [show("row4")]),
    L("Everything targets Spring AI 2.0, on Spring Boot 4 and Java 21.", [show("banner")], hold=0.5)]},
 {"type": "shot", "chapter": "The practice app",
  "kicker": "**03** · Practice app", "heading": "Start an [[interview]]",
  "img": "shots/app-home-crop.png", "label": "SpringAI-Interview.exe", "zoom": 0.03,
  "marks": [{"x": 5, "y": 33, "w": 33, "h": 17, "label": "3 modes"},
            {"x": 5, "y": 51.5, "w": 48, "h": 27, "label": "Pick your topics"},
            {"x": 5, "y": 86, "w": 30, "h": 7.5, "label": "Start, or save the PDF"}],
  "lines": [
    L("This is the practice app. Type your name, and choose a mode.", [show("frame")]),
    L("A quick interview is twenty questions, one per topic. It takes about fifteen minutes. Or take all eighty.", [show("mark1")]),
    L("If you want to focus, tick the topics you need, like RAG and MCP, and you'll get every question for those topics.", [show("mark2")]),
    L("Then click Start. You can also save the full study guide as a PDF from here.", [show("mark3")]),
    L("Windows may warn you the first time, because the file isn't signed. Choose More info, then Run anyway.", hold=0.5)]},
 {"type": "shot", "chapter": "Learning mode: every answer explained",
  "kicker": "**03** · Practice app", "heading": "Learn from every [[answer]]",
  "img": "shots/app-explain-crop.png", "label": "Question 1 of 20", "zoom": 0.03,
  "marks": [{"x": 5, "y": 41, "w": 90, "h": 11, "label": "My answer: wrong"},
            {"x": 5, "y": 59.5, "w": 90, "h": 11, "label": "The correct answer"},
            {"x": 5, "y": 81, "w": 66, "h": 16, "label": "Why", "below": True}],
  "lines": [
    L("Each question tells you its topic. This one is about model options: what does a low temperature do?", [show("frame")]),
    L("I chose shorter responses, on purpose. The app marks it in red.", [show("mark1")]),
    L("And shows the correct answer in green: more deterministic, focused output.", [show("mark2")]),
    L("Then it explains why, the way a senior engineer would. Even at temperature zero, many providers aren't fully deterministic, so your tests must not rely on exact text.", [show("mark3")]),
    L("The answers are shuffled every time, so you can't just remember positions. You can also use the keys one to four, and Enter.", hold=0.5)]},
 {"type": "shot", "chapter": "Your score and level",
  "kicker": "**04** · Your report", "heading": "Score, level and [[topics]]",
  "img": "shots/app-report.png", "label": "Your interview report", "zoom": 0.03,
  "marks": [{"x": 4.5, "y": 11, "w": 47, "h": 12, "label": "Score and level", "below": True},
            {"x": 5, "y": 35, "w": 46, "h": 59, "label": "Score by topic"},
            {"x": 5.3, "y": 23.5, "w": 11.2, "h": 5.5, "label": "Save as PDF", "below": True}],
  "lines": [
    L("When you finish, you get your report.", [show("frame")]),
    L("Your score, and your level: Novice, Apprentice, Practitioner, or Expert-ready. Here, seventy percent: Practitioner.", [show("mark1")]),
    L("Below, your score in each of the twenty topics, so you see at a glance where you stand.", [show("mark2")]),
    L("And one click saves the whole report as a PDF.", [show("mark3")], hold=0.4)]},
 {"type": "shot", "chapter": "Strong and weak points",
  "kicker": "**04** · Your report", "heading": "Strong and [[weak]] points",
  "img": "shots/app-report2-crop.png", "label": "Your interview report", "zoom": 0.03,
  "marks": [{"x": 5, "y": 0.5, "w": 26, "h": 40, "label": "Strong: 75% and more", "below": True},
            {"x": 5, "y": 42.5, "w": 66, "h": 55, "label": "Weak: what to study"}],
  "lines": [
    L("Then come your strong points: the topics where you scored seventy-five percent or more.", [show("frame"), show("mark1", 0.6)]),
    L("And your weak points, below fifty percent. For each one, the app tells you exactly what to study.", [show("mark2")]),
    L("For MCP, for example: the roles, the primitives, the transports, and the server annotations."),
    L("Further down, you can review every question you missed, with the correct answer and the explanation.", hold=0.5)]},
 {"type": "shot", "chapter": "The PDF score report",
  "kicker": "**05** · PDF report", "heading": "The [[PDF]] score report",
  "img": "shots/report-spread.png", "bare": True, "zoom": 0.03,
  "marks": [{"x": 6, "y": 13.3, "w": 39.4, "h": 7.8, "label": "Score and level", "below": True},
            {"x": 6, "y": 26.6, "w": 39.4, "h": 45, "label": "Topic bars"},
            {"x": 55, "y": 11, "w": 39.8, "h": 13.4, "label": "Answer review", "below": True}],
  "lines": [
    L("Here's the saved PDF report. It's easy to keep, print, or compare over time.", [show("frame")]),
    L("Page one has your score and level.", [show("mark1")]),
    L("A bar for each topic, then your strong and weak points.", [show("mark2")]),
    L("And the answer review lists every question, marked correct or wrong, with your answer, the right one, and the explanation.", [show("mark3")], hold=0.5)]},
 {"type": "shot", "chapter": "The Q&A study guide PDF",
  "kicker": "**06** · Study guide", "heading": "80 questions, [[answered]]",
  "img": "shots/guide-spread.png", "bare": True, "zoom": 0.03,
  "marks": [{"x": 6, "y": 33.5, "w": 18, "h": 46, "label": "20 topics"},
            {"x": 55, "y": 23.3, "w": 39.6, "h": 7.3, "label": "Answer + explanation", "below": True}],
  "lines": [
    L("The last file is the study guide. Twenty-three pages, with all eighty questions.", [show("frame")]),
    L("They're grouped by topic, in the same twenty topics as the app.", [show("mark1")]),
    L("Each question has four options, the answer, and an explanation, with the class names and properties you'd mention in an interview.", [show("mark2")]),
    L("An answer key at the end lets you test yourself on paper.", hold=0.5)]},
 {"type": "cards", "chapter": "How to prepare with the kit",
  "kicker": "**07** · Study plan", "heading": "How to [[prepare]]",
  "cards": [{"title": "Baseline", "text": "Quick interview, learning mode off"},
            {"title": "Study", "text": "Read the weak topics in the PDF"},
            {"title": "Practise", "text": "Pick topics mode on your weak spots"},
            {"title": "Full run", "text": "All 80 questions · aim for 85%"}],
  "lines": [
    L("So, how should you prepare?", [show("heading")]),
    L("First, take a quick interview with learning mode off. That's your honest baseline.", [show("card1")]),
    L("Then read your weak topics in the study guide. Say the explanations out loud, as if you were in the interview.", [show("card2")]),
    L("Next, use Pick topics mode to practise only those weak spots, until they turn green.", [show("card3")]),
    L("Finally, take the full eighty-question interview. Aim for eighty-five percent, the Expert-ready level.", [show("card4")], hold=0.5)]},
 {"type": "rows", "chapter": "Download the kit",
  "kicker": "**08** · Download", "heading": "Get the [[kit]]",
  "rows": [{"label": "App", "text": "SpringAI-Interview.exe (Windows, no install)"},
           {"label": "PDF", "text": "Spring-AI-Interview-Questions-and-Answers.pdf"},
           {"label": "Source", "text": "Python source to run it on macOS or Linux"}],
  "banner": "Free on GitHub · link in the description",
  "lines": [
    L("Everything is free, on GitHub.", [show("heading")]),
    L("The practice app, for Windows.", [show("row1")]),
    L("The questions and answers PDF.", [show("row2")]),
    L("And the Python source, if you're on macOS or Linux, or want to add your own questions.", [show("row3")]),
    L("The link is in the description, next to the free Spring AI course and book.", [show("banner")], hold=0.5)]},
 {"type": "checks", "chapter": "Recap", "heading": "[[Recap]]",
  "items": ["**80 senior questions** in **20 topics**, from ChatClient to MCP and production",
            "The **app** scores you and shows your **strong and weak points**",
            "Study the **explanations**: that's what interviewers want to hear"],
  "lines": [
    L("Let's recap.", [show("heading")]),
    L("Eighty senior-level questions, in twenty topics, from ChatClient to MCP and production.", [show("item1")]),
    L("The app scores you, gives you a level, and shows your strong and weak points, with a PDF report.", [show("item2")]),
    L("And study the explanations, not just the answers. That's what interviewers want to hear.", [show("item3")], hold=0.6)]},
 {"type": "outro", "title": "Good luck in your [[interview]]",
  "subtitle": "Free Spring AI course, book and quizzes on the channel",
  "cta": "Like · Subscribe · Share with a friend who's job hunting",
  "lines": [
    L("Thanks for watching, and good luck in your interview.", [show("line1")]),
    L("If this helped, like the video, subscribe, and share it with a friend who's preparing too.", [show("line2")], hold=1.0)]},
]

S = {"title": "spring-ai-interview-prep-kit", "voice": "en-US-AndrewNeural", "steps": [], "scenes": scenes}
(HERE / "script.json").write_text(json.dumps(S, indent=1, ensure_ascii=False), encoding="utf-8")
print(sum(len(s["lines"]) for s in scenes), "lines")
