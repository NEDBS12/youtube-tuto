"""Generates three weeks of realistic sample sessions for --demo."""
import os
import random
from datetime import date, datetime, timedelta

import storage

WORK = [("code.exe", "app.py - screenAnalyze - Visual Studio Code"),
        ("chrome.exe", "Issues · my-project - GitHub - Google Chrome"),
        ("chrome.exe", "python - sqlite WAL mode - Stack Overflow - Google Chrome"),
        ("windowsterminal.exe", "PowerShell"),
        ("winword.exe", "Quarterly report.docx - Word"),
        ("excel.exe", "Budget 2026.xlsx - Excel"),
        ("chrome.exe", "Project plan - Google Docs - Google Chrome"),
        ("notion.exe", "Sprint board - Notion")]
NEUTRAL = [("outlook.exe", "Inbox - Outlook"), ("ms-teams.exe", "Chat | Microsoft Teams"),
           ("chrome.exe", "Inbox (12) - Gmail - Google Chrome"), ("explorer.exe", "Downloads"),
           ("chrome.exe", "best standing desk - Google Search - Google Chrome"), ("slack.exe", "general - Slack")]
FUN = [("chrome.exe", "lofi beats - YouTube - Google Chrome"), ("chrome.exe", "Instagram - Google Chrome"),
       ("chrome.exe", "r/programming - Reddit - Google Chrome"), ("whatsapp.exe", "WhatsApp"),
       ("chrome.exe", "Home / X - Google Chrome"), ("chrome.exe", "Facebook - Google Chrome"),
       ("chrome.exe", "Netflix - Google Chrome")]


def generate(path, days=21):
    if os.path.exists(path):
        os.remove(path)
    conn = storage.connect(path)
    rnd = random.Random(7)
    today = date.today()
    rows = []
    for i in range(days - 1, -1, -1):
        d = today - timedelta(days=i)
        weekend = d.weekday() >= 5
        t = datetime(d.year, d.month, d.day, rnd.choice([8, 9, 9, 10]), rnd.randint(0, 50)).timestamp()
        stop = t + rnd.uniform(4, 6.5 if weekend else 9.5) * 3600
        if i == 0:  # today: a session that ends right now
            stop = datetime.now().timestamp()
            t = stop - rnd.uniform(3, 5) * 3600
        while t < stop:
            hour = datetime.fromtimestamp(t).hour
            slump = hour in (13, 14, 16) or hour >= 20
            p_fun = (0.45 if weekend else 0.18) + (0.18 if slump else 0)
            r = rnd.random()
            if r < p_fun:
                exe, title = rnd.choice(FUN)
                dur = rnd.uniform(60, 900 if "youtube" in title.lower() or "netflix" in title.lower() else 420)
            elif r < p_fun + 0.2:
                exe, title = rnd.choice(NEUTRAL)
                dur = rnd.uniform(30, 420)
            else:
                exe, title = rnd.choice(WORK[:5] if hour < 13 else WORK)
                dur = rnd.uniform(120, 2400 if hour in (9, 10, 11, 15) else 1200)
            rows.append((t, t + dur, exe, title))
            t += dur
            if rnd.random() < 0.08:
                away = rnd.uniform(300, 2700)
                rows.append((t, t + away, storage.IDLE, ""))
                t += away
    conn.executemany("INSERT INTO sessions(start, end, exe, title) VALUES (?,?,?,?)", rows)
    conn.commit()
    conn.close()
