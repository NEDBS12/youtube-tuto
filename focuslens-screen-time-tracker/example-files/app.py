"""FocusLens - screen-time tracker + local dashboard.

    python app.py            track this PC and serve the dashboard
    python app.py --demo     dashboard over generated sample data (no tracking)
    python app.py --no-browser

The dashboard is served only on 127.0.0.1; all data stays in this folder.
"""
import argparse
import json
import os
import socket
import sys
import webbrowser
from datetime import date
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

import analytics
import rules
import storage

if getattr(sys, "frozen", False):  # running as FocusLens.exe: data next to the exe
    BASE = os.path.dirname(sys.executable)
    STATIC = os.path.join(sys._MEIPASS, "static")
else:
    BASE = os.path.dirname(os.path.abspath(__file__))
    STATIC = os.path.join(BASE, "static")
PORT = 8765


class Handler(SimpleHTTPRequestHandler):
    db_path = None
    demo = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC, **kwargs)

    def log_message(self, *args):
        pass

    def _json(self, payload, status=200):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urlparse(self.path)
        if not url.path.startswith("/api/"):
            return super().do_GET()
        q = {k: v[0] for k, v in parse_qs(url.query).items()}
        cfg = rules.load_config()
        conn = storage.connect(self.db_path)
        try:
            d = analytics.parse_date(q.get("date"))
            if url.path == "/api/day":
                return self._json(analytics.day_report(conn, d, cfg))
            if url.path == "/api/range":
                days = min(max(int(q.get("days", 7)), 1), 90)
                return self._json(analytics.range_report(conn, d, days, cfg))
            if url.path == "/api/habits":
                days = min(max(int(q.get("days", 28)), 1), 90)
                return self._json(analytics.habits_report(conn, d, days, cfg))
            if url.path == "/api/config":
                return self._json({"settings": cfg["settings"], "demo": self.demo,
                                   "today": date.today().isoformat()})
            self._json({"error": "not found"}, 404)
        finally:
            conn.close()

    def do_POST(self):
        length = int(self.headers.get("Content-Length") or 0)
        try:
            body = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            return self._json({"error": "bad json"}, 400)
        path = urlparse(self.path).path

        if path == "/api/override":
            activity, category = body.get("activity"), body.get("category")
            if not activity or category not in rules.CATEGORIES:
                return self._json({"error": "invalid"}, 400)
            rules.update_config(lambda c: c["overrides"].__setitem__(activity, category))
            return self._json({"ok": True})

        if path == "/api/settings":
            def apply(c):
                for key, lo, hi in (("goal_hours", 0.5, 16), ("idle_minutes", 1, 60), ("media_idle_minutes", 1, 180)):
                    if key in body:
                        c["settings"][key] = min(max(float(body[key]), lo), hi)
            cfg = rules.update_config(apply)
            return self._json({"settings": cfg["settings"]})

        self._json({"error": "not found"}, 404)


def port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


def main():
    ap = argparse.ArgumentParser(description="FocusLens screen-time tracker")
    ap.add_argument("--demo", action="store_true", help="use generated sample data")
    ap.add_argument("--no-browser", action="store_true")
    ap.add_argument("--port", type=int, default=PORT)
    args = ap.parse_args()
    url = f"http://127.0.0.1:{args.port}/"

    if port_in_use(args.port):
        print("FocusLens is already running ->", url)
        if not args.no_browser:
            webbrowser.open(url)
        return

    if args.demo:
        import demo
        Handler.db_path = os.path.join(BASE, "demo.db")
        Handler.demo = True
        demo.generate(Handler.db_path)
    else:
        if sys.platform != "win32":
            sys.exit("Tracking works on Windows only. Use --demo to preview the dashboard.")
        from tracker import Tracker
        Handler.db_path = os.path.join(BASE, "screentime.db")
        storage.connect(Handler.db_path).close()
        Tracker(Handler.db_path).start()

    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print("FocusLens dashboard ->", url, "(demo data)" if args.demo else "(tracking)")
    if not args.no_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
