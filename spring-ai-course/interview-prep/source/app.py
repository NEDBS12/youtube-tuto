"""Spring AI Senior Interview - desktop quiz with a scored report (strong and weak points)."""
import os
import random
import sys
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, ttk

from questions import ADVICE, Q, TOPICS, level
from report import strengths, topic_stats, write_guide, write_report

GREEN, DARK, BG, CARD = "#6DB33F", "#1F2937", "#F4F6F8", "#FFFFFF"
RED, AMBER, MUTED = "#DC2626", "#D97706", "#6B7280"
TOPIC_NAME = dict(TOPICS)
FONT = "Segoe UI"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Spring AI Senior Interview")
        self.geometry("1000x720")
        self.minsize(820, 600)
        self.configure(bg=BG)
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("G.Horizontal.TProgressbar", background=GREEN, troughcolor="#E5E7EB", thickness=8)
        style.configure("TCheckbutton", background=CARD, font=(FONT, 10))
        self.bind("<Return>", lambda e: self._enter())
        for k in "1234":
            self.bind(k, lambda e, k=k: self._pick(int(k) - 1))
        self.enter_action = None
        self.home()

    # ---------- helpers ----------
    def clear(self):
        for w in self.winfo_children():
            w.destroy()
        self.enter_action = None

    def _enter(self):
        if self.enter_action:
            self.enter_action()

    def _pick(self, k):
        if getattr(self, "choice", None) is not None and not self.answered and k < len(self.cur_opts):
            self.choice.set(k)

    def header(self, text, sub=""):
        bar = tk.Frame(self, bg=DARK)
        bar.pack(fill="x")
        tk.Label(bar, text="  Spring AI  ", bg=GREEN, fg="white", font=(FONT, 12, "bold")).pack(side="left", padx=(16, 10), pady=12)
        tk.Label(bar, text=text, bg=DARK, fg="white", font=(FONT, 14, "bold")).pack(side="left")
        if sub:
            tk.Label(bar, text=sub, bg=DARK, fg="#D1D5DB", font=(FONT, 10)).pack(side="right", padx=16)

    def button(self, parent, text, cmd, primary=True):
        b = tk.Button(parent, text=text, command=cmd, font=(FONT, 10, "bold"), relief="flat", cursor="hand2",
                      bg=GREEN if primary else "#E5E7EB", fg="white" if primary else DARK,
                      activebackground="#5A9A32" if primary else "#D1D5DB", padx=16, pady=7, bd=0)
        return b

    def scrollable(self):
        outer = tk.Frame(self, bg=BG)
        outer.pack(fill="both", expand=True)
        canvas = tk.Canvas(outer, bg=BG, highlightthickness=0)
        sb = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=BG)
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        win = canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfigure(win, width=e.width))
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        self.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-e.delta / 120), "units"))
        return inner

    # ---------- home ----------
    def home(self):
        self.clear()
        self.unbind_all("<MouseWheel>")
        self.header("Senior Interview Simulator", f"{len(Q)} questions - {len(TOPICS)} topics")
        card = tk.Frame(self.scrollable(), bg=CARD, padx=30, pady=24)
        card.pack(fill="x", padx=40, pady=24)

        tk.Label(card, text="Test your Spring AI knowledge like in a senior interview", bg=CARD, fg=DARK,
                 font=(FONT, 16, "bold")).pack(anchor="w")
        tk.Label(card, text="Answer, read the explanation, then get a report with your score, level, strong and weak points.",
                 bg=CARD, fg=MUTED, font=(FONT, 10)).pack(anchor="w", pady=(2, 16))

        row = tk.Frame(card, bg=CARD)
        row.pack(anchor="w", fill="x")
        tk.Label(row, text="Your name", bg=CARD, fg=DARK, font=(FONT, 10, "bold")).pack(side="left")
        self.name = tk.Entry(row, font=(FONT, 11), width=30, relief="solid", bd=1)
        self.name.pack(side="left", padx=10)
        self.name.focus_set()

        tk.Label(card, text="Mode", bg=CARD, fg=DARK, font=(FONT, 10, "bold")).pack(anchor="w", pady=(16, 4))
        self.mode = tk.StringVar(value="quick")
        for val, txt in [("quick", f"Quick interview - {len(TOPICS)} questions, one per topic (about {round(len(TOPICS) * 0.75)} min)"),
                         ("full", f"Full interview - all {len(Q)} questions"),
                         ("topics", "Pick topics - all questions of the topics you tick below")]:
            tk.Radiobutton(card, text=txt, variable=self.mode, value=val, bg=CARD, fg=DARK, font=(FONT, 10),
                           activebackground=CARD, selectcolor=CARD, anchor="w").pack(anchor="w")

        self.explain = tk.BooleanVar(value=True)
        ttk.Checkbutton(card, text="Show the answer and explanation after each question (learning mode)",
                        variable=self.explain).pack(anchor="w", pady=(10, 0))

        btns = tk.Frame(card, bg=CARD)
        btns.pack(anchor="w", pady=(14, 0))
        self.button(btns, "Start interview  >", self.start).pack(side="left")
        self.button(btns, "Save Q&A study guide (PDF)", self.save_guide, primary=False).pack(side="left", padx=10)
        tk.Label(card, text="Keyboard: 1-4 to choose, Enter to submit / continue.", bg=CARD, fg=MUTED,
                 font=(FONT, 9)).pack(anchor="w", pady=(8, 0))

        tk.Label(card, text="Topics (for Pick topics)", bg=CARD, fg=DARK, font=(FONT, 10, "bold")).pack(anchor="w", pady=(16, 4))
        grid = tk.Frame(card, bg=CARD)
        grid.pack(anchor="w", fill="x")
        self.topic_vars = {}
        for i, (key, label) in enumerate(TOPICS):
            v = tk.BooleanVar(value=False)
            self.topic_vars[key] = v
            ttk.Checkbutton(grid, text=label, variable=v,
                            command=lambda: self.mode.set("topics")).grid(row=i // 3, column=i % 3, sticky="w", padx=(0, 22), pady=1)
        self.enter_action = self.start

    def save_guide(self):
        path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")],
                                            initialfile="Spring-AI-Interview-Questions-and-Answers.pdf")
        if path:
            write_guide(path)
            self._open(path)

    # ---------- quiz ----------
    def start(self):
        mode = self.mode.get()
        if mode == "quick":
            picked = [random.choice([i for i, q in enumerate(Q) if q["t"] == k]) for k, _ in TOPICS]
        elif mode == "full":
            picked = list(range(len(Q)))
        else:
            keys = {k for k, v in self.topic_vars.items() if v.get()}
            if not keys:
                messagebox.showinfo("Pick topics", "Select at least one topic.")
                return
            picked = [i for i, q in enumerate(Q) if q["t"] in keys]
        random.shuffle(picked)
        self.user = self.name.get().strip()
        self.learn = self.explain.get()
        self.queue = picked
        self.answers = []          # (question index, chosen original option index or None)
        self.started = datetime.now()
        self.pos = 0
        self.show_question()

    def show_question(self):
        self.clear()
        qi = self.queue[self.pos]
        q = Q[qi]
        right = sum(1 for _, c in self.answers if c == 0)
        self.header(f"Question {self.pos + 1} of {len(self.queue)}", f"Score so far: {right}/{len(self.answers)}")
        pb = ttk.Progressbar(self, style="G.Horizontal.TProgressbar", maximum=len(self.queue), value=self.pos)
        pb.pack(fill="x")

        card = tk.Frame(self, bg=CARD, padx=30, pady=22)
        card.pack(fill="both", expand=True, padx=40, pady=20)
        tk.Label(card, text=TOPIC_NAME[q["t"]].upper(), bg=CARD, fg=GREEN, font=(FONT, 9, "bold")).pack(anchor="w")
        tk.Label(card, text=q["q"], bg=CARD, fg=DARK, font=(FONT, 14, "bold"), wraplength=840,
                 justify="left").pack(anchor="w", pady=(4, 14))

        order = list(range(len(q["o"])))
        random.shuffle(order)
        self.cur_order = order
        self.cur_opts = [q["o"][k] for k in order]
        self.choice = tk.IntVar(value=-1)
        self.answered = False
        self.opt_widgets = []
        for k, text in enumerate(self.cur_opts):
            rb = tk.Radiobutton(card, text=f"{k + 1}.  {text}", variable=self.choice, value=k, bg=CARD, fg=DARK,
                                font=(FONT, 11), wraplength=820, justify="left", anchor="w", activebackground=CARD,
                                selectcolor=CARD, padx=6, pady=5)
            rb.pack(anchor="w", fill="x")
            self.opt_widgets.append(rb)

        self.feedback = tk.Frame(card, bg=CARD)
        self.feedback.pack(fill="x", pady=(10, 0))
        bar = tk.Frame(card, bg=CARD)
        bar.pack(side="bottom", fill="x", pady=(10, 0))
        self.button(bar, "Quit and see report", self.finish, primary=False).pack(side="left")
        self.skip_btn = self.button(bar, "Skip", self.skip, primary=False)
        self.skip_btn.pack(side="right", padx=(0, 10))
        self.main_btn = self.button(bar, "Submit answer", self.submit)
        self.main_btn.pack(side="right", padx=(0, 10))
        self.enter_action = self.submit

    def _record(self, chosen_display):
        orig = None if chosen_display is None else self.cur_order[chosen_display]
        self.answers.append((self.queue[self.pos], orig))
        return orig

    def skip(self):
        if self.answered:
            return
        self.answered = True
        self._record(None)
        self.reveal(None)

    def submit(self):
        if self.answered:
            return
        k = self.choice.get()
        if k < 0:
            messagebox.showinfo("No answer", "Choose an answer first (or press Skip).")
            return
        self.answered = True
        self._record(k)
        self.reveal(k)

    def reveal(self, k):
        correct = self.cur_order.index(0)
        for i, rb in enumerate(self.opt_widgets):
            rb.configure(state="disabled", disabledforeground=DARK)
            if i == correct:
                rb.configure(bg="#E8F5E0", disabledforeground="#2F6B12")
            elif i == k:
                rb.configure(bg="#FDE8E8", disabledforeground=RED)
        self.skip_btn.pack_forget()
        if self.learn:
            ok = k == correct
            head = "Correct!" if ok else ("Skipped." if k is None else "Not quite.")
            tk.Label(self.feedback, text=head, bg=CARD, fg=GREEN if ok else RED,
                     font=(FONT, 12, "bold")).pack(anchor="w")
            tk.Label(self.feedback, text=Q[self.queue[self.pos]]["e"], bg=CARD, fg=DARK, font=(FONT, 10),
                     wraplength=840, justify="left").pack(anchor="w", pady=(2, 0))
            last = self.pos + 1 >= len(self.queue)
            self.main_btn.configure(text="See my report" if last else "Next question  >", command=self.next)
            self.enter_action = self.next
        else:
            self.next()

    def next(self):
        self.pos += 1
        if self.pos >= len(self.queue):
            self.finish()
        else:
            self.show_question()

    # ---------- report ----------
    def finish(self):
        self.finished = datetime.now()
        if not self.answers:
            self.home()
            return
        self.clear()
        answers = self.answers
        right = sum(1 for _, c in answers if c == 0)
        pct = round(100 * right / len(answers))
        stats = topic_stats(answers)
        strong, mid, weak = strengths(stats)
        mins, secs = divmod(int((self.finished - self.started).total_seconds()), 60)

        self.header("Your interview report", f"{self.user or 'Anonymous'} - {mins} min {secs} s")
        inner = self.scrollable()
        card = tk.Frame(inner, bg=CARD, padx=30, pady=20)
        card.pack(fill="x", padx=40, pady=20)

        top = tk.Frame(card, bg=CARD)
        top.pack(fill="x")
        color = GREEN if pct >= 70 else (AMBER if pct >= 50 else RED)
        tk.Label(top, text=f"{pct}%", bg=CARD, fg=color, font=(FONT, 40, "bold")).pack(side="left")
        info = tk.Frame(top, bg=CARD)
        info.pack(side="left", padx=20)
        tk.Label(info, text=f"Level: {level(pct)}", bg=CARD, fg=DARK, font=(FONT, 16, "bold")).pack(anchor="w")
        tk.Label(info, text=f"{right} correct out of {len(answers)} questions", bg=CARD, fg=MUTED,
                 font=(FONT, 11)).pack(anchor="w")
        tk.Label(info, text="0-49% Novice  |  50-69% Apprentice  |  70-84% Practitioner  |  85-100% Expert-ready",
                 bg=CARD, fg=MUTED, font=(FONT, 9)).pack(anchor="w", pady=(4, 0))

        btns = tk.Frame(card, bg=CARD)
        btns.pack(anchor="w", pady=(14, 6))
        self.button(btns, "Save PDF report", self.save_report).pack(side="left")
        self.button(btns, "New interview", self.home, primary=False).pack(side="left", padx=10)
        self.button(btns, "Quit", self.destroy, primary=False).pack(side="left")

        def section(title):
            tk.Label(card, text=title, bg=CARD, fg=GREEN, font=(FONT, 13, "bold")).pack(anchor="w", pady=(16, 4))

        section("Score by topic")
        table = tk.Frame(card, bg=CARD)
        table.pack(anchor="w", fill="x")
        for r, (key, label) in enumerate([t for t in TOPICS if t[0] in stats]):
            ok, n = stats[key]
            tp = round(100 * ok / n)
            c = GREEN if tp >= 75 else (AMBER if tp >= 50 else RED)
            tk.Label(table, text=label, bg=CARD, fg=DARK, font=(FONT, 10), anchor="w", width=30).grid(row=r, column=0, sticky="w")
            cv = tk.Canvas(table, width=260, height=14, bg="#E5E7EB", highlightthickness=0)
            cv.create_rectangle(0, 0, max(2, 260 * tp / 100), 14, fill=c, width=0)
            cv.grid(row=r, column=1, padx=10, pady=2)
            tk.Label(table, text=f"{ok}/{n}  ({tp}%)", bg=CARD, fg=DARK, font=(FONT, 10)).grid(row=r, column=2, sticky="w")

        section("Strong points")
        tk.Label(card, text="\n".join("+  " + TOPIC_NAME[k] for k in strong) or "No topic reached 75% yet.",
                 bg=CARD, fg="#2F6B12", font=(FONT, 10), justify="left").pack(anchor="w")
        if mid:
            section("Average (50-74%)")
            tk.Label(card, text="\n".join("~  " + TOPIC_NAME[k] for k in mid), bg=CARD, fg=AMBER,
                     font=(FONT, 10), justify="left").pack(anchor="w")
        section("Weak points and what to study")
        if weak:
            for k in weak:
                tk.Label(card, text="-  " + TOPIC_NAME[k], bg=CARD, fg=RED, font=(FONT, 10, "bold")).pack(anchor="w")
                tk.Label(card, text=ADVICE[k], bg=CARD, fg=DARK, font=(FONT, 10), wraplength=820,
                         justify="left").pack(anchor="w", padx=(18, 0), pady=(0, 4))
        else:
            tk.Label(card, text="No weak topic (below 50%). Great job!", bg=CARD, fg=DARK, font=(FONT, 10)).pack(anchor="w")

        wrong = [(qi, c) for qi, c in answers if c != 0]
        section(f"Questions to review ({len(wrong)})")
        for qi, c in wrong:
            q = Q[qi]
            tk.Label(card, text=q["q"], bg=CARD, fg=DARK, font=(FONT, 10, "bold"), wraplength=820,
                     justify="left").pack(anchor="w", pady=(6, 0))
            if c is not None:
                tk.Label(card, text="Your answer: " + q["o"][c], bg=CARD, fg=RED, font=(FONT, 10), wraplength=820,
                         justify="left").pack(anchor="w")
            tk.Label(card, text="Correct: " + q["o"][0], bg=CARD, fg="#2F6B12", font=(FONT, 10), wraplength=820,
                     justify="left").pack(anchor="w")
            tk.Label(card, text=q["e"], bg=CARD, fg=MUTED, font=(FONT, 9), wraplength=820,
                     justify="left").pack(anchor="w")
        self.enter_action = self.save_report

    def save_report(self):
        default = f"Spring-AI-Interview-Report-{(self.user or 'candidate').replace(' ', '-')}-{self.finished:%Y%m%d-%H%M}.pdf"
        path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")], initialfile=default)
        if path:
            write_report(path, self.user, self.answers, self.started, self.finished)
            self._open(path)

    def _open(self, path):
        try:
            os.startfile(path)
        except Exception:
            messagebox.showinfo("Saved", f"Saved to {path}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--guide":
        write_guide(sys.argv[2] if len(sys.argv) > 2 else "Spring-AI-Interview-Questions-and-Answers.pdf")
    else:
        App().mainloop()
