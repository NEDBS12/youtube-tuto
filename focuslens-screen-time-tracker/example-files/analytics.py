"""Turns raw sessions into the numbers the dashboard shows."""
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta

import rules
import storage

DEEP_WORK_MIN = 25 * 60       # a productive block this long counts as deep work
FOCUS_GAP_TOLERANCE = 2 * 60  # short non-productive blips don't break a focus block
SWITCH_MIN = 5                # ignore windows shown for less than this (alt-tab noise)


def day_bounds(d):
    start = datetime(d.year, d.month, d.day).timestamp()
    end = datetime.combine(d + timedelta(days=1), datetime.min.time()).timestamp()
    return start, end


def _classified(conn, t0, t1, cfg):
    out = []
    for s, e, exe, title in storage.fetch(conn, t0, t1):
        if exe == storage.IDLE:
            out.append({"start": s, "end": e, "activity": "Away", "app": "", "category": "idle", "title": ""})
        else:
            activity, app, category = rules.classify(exe, title, cfg)
            out.append({"start": s, "end": e, "activity": activity, "app": app,
                        "category": category, "title": title})
    return out


def _merge_runs(rows, gap=3):
    """Join consecutive rows of the same activity into one block."""
    blocks = []
    for r in rows:
        last = blocks[-1] if blocks else None
        if last and last["activity"] == r["activity"] and r["start"] - last["end"] <= gap:
            last["end"] = max(last["end"], r["end"])
        else:
            blocks.append({k: r[k] for k in ("start", "end", "activity", "app", "category")})
    return blocks


def _focus_blocks(blocks):
    """Productive stretches, tolerating short interruptions."""
    out, cur = [], None
    for b in blocks:
        if b["category"] == "productive":
            if cur and b["start"] - cur["end"] <= FOCUS_GAP_TOLERANCE:
                cur["end"] = b["end"]
                cur["work"] += b["end"] - b["start"]
            else:
                cur = {"start": b["start"], "end": b["end"], "work": b["end"] - b["start"]}
                out.append(cur)
    return out


def _summary(rows):
    totals = Counter()
    for r in rows:
        totals[r["category"]] += r["end"] - r["start"]
    active = totals["productive"] + totals["neutral"] + totals["distracting"]
    focus = round(100 * (totals["productive"] + 0.4 * totals["neutral"]) / active) if active else 0
    return {
        "productive": round(totals["productive"]), "neutral": round(totals["neutral"]),
        "distracting": round(totals["distracting"]), "idle": round(totals["idle"]),
        "active": round(active), "focus_score": focus,
    }


