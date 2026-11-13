"""SQLite storage: one row per continuous session in one window."""
import sqlite3

IDLE = "__idle__"

SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    start REAL NOT NULL,
    end   REAL NOT NULL,
    exe   TEXT NOT NULL,
    title TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_sessions_start ON sessions(start);
CREATE INDEX IF NOT EXISTS idx_sessions_end ON sessions(end);
"""


def connect(path):
    conn = sqlite3.connect(path, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.executescript(SCHEMA)
    return conn


def insert(conn, start, end, exe, title):
    cur = conn.execute(
        "INSERT INTO sessions(start, end, exe, title) VALUES (?, ?, ?, ?)",
        (start, end, exe, title),
    )
    conn.commit()
    return cur.lastrowid


def update_end(conn, row_id, end):
    conn.execute("UPDATE sessions SET end = ? WHERE id = ?", (end, row_id))
    conn.commit()


def fetch(conn, t0, t1):
    """Sessions overlapping [t0, t1), clipped to that window."""
    rows = conn.execute(
        "SELECT start, end, exe, title FROM sessions "
        "WHERE end > ? AND start < ? ORDER BY start",
        (t0, t1),
    ).fetchall()
    out = []
    for start, end, exe, title in rows:
        s, e = max(start, t0), min(end, t1)
        if e > s:
            out.append((s, e, exe, title))
    return out
