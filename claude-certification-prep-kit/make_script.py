"""Writes script.json for the unofficial Claude certification prep kit video (3 shared files: guide PDF, mock exam PDF, app .exe)."""
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
  "kicker": "Unofficial · Not provided by Anthropic",
  "title": "Claude Certified Architect\n[[unofficial]] prep kit",
  "subtitle": "Study guide PDF · Mock exams PDF · Practice app (.exe)",
  "lines": [
    L("Are you preparing for the Claude Certified Architect, Foundations exam, and wondering where to start?"),
    L("In this video, I'm sharing three free files to help you prepare: a study guide in PDF, a mock exam workbook in PDF, and a Windows practice app."),
    L("But first, one important note.", hold=0.5)]},
 {"type": "bullets", "chapter": "Important: not official, not by Anthropic",
  "kicker": "**Please read** · Disclaimer",
  "heading": "[[Not official]] · not provided by Anthropic",
  "items": ["**Not provided by Anthropic**, and not reviewed or endorsed by **Anthropic**",
            "**Not official** exam material: these are **original practice questions**, not real exam questions",
            "Exam details can change: always **confirm on the official exam page**"],
  "lines": [
    L("These files are not official, and they are not provided by Anthropic.", [show("heading")]),
    L("They are independent study material. Anthropic did not make them, review them, or endorse them.", [show("item1")]),
    L("The questions are original practice questions, written to match the published exam domains. They are not real exam questions.", [show("item2")]),
    L("And exam details, like the format or the pass mark, can change. So always confirm them on the official exam page before you book.", [show("item3")], hold=0.6)]},
 {"type": "rows", "chapter": "The exam at a glance",
  "kicker": "**01** · The exam",
  "heading": "The exam at a [[glance]]",
  "rows": [{"label": "Format", "text": "60 scenario-based questions · 120 minutes"},
           {"label": "Scenarios", "text": "4 drawn at random from a bank of 6"},
           {"label": "Scoring", "text": "Scaled from 100 to 1,000 · pass mark 720"}],
  "banner": "5 domains: agents · tools & MCP · Claude Code · prompts · context",
  "lines": [
    L("Here's what the exam looks like, based on the published exam guide.", [show("heading")]),
    L("Sixty multiple-choice questions in two hours. That's about two minutes per question.", [show("row1")]),
    L("Every question sits inside a realistic production scenario. You get four scenarios, drawn from a bank of six.", [show("row2")]),
    L("Scores are scaled from 100 to 1,000, and the pass mark is 720.", [show("row3")],
      tts="Scores are scaled from one hundred to one thousand, and the pass mark is seven hundred and twenty."),
    L("The questions cover five domains: agent architecture, tool design and MCP, Claude Code, prompt engineering, and context management.", [show("banner")], hold=0.5)]},
 {"type": "cards", "chapter": "The 3 files",
  "kicker": "**02** · What you get",
  "heading": "[[3 files]] to prepare",
  "cards": [{"title": "Study guide (PDF)", "text": "57 pages: every domain, explained for beginners"},
            {"title": "Mock exams (PDF)", "text": "10 exams · 200 questions · answer keys"},
            {"title": "Practice app (.exe)", "text": "The same 10 exams · practice & timed modes"}],
  "lines": [
    L("You get three files.", [show("heading")]),
    L("A fifty-seven page study guide that teaches every domain.", [show("card1")]),
    L("A printable mock exam workbook: ten exams, two hundred questions, with full answer keys.", [show("card2")]),
    L("And a Windows practice app, with the same ten exams, in practice and timed modes.", [show("card3")], hold=0.5)]},
 {"type": "shot", "chapter": "File 1: The study guide PDF",
  "kicker": "**File 1** · Study guide PDF", "heading": "The [[study guide]]",
  "img": "shots/guide-spread.png", "bare": True, "zoom": 0.03,
  "marks": [{"x": 36.5, "y": 67.5, "w": 26.5, "h": 21, "label": "Domain weights"},
            {"x": 70, "y": 45.5, "w": 26.5, "h": 34.5, "label": "Annotated code"}],
  "lines": [
    L("Let's start with the study guide.", [show("frame")]),
    L("It's written for beginners. Chapter zero explains the exam, and chapter one covers the basics, like what an API call and a tool are."),
    L("Then there's one chapter per domain, so you can see exactly how much each one is worth.", [show("mark1")]),
    L("Each chapter explains the ideas with real code, annotated line by line, like this agent loop.", [show("mark2")], hold=0.3)]},
 {"type": "shot", "kicker": "**File 1** · Study guide PDF", "heading": "Patterns, diagrams and real config",
  "img": "shots/guide-inside.png", "bare": True, "zoom": 0.03,
  "marks": [{"x": 6, "y": 11.5, "w": 39, "h": 24.5, "label": "When to use each pattern"},
            {"x": 6, "y": 46.5, "w": 39, "h": 20.5, "label": "Architecture diagrams"},
            {"x": 55.5, "y": 8.8, "w": 39, "h": 19, "label": "Real settings files", "below": True}],
  "lines": [
    L("Inside, you'll find comparison tables, like the workflow patterns and when to use each one.", [show("frame"), show("mark1", 0.6)]),
    L("Diagrams, like this coordinator and its subagents.", [show("mark2")]),
    L("And real configuration files for Claude Code, such as permission rules and hooks.", [show("mark3")]),
    L("Every chapter ends with a lab exercise and a short quiz. Later chapters solve all six exam scenarios, and finish with a four-week study plan and a glossary.", hold=0.6)]},
 {"type": "shot", "chapter": "File 2: The mock exams PDF",
  "kicker": "**File 2** · Mock exams PDF", "heading": "The [[mock exams]] workbook",
  "img": "shots/workbook-spread.png", "bare": True, "zoom": 0.03,
  "marks": [{"x": 37, "y": 29.5, "w": 26.5, "h": 9, "label": "Questions grouped by scenario"},
            {"x": 70, "y": 9, "w": 26.5, "h": 14.5, "label": "Why each option is wrong", "below": True}],
  "lines": [
    L("The second file is the mock exam workbook: ten exams in a ninety-six page PDF, from Foundation level up to exam level.", [show("frame")]),
    L("Each exam has twenty questions grouped under their scenario, like on the real exam, and an answer sheet you can print.", [show("mark1")]),
    L("After each exam, the answer key explains the correct answer and why every other option is wrong.", [show("mark2")]),
    L("At the end, a score table and a master answer grid help you track all ten attempts.", hold=0.5)]},
 {"type": "shot", "chapter": "File 3: The practice app (.exe)",
  "kicker": "**File 3** · Practice app", "heading": "One click to start",
  "img": "shots/launcher.png", "label": "CCA-F_Mock_Exams.exe", "zoom": 0.02,
  "points": ["Opens the **practice app** in its own window", "Opens the **mock exams PDF**",
             "One file: **no install**, works **offline**"],
  "marks": [{"x": 5.5, "y": 44.5, "w": 89, "h": 13.5},
            {"x": 5.5, "y": 65.5, "w": 89, "h": 14}],
  "lines": [
    L("The third file is the Windows app. It's a single file, so there's nothing to install.", [show("frame")]),
    L("Double-click it, and choose Start the practice app. It opens in its own window.", [show("item1"), show("mark1")]),
    L("You can also open the mock exam workbook from here.", [show("item2"), show("mark2")]),
    L("Everything is bundled inside, so it works offline too.", [show("item3")]),
    L("Windows may warn you the first time, because the file isn't signed. Choose More info, then Run anyway.", hold=0.5)]},
 {"type": "shot", "kicker": "**File 3** · Practice app", "heading": "The [[practice app]]",
  "img": "shots/app-home-crop.png", "label": "CCA-F Mock Exams", "zoom": 0.03,
  "marks": [{"x": 1, "y": 1.5, "w": 98, "h": 17.5, "label": "Exam format", "below": True},
            {"x": 1, "y": 23.5, "w": 98, "h": 34.5, "label": "Domain weights", "below": True},
            {"x": 79.5, "y": 71, "w": 17.5, "h": 22.5, "label": "Two modes"}],
  "lines": [
    L("This is the practice app. It's where you'll spend most of your time.", [show("frame")]),
    L("The home page sums up the exam format.", [show("mark1")]),
    L("And the five domain weights, so you know where to focus.", [show("mark2")]),
    L("Below, you'll find the ten mock exams. Each one has twenty questions across four scenarios."),
    L("Every exam has two modes: Practice, and Timed.", [show("mark3")], hold=0.4)]},
 {"type": "shot", "kicker": "**File 3** · Practice mode", "heading": "Practice mode: learn from every answer",
  "img": "shots/app-explain-crop.png", "label": "Mock Exam 1 · Practice", "zoom": 0.03,
  "marks": [{"x": 1, "y": 21.8, "w": 98, "h": 13.5, "label": "Why this answer is wrong"},
            {"x": 1, "y": 50.3, "w": 98, "h": 9, "label": "The correct answer"},
            {"x": 1, "y": 78.6, "w": 98, "h": 20, "label": "The explanation"}],
  "lines": [
    L("In practice mode, you pick an answer and check it right away.", [show("frame")]),
    L("Here, I chose A on purpose. The app marks it wrong, and tells me why it's wrong.", [show("mark1")]),
    L("It highlights the correct answer.", [show("mark2")]),
    L("And explains the reasoning behind it. Every wrong option has its own note too, because understanding the traps is how you pass a scenario exam.", [show("mark3")], hold=0.5)]},
 {"type": "shot", "chapter": "Timed mode and results",
  "kicker": "**File 3** · Timed mode", "heading": "Timed mode: exam conditions",
  "img": "shots/app-timed-crop.png", "label": "Mock Exam 9 · Timed", "zoom": 0.03,
  "marks": [{"x": 89.5, "y": 1, "w": 9.5, "h": 6.2, "label": "40-minute timer", "below": True},
            {"x": 1, "y": 92.8, "w": 94.5, "h": 6.8, "label": "Navigator: answered and flagged"}],
  "lines": [
    L("Timed mode puts you under exam conditions.", [show("frame")]),
    L("You get two minutes per question, so forty minutes for the whole exam.", [show("mark1")]),
    L("You can flag a question, move on, and come back to it later from the navigator, just as you would on exam day.", [show("mark2")], hold=0.3)]},
 {"type": "shot", "kicker": "**File 3** · Results", "heading": "Results by domain",
  "img": "shots/app-results-crop.png", "label": "Mock Exam 4 · Results", "zoom": 0.03,
  "marks": [{"x": 1, "y": 0.8, "w": 98, "h": 20, "label": "Estimated scaled score", "below": True},
            {"x": 1, "y": 23, "w": 98, "h": 25.5, "label": "Score per domain", "below": True},
            {"x": 1, "y": 58, "w": 98, "h": 41.5, "label": "Review your misses"}],
  "lines": [
    L("When you finish, you get your score and an estimated scaled score. It's a simple estimate, not the official formula.", [show("frame"), show("mark1", 0.6)]),
    L("You also see your score in each domain, so your weak spots are obvious.", [show("mark2")]),
    L("And you can review every question you missed, with your answer, the correct one, and the explanation.", [show("mark3")]),
    L("Your best score for each exam is saved, so you can track your progress.", hold=0.5)]},
 {"type": "rows", "chapter": "Download the 3 files",
  "kicker": "**03** · Download", "heading": "Get the [[3 files]]",
  "rows": [{"label": "Guide", "text": "Claude_Certified_Architect_Foundations_Study_Guide.pdf"},
           {"label": "Mock exams", "text": "CCA-F_Mock_Exams.pdf"},
           {"label": "App", "text": "CCA-F_Mock_Exams.exe (Windows)"}],
  "banner": "Free download · link in the description · unofficial, not by Anthropic",
  "lines": [
    L("Here are the three files.", [show("heading")]),
    L("The study guide PDF.", [show("row1")]),
    L("The mock exams PDF.", [show("row2")]),
    L("And the practice app, for Windows.", [show("row3")]),
    L("They're free. The download link is in the description. And remember, they're unofficial, and not provided by Anthropic.", [show("banner")], hold=0.5)]},
 {"type": "cards", "chapter": "How to study with the files",
  "kicker": "**04** · Study plan", "heading": "How to [[study]] with them",
  "cards": [{"title": "Learn", "text": "Read one domain chapter at a time and do its lab"},
            {"title": "Practise: exams 1–5", "text": "Practice mode. Read every explanation"},
            {"title": "Test: exams 6–10", "text": "Timed mode. No notes, 40 minutes each"},
            {"title": "Review", "text": "Re-read your misses. Aim for 16/20 before booking"}],
  "lines": [
    L("So, how should you use them?", [show("heading")]),
    L("First, learn. Read the study guide one domain at a time, and do the lab at the end of each chapter.", [show("card1")]),
    L("Then practise with exams one to five, in practice mode. Read every explanation, even when you're right.", [show("card2")]),
    L("Next, test yourself with exams six to ten in timed mode. No notes, forty minutes each.", [show("card3")]),
    L("Finally, review your misses. Aim for sixteen out of twenty, or better, before you book the real exam.", [show("card4")], hold=0.5)]},
 {"type": "checks", "chapter": "Recap", "heading": "[[Recap]]",
  "items": ["The **study guide PDF** teaches all five domains, from the basics",
            "**200 original questions** with explanations, in the **PDF** and the **app**",
            "**Not official, not provided by Anthropic**: confirm exam details on the official page"],
  "lines": [
    L("Let's recap.", [show("heading")]),
    L("The study guide teaches all five domains, starting from the basics.", [show("item1")]),
    L("Two hundred original questions, with explanations, in the mock exam PDF and in the practice app.", [show("item2")]),
    L("And remember: these files are not official, and not provided by Anthropic. Always confirm the exam details on the official exam page.", [show("item3")], hold=0.6)]},
 {"type": "outro", "title": "Good luck on your [[exam]]",
  "subtitle": "Unofficial study material · not provided by, affiliated with or endorsed by Anthropic",
  "lines": [
    L("Thanks for watching, and good luck on your exam.", [show("line1")]),
    L("If this helped, like the video and subscribe for more.", [show("line2")], hold=1.0)]},
]

S = {"title": "claude-certification-prep-kit", "voice": "en-US-AndrewNeural", "steps": [], "scenes": scenes}
(HERE / "script.json").write_text(json.dumps(S, indent=1, ensure_ascii=False), encoding="utf-8")
print(sum(len(s["lines"]) for s in scenes), "lines")