def day_report(conn, d, cfg):
    t0, t1 = day_bounds(d)
    rows = _classified(conn, t0, t1, cfg)
    blocks = _merge_runs(rows)
    summary = _summary(rows)

    hourly = [{"hour": h, "productive": 0, "neutral": 0, "distracting": 0} for h in range(24)]
    for r in rows:
        if r["category"] == "idle":
            continue
        s = r["start"]
        while s < r["end"]:
            h = int((s - t0) // 3600)
            if h > 23:
                break
            chunk_end = min(r["end"], t0 + (h + 1) * 3600)
            hourly[h][r["category"]] += chunk_end - s
            s = chunk_end
    for h in hourly:
        for c in rules.CATEGORIES:
            h[c] = round(h[c])

    acts = {}
    for r in rows:
        if r["category"] == "idle":
            continue
        a = acts.setdefault(r["activity"], {"name": r["activity"], "app": r["app"], "category": r["category"],
                                            "seconds": 0, "sessions": 0, "titles": Counter()})
        dur = r["end"] - r["start"]
        a["seconds"] += dur
        if r["title"]:
            a["titles"][r["title"]] += dur
    for b in blocks:
        if b["activity"] in acts and b["end"] - b["start"] >= SWITCH_MIN:
            acts[b["activity"]]["sessions"] += 1
    activities = sorted(acts.values(), key=lambda a: -a["seconds"])
    for a in activities:
        a["seconds"] = round(a["seconds"])
        a["titles"] = [{"title": t, "seconds": round(s)} for t, s in a["titles"].most_common(5)]

    meaningful = [b for b in blocks if b["category"] != "idle" and b["end"] - b["start"] >= SWITCH_MIN]
    switches = sum(1 for a, b in zip(meaningful, meaningful[1:]) if a["activity"] != b["activity"])
    focus = _focus_blocks(blocks)
    deep = [f for f in focus if f["work"] >= DEEP_WORK_MIN]
    longest = max((f["work"] for f in focus), default=0)
    active_rows = [r for r in rows if r["category"] != "idle"]

    return {
        "date": d.isoformat(),
        "summary": summary,
        "switches": switches,
        "switches_per_hour": round(switches / (summary["active"] / 3600), 1) if summary["active"] >= 600 else 0,
        "longest_focus": round(longest),
        "deep_sessions": [{"start": f["start"], "end": f["end"], "seconds": round(f["work"])} for f in deep],
        "first_seen": active_rows[0]["start"] if active_rows else None,
        "last_seen": active_rows[-1]["end"] if active_rows else None,
        "hourly": hourly,
        "timeline": [{**b, "seconds": round(b["end"] - b["start"])} for b in blocks if b["end"] - b["start"] >= 1],
        "activities": activities,
        "goal_hours": cfg["settings"]["goal_hours"],
    }


def range_report(conn, end, days, cfg):
    out = []
    for i in range(days - 1, -1, -1):
        d = end - timedelta(days=i)
        t0, t1 = day_bounds(d)
        s = _summary(_classified(conn, t0, t1, cfg))
        s["date"] = d.isoformat()
        out.append(s)
    return out


def habits_report(conn, end, days, cfg):
    """Patterns across many days: when distraction happens and what triggers it."""
    t0, _ = day_bounds(end - timedelta(days=days - 1))
    _, t1 = day_bounds(end)
    rows = _classified(conn, t0, t1, cfg)

    # weekday x hour grid of minutes per category
    grid = defaultdict(lambda: Counter())
    day_seen = set()
    for r in rows:
        if r["category"] == "idle":
            continue
        s = r["start"]
        while s < r["end"]:
            dt = datetime.fromtimestamp(s)
            day_seen.add(dt.date())
            next_hour = (dt.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)).timestamp()
            e = min(r["end"], next_hour)
            grid[(dt.weekday(), dt.hour)][r["category"]] += e - s
            s = e
    weekday_count = Counter(d.weekday() for d in day_seen)
    heat = []
    for wd in range(7):
        n = max(weekday_count[wd], 1)
        for h in range(24):
            c = grid[(wd, h)]
            heat.append({"weekday": wd, "hour": h,
                         "productive": round(c["productive"] / n / 60, 1),
                         "neutral": round(c["neutral"] / n / 60, 1),
                         "distracting": round(c["distracting"] / n / 60, 1)})

    # what you jump to right after productive work
    blocks = [b for b in _merge_runs(rows) if b["end"] - b["start"] >= SWITCH_MIN]
    triggers = Counter()
    for a, b in zip(blocks, blocks[1:]):
        if a["category"] == "productive" and b["category"] == "distracting":
            triggers[(a["activity"], b["activity"])] += 1
    top_triggers = [{"from": f, "to": t, "count": n} for (f, t), n in triggers.most_common(5)]

    # how long distraction episodes last once they start
    episodes = []
    run = 0
    for b in blocks:
        if b["category"] == "distracting":
            run += b["end"] - b["start"]
        elif run:
            episodes.append(run)
            run = 0
    if run:
        episodes.append(run)

    return {
        "days": days,
        "tracked_days": len(day_seen),
        "heatmap": heat,
        "triggers": top_triggers,
        "distraction_episodes": len(episodes),
        "avg_distraction_episode": round(sum(episodes) / len(episodes)) if episodes else 0,
    }


def parse_date(s):
    try:
        return date.fromisoformat(s)
    except (TypeError, ValueError):
        return date.today()
