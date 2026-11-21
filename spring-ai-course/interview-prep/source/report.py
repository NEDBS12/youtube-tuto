"""PDF output: the candidate's score report, and the full Q&A study guide."""
import random
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

from questions import ADVICE, Q, TOPICS, level

GREEN = colors.HexColor("#6DB33F")      # Spring green
DARK = colors.HexColor("#1F2937")
MUTED = colors.HexColor("#6B7280")
RED = colors.HexColor("#DC2626")
AMBER = colors.HexColor("#D97706")
LIGHT = colors.HexColor("#F3F4F6")
TOPIC_NAME = dict(TOPICS)

ss = getSampleStyleSheet()
H1 = ParagraphStyle("h1", parent=ss["Title"], textColor=DARK, fontSize=22, spaceAfter=6)
H2 = ParagraphStyle("h2", parent=ss["Heading2"], textColor=GREEN, spaceBefore=10, spaceAfter=4)
BODY = ParagraphStyle("body", parent=ss["BodyText"], fontSize=9.5, leading=13, textColor=DARK)
SMALL = ParagraphStyle("small", parent=BODY, fontSize=8.5, leading=11, textColor=MUTED)
QSTYLE = ParagraphStyle("q", parent=BODY, fontName="Helvetica-Bold", fontSize=10.5, leading=14, spaceBefore=6)
CENTER = ParagraphStyle("c", parent=BODY, alignment=TA_CENTER)


def shuffled(i, rng=None):
    """Options of question i in display order, and the index of the correct one."""
    q = Q[i]
    order = list(range(len(q["o"])))
    (rng or random.Random(i * 7919)).shuffle(order)
    return [q["o"][k] for k in order], order.index(0)


def p(text, style=BODY):
    return Paragraph(escape(text), style)


def _footer(title):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(MUTED)
        canvas.drawString(18 * mm, 10 * mm, title)
        canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, f"Page {doc.page}")
        canvas.restoreState()
    return draw


def _doc(path, title):
    return SimpleDocTemplate(path, pagesize=A4, title=title, author="Spring AI Interview Prep",
                             leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm, bottomMargin=18 * mm)


def topic_stats(answers):
    """answers: list of (question_index, chosen_original_option_index). Returns {topic: (right, total)}."""
    stats = {}
    for qi, chosen in answers:
        t = Q[qi]["t"]
        r, n = stats.get(t, (0, 0))
        stats[t] = (r + (chosen == 0), n + 1)
    return stats


def strengths(stats):
    ordered = [k for k, _ in TOPICS if k in stats]
    strong = [t for t in ordered if stats[t][0] / stats[t][1] >= 0.75]
    weak = [t for t in ordered if stats[t][0] / stats[t][1] < 0.5]
    mid = [t for t in ordered if t not in strong and t not in weak]
    return strong, mid, weak


def _bar(pct, width=60 * mm):
    color = GREEN if pct >= 75 else (AMBER if pct >= 50 else RED)
    filled = max(pct / 100 * width, 0.5)
    t = Table([["", ""]], colWidths=[filled, max(width - filled, 0.5)], rowHeights=[3.5 * mm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, 0), color), ("BACKGROUND", (1, 0), (1, 0), LIGHT),
                           ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0)]))
    return t


