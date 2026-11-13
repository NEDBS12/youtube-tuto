import json, pathlib

root = pathlib.Path(__file__).parent

def show(el, at=None):
    a = {"k": "show", "el": el}
    if at is not None:
        a["at"] = at
    return a

IQ = lambda s: s.replace("IQ", "I Q")  # say "I Q", not "ick"

def L(say, do=None, hold=None, tts=None):
    line = {"say": say}
    if tts or "IQ" in say:
        line["tts"] = tts or IQ(say)
    if do:
        line["do"] = do
    if hold:
        line["hold"] = hold
    return line

S = {
    "title": "iq-test-promo",
    "voice": "en-US-AvaMultilingualNeural",
    "rate": "+0%",
    "steps": ["Open", "Answer", "Review"],
    "scenes": [
        {
            "type": "title", "chapter": "Introduction",
            "kicker": "Free desktop app · Windows",
            "title": "How Sharp Is\n[[Your Mind?]]",
            "subtitle": "Meet Adult IQ Test: 32 questions, 25 minutes, instant results",
            "lines": [
                L("Have you ever wondered how sharp your mind really is?"),
                L("Meet Adult IQ Test, a free app that challenges your reasoning in just twenty-five minutes."),
                L("And the moment you finish, it shows you exactly where you stand.", hold=0.7),
            ],
        },
        {
            "type": "cards", "chapter": "What it tests", "rail": False,
            "kicker": "**01** · What it tests",
            "heading": "Four ways of [[thinking]]",
            "cards": [
                {"title": "Numerical", "text": "Number sequences and quick math traps"},
                {"title": "Verbal", "text": "Analogies, vocabulary and odd-one-out"},
                {"title": "Logical", "text": "Deduction and lateral thinking"},
                {"title": "Pattern & Spatial", "text": "Letter patterns, cubes and mirrors"},
            ],
            "lines": [
                L("The test has thirty-two questions, covering four ways of thinking.", [show("heading")]),
                L("Numerical reasoning, with sequences and sneaky math traps.", [show("card1")]),
                L("Verbal reasoning, with analogies and vocabulary.", [show("card2")]),
                L("Logical reasoning, where you follow the clues to the only possible answer.", [show("card3")]),
                L("And pattern and spatial reasoning, where you turn shapes around in your head.", [show("card4")], hold=0.6),
            ],
        },
        {
            "type": "compare", "chapter": "Try one now",
            "kicker": "**02** · Try one now",
            "heading": "Can you [[solve this?]]",
            "left": {"title": "The question", "body": "A bat and a ball cost **$1.10** in total.\nThe bat costs **$1.00 more** than the ball.\n\nHow much does the ball cost?"},
            "right": {"title": "The answer", "body": "**5 cents**, not 10.\n\nBall = x, bat = x + $1.00\n2x + $1.00 = $1.10\nx = **$0.05**"},
            "lines": [
                L("Let's warm up with a real question from the test.", [show("heading")]),
                L("A bat and a ball cost one dollar ten in total. The bat costs one dollar more than the ball. How much does the ball cost?", [show("left")]),
                L("Pause the video if you want to think about it.", hold=2.5),
                L("Most people say ten cents. But then the bat would cost one dollar ten, and the total would be one dollar twenty.", [show("arrow")]),
                L("The right answer is five cents. That's the kind of trap the test is full of.", [show("right")], hold=0.7),
            ],
        },
        {
            "type": "shot", "chapter": "Take the test",
            "kicker": "**03** · Take the test",
            "heading": "A clean, [[calm]] start",
            "img": "shots/01-intro.png", "w": 2160, "h": 1215, "label": "Adult IQ Test",
            "points": ["**32 questions** in **25 minutes**", "Harder questions are **worth more**", "Add your name, then press **Start**"],
            "lines": [
                L("When you open the app, you're welcomed by a clean, calm start screen.", [show("heading"), show("frame")]),
                L("You'll get thirty-two questions and twenty-five minutes.", [show("item1")]),
                L("Harder questions are worth more points, so every answer counts.", [show("item2")]),
                L("Just type your name, press start, and the clock begins.", [show("item3")], hold=0.5),
            ],
        },
        {
            "type": "shot",
            "kicker": "**03** · Take the test",
            "heading": "One question at a [[time]]",
            "img": "shots/03-logical.png", "w": 2160, "h": 1215, "label": "Question 20 of 32",
            "marks": [
                {"x": 89, "y": 1, "w": 9, "h": 7, "label": "Live timer", "below": True},
                {"x": 70.5, "y": 21.5, "w": 7.5, "h": 4, "label": "Difficulty", "below": True},
                {"x": 21, "y": 73, "w": 58.5, "h": 25, "label": "Jump to any question"},
            ],
            "lines": [
                L("Each question has its own card, so you can focus on one thing at a time.", [show("heading"), show("frame")]),
                L("The timer stays in the corner, and turns red in the final minute.", [show("mark1")]),
                L("These little bars tell you how hard the question is.", [show("mark2")]),
                L("And if you get stuck, use this map to skip ahead, then come back whenever you like.", [show("mark3")], hold=0.5),
            ],
        },
        {
            "type": "shot",
            "kicker": "**03** · Take the test",
            "heading": "From numbers to [[3D thinking]]",
            "img": "shots/04-spatial.png", "w": 2160, "h": 1215, "label": "Question 27 of 32", "zoom": 0.06,
            "lines": [
                L("The questions get more interesting as you go, all the way to spatial puzzles like this painted cube.", [show("heading"), show("frame")]),
                L("Take your time on these. They're the ones that turn a good score into a great one.", hold=0.6),
            ],
        },
        {
            "type": "shot", "chapter": "Your results",
            "kicker": "**04** · Your results",
            "heading": "Your [[estimated IQ]]",
            "img": "shots/05-result.png", "w": 2160, "h": 1215, "label": "Results",
            "points": ["Score on a **55 to 145** scale", "Your **percentile**", "Classification and **time taken**"],
            "lines": [
                L("Now for the exciting part. Your results appear instantly.", [show("heading"), show("frame")]),
                L("Your estimated IQ is shown on a gauge, from fifty-five to one hundred forty-five.", [show("item1")]),
                L("You also see your percentile, so you know how you compare with everyone else.", [show("item2")]),
                L("Plus your classification, how many you got right, and how long you took.", [show("item3")], hold=0.5),
            ],
        },
        {
            "type": "shot",
            "kicker": "**04** · Your results",
            "heading": "Your strengths at a [[glance]]",
            "img": "shots/06-skills.png", "w": 2160, "h": 1215, "label": "Score by skill area",
            "marks": [{"x": 22, "y": 60, "w": 56, "h": 15.5, "label": "One bar per skill area"}],
            "lines": [
                L("Scroll down, and your score is broken down by skill area.", [show("heading"), show("frame")]),
                L("So you can see exactly where you shine, and where there's room to grow.", [show("mark1")], hold=0.5),
            ],
        },
        {
            "type": "shot",
            "kicker": "**04** · Your results",
            "heading": "Learn from every [[mistake]]",
            "img": "shots/07-review.png", "w": 2160, "h": 1215, "label": "Answer review",
            "marks": [{"x": 20.5, "y": 11, "w": 59, "h": 23.5, "label": "Your answer, the right one, and why", "below": True}],
            "lines": [
                L("And here's what makes this app special: the answer review.", [show("heading"), show("frame")]),
                L("For every question, you see your answer, the correct one, and a short explanation.", [show("mark1")]),
                L("So it's not just a score. It's practice that makes you sharper every time.", hold=0.6),
            ],
        },
        {
            "type": "rows", "chapter": "Get started",
            "kicker": "**05** · Get started",
            "heading": "Ready in [[seconds]]",
            "rows": [
                {"label": "Unzip", "text": "Extract the **IQTest** folder anywhere on your PC"},
                {"label": "Open", "text": "Double-click **IQTest.exe**"},
                {"label": "Play", "text": "The test opens in your **browser**, ready to start"},
            ],
            "banner": "Windows · Free · No installation · No Java needed",
            "lines": [
                L("Getting started takes just a few seconds.", [show("heading")]),
                L("Unzip the IQTest folder anywhere on your computer.", [show("row1")], tts="Unzip the I Q Test folder anywhere on your computer."),
                L("Double-click IQTest.exe.", [show("row2")], tts="Double-click I Q Test dot E X E."),
                L("A small window opens, and the test appears right in your browser.", [show("row3")]),
                L("There's nothing to install, and you don't need Java. It just works.", [show("banner")], hold=0.6),
            ],
        },
        {
            "type": "cards", "chapter": "Tips for your best score", "rail": False,
            "kicker": "**06** · Tips",
            "heading": "Tips for your [[best score]]",
            "cards": [
                {"title": "Find a quiet spot", "text": "Give yourself 25 uninterrupted minutes"},
                {"title": "Don't rush", "text": "Hard questions are worth 3× the points"},
                {"title": "Skip and return", "text": "Use the question map when you're stuck"},
                {"title": "Read the review", "text": "The explanations are how you improve"},
            ],
            "lines": [
                L("Before you begin, here are four quick tips.", [show("heading")]),
                L("Find a quiet spot, and give yourself twenty-five minutes without interruptions.", [show("card1")]),
                L("Don't rush. The hardest questions are worth three times as much.", [show("card2")]),
                L("If a question stops you, skip it, and come back with the question map.", [show("card3")]),
                L("And afterwards, read the explanations. That's where the real progress happens.", [show("card4")], hold=0.6),
            ],
        },
        {
            "type": "checks", "chapter": "Why you'll love it",
            "heading": "Why you'll [[love it]]",
            "items": ["**32 questions** across 4 reasoning areas", "Instant **IQ estimate**, percentile and breakdown", "An **answer review** that helps you improve"],
            "lines": [
                L("So, why will you love it?", [show("heading")]),
                L("Thirty-two carefully chosen questions, across four reasoning areas.", [show("item1")]),
                L("An instant IQ estimate, with your percentile and a full breakdown.", [show("item2")]),
                L("And an answer review that helps you get better every time.", [show("item3")]),
                L("Just remember, it's a fun estimate for self-assessment, not a clinical IQ test.", hold=0.6),
            ],
        },
        {
            "type": "outro",
            "title": "Challenge Your Mind",
            "subtitle": "Take the test and share your score in the comments",
            "cta": "Subscribe to Zero Cost AI for more free apps",
            "lines": [
                L("Now it's your turn. Take the test, and tell me your score in the comments.", [show("line1")]),
                L("And subscribe to Zero Cost AI for more free apps like this one. See you next time!", [show("line2", at=1.0)], hold=1.5),
            ],
        },
    ],
}

(root / "script.json").write_text(json.dumps(S, indent=1, ensure_ascii=False), encoding="utf-8")
print("wrote script.json")