def write_report(path, name, answers, started, finished):
    """Candidate report: score, level, per-topic breakdown, strong and weak points, answer review."""
    right = sum(1 for _, c in answers if c == 0)
    total = len(answers)
    pct = round(100 * right / total) if total else 0
    stats = topic_stats(answers)
    strong, mid, weak = strengths(stats)
    mins, secs = divmod(int((finished - started).total_seconds()), 60)

    s = [p("Spring AI Senior Interview - Score Report", H1),
         p(f"Candidate: {name or 'Anonymous'}    Date: {finished:%Y-%m-%d %H:%M}    Time: {mins} min {secs} s", SMALL),
         Spacer(1, 6)]

    score = Table([[Paragraph(f"<font size=26 color='#6DB33F'><b>{pct}%</b></font>", CENTER),
                    Paragraph(f"<font size=14><b>{right} / {total}</b></font><br/>correct answers", CENTER),
                    Paragraph(f"<font size=14><b>{level(pct)}</b></font><br/>level", CENTER)]],
                  colWidths=[58 * mm] * 3, rowHeights=[22 * mm])
    score.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.6, GREEN), ("INNERGRID", (0, 0), (-1, -1), 0.3, LIGHT),
                               ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("BACKGROUND", (0, 0), (-1, -1), colors.white)]))
    s += [score, Spacer(1, 4),
          p("Levels: 0-49% Novice, 50-69% Apprentice, 70-84% Practitioner, 85-100% Expert-ready.", SMALL)]

    s.append(p("Score by topic", H2))
    rows = [[p("Topic", QSTYLE), p("Score", QSTYLE), p("", BODY), p("Result", QSTYLE)]]
    for key, label in TOPICS:
        if key not in stats:
            continue
        r, n = stats[key]
        tp = round(100 * r / n)
        verdict = "Strong" if key in strong else ("Weak" if key in weak else "Average")
        rows.append([p(label), p(f"{r}/{n}  ({tp}%)"), _bar(tp), p(verdict)])
    t = Table(rows, colWidths=[62 * mm, 28 * mm, 64 * mm, 20 * mm])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LINEBELOW", (0, 0), (-1, 0), 0.6, GREEN),
                           ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT])]))
    s.append(t)

    s.append(p("Strong points", H2))
    s.append(p(", ".join(TOPIC_NAME[k] for k in strong) if strong else "No topic reached 75% yet. Keep practising!"))
    if mid:
        s.append(p("Average (50-74%)", H2))
        s.append(p(", ".join(TOPIC_NAME[k] for k in mid)))
    s.append(p("Weak points and what to study", H2))
    if weak:
        for k in weak:
            s.append(Paragraph(f"<b>{escape(TOPIC_NAME[k])}</b>: {escape(ADVICE[k])}", BODY))
            s.append(Spacer(1, 3))
    else:
        s.append(p("No weak topic (below 50%). Great job!"))

    s += [PageBreak(), p("Answer review", H2)]
    for n, (qi, chosen) in enumerate(answers, 1):
        q = Q[qi]
        ok = chosen == 0
        mark = "<font color='#6DB33F'><b>CORRECT</b></font>" if ok else "<font color='#DC2626'><b>WRONG</b></font>"
        block = [Paragraph(f"{n}. {escape(q['q'])}  {mark}", QSTYLE),
                 p(f"Topic: {TOPIC_NAME[q['t']]}", SMALL)]
        if chosen is None:
            block.append(Paragraph("<b>Your answer:</b> (skipped)", BODY))
        elif not ok:
            block.append(Paragraph(f"<b>Your answer:</b> {escape(q['o'][chosen])}", BODY))
        block += [Paragraph(f"<b>Correct answer:</b> {escape(q['o'][0])}", BODY),
                  Paragraph(f"<b>Explanation:</b> {escape(q['e'])}", BODY)]
        s.append(KeepTogether(block))

    _doc(path, "Spring AI Interview Score Report").build(
        s, onFirstPage=_footer("Spring AI Senior Interview - Score Report"),
        onLaterPages=_footer("Spring AI Senior Interview - Score Report"))


def write_guide(path):
    """Full study guide: every question with options, the answer and the explanation."""
    title = "Spring AI Senior Interview Questions and Answers"
    s = [Spacer(1, 40 * mm), p(title, H1),
         p(f"{len(Q)} questions in {len(TOPICS)} topics, with answers and detailed explanations. "
           "Covers Spring AI 2.0.x on Spring Boot 4 and Java 21.", CENTER),
         Spacer(1, 10 * mm), p("Topics", H2)]
    for n, (key, label) in enumerate(TOPICS, 1):
        count = sum(1 for q in Q if q["t"] == key)
        s.append(p(f"{n}. {label} ({count} questions)"))
    s += [Spacer(1, 6 * mm),
          p("How to use it: answer each question on your own, then read the answer and the explanation. "
            "The explanation is what an interviewer expects a senior engineer to say. To test yourself and "
            "get a score report, run SpringAI-Interview.exe.", BODY),
          PageBreak()]

    n = 0
    for tn, (key, label) in enumerate(TOPICS, 1):
        s.append(p(f"{tn}. {label}", H2))
        for i, q in enumerate(Q):
            if q["t"] != key:
                continue
            n += 1
            opts, ans = shuffled(i)
            block = [p(f"Q{n}. {q['q']}", QSTYLE)]
            for k, o in enumerate(opts):
                block.append(p(f"   {'ABCD'[k]}. {o}"))
            block += [Spacer(1, 2),
                      Paragraph(f"<font color='#6DB33F'><b>Answer: {'ABCD'[ans]}.</b></font> {escape(opts[ans])}", BODY),
                      Paragraph(f"<b>Explanation:</b> {escape(q['e'])}", BODY), Spacer(1, 4)]
            s.append(KeepTogether(block))

    s += [PageBreak(), p("Answer key", H2)]
    key_rows, row = [], []
    n = 0
    for key, _ in TOPICS:
        for i, q in enumerate(Q):
            if q["t"] == key:
                n += 1
                row.append(f"Q{n}: {'ABCD'[shuffled(i)[1]]}")
                if len(row) == 8:
                    key_rows.append(row)
                    row = []
    if row:
        key_rows.append(row + [""] * (8 - len(row)))
    t = Table(key_rows)
    t.setStyle(TableStyle([("FONTSIZE", (0, 0), (-1, -1), 9), ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, LIGHT])]))
    s.append(t)
    _doc(path, title).build(s, onFirstPage=lambda c, d: None, onLaterPages=_footer(title))
