"""Foreground-window tracker for Windows (stdlib only, uses ctypes).

Every second it samples the active window (process + title) and the time since
the last keyboard/mouse input. Consecutive identical samples are merged into one
session row in SQLite, so the database stays small.
"""
import ctypes
import ctypes.wintypes as wt
import os
import threading
import time

import storage
import rules

user32 = ctypes.WinDLL("user32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

PROCESS_QUERY_LIMITED_INFORMATION = 0x1000


class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", wt.UINT), ("dwTime", wt.DWORD)]


user32.GetForegroundWindow.restype = wt.HWND
user32.GetWindowTextLengthW.argtypes = [wt.HWND]
user32.GetWindowTextW.argtypes = [wt.HWND, wt.LPWSTR, ctypes.c_int]
user32.GetWindowThreadProcessId.argtypes = [wt.HWND, ctypes.POINTER(wt.DWORD)]
kernel32.OpenProcess.restype = wt.HANDLE
kernel32.QueryFullProcessImageNameW.argtypes = [wt.HANDLE, wt.DWORD, wt.LPWSTR, ctypes.POINTER(wt.DWORD)]
kernel32.GetTickCount.restype = wt.DWORD


def idle_seconds():
    info = LASTINPUTINFO()
    info.cbSize = ctypes.sizeof(LASTINPUTINFO)
    if not user32.GetLastInputInfo(ctypes.byref(info)):
        return 0.0
    elapsed = (kernel32.GetTickCount() - info.dwTime) & 0xFFFFFFFF
    return elapsed / 1000.0


def foreground_window():
    """Return (exe_name, window_title) of the active window, or (None, None)."""
    hwnd = user32.GetForegroundWindow()
    if not hwnd:
        return None, None
    length = user32.GetWindowTextLengthW(hwnd)
    buf = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buf, length + 1)
    title = buf.value

    pid = wt.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    exe = None
    handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid.value)
    if handle:
        try:
            size = wt.DWORD(1024)
            path = ctypes.create_unicode_buffer(size.value)
            if kernel32.QueryFullProcessImageNameW(handle, 0, path, ctypes.byref(size)):
                exe = os.path.basename(path.value).lower()
        finally:
            kernel32.CloseHandle(handle)
    return exe, title


class Tracker(threading.Thread):
    SAMPLE_EVERY = 1.0
    FLUSH_EVERY = 10.0

    def __init__(self, db_path):
        super().__init__(daemon=True)
        self.db_path = db_path
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def _sample(self, cfg):
        """Return (exe, title, started_at) for the current state."""
        now = time.time()
        exe, title = foreground_window()
        idle = idle_seconds()
        threshold = cfg["settings"]["idle_minutes"] * 60
        # Watching a video produces no input; give media a longer grace period.
        if exe and rules.is_media(exe, title or "", cfg):
            threshold = max(threshold, cfg["settings"]["media_idle_minutes"] * 60)
        if exe in (None, "lockapp.exe", "logonui.exe") or idle >= threshold:
            return storage.IDLE, "", now - (idle if idle >= threshold else 0)
        return exe, title or "", now

    def run(self):
        conn = storage.connect(self.db_path)
        cfg = rules.load_config()
        cfg_loaded = time.time()
        current = None  # dict(id, exe, title, end)
        last_flush = 0.0
        while not self._stop.is_set():
            try:
                if time.time() - cfg_loaded > 30:
                    cfg, cfg_loaded = rules.load_config(), time.time()
                exe, title, started = self._sample(cfg)
                now = time.time()
                # A sleep/hibernate gap: close the old row where it really ended.
                if current and now - current["end"] > 30:
                    storage.update_end(conn, current["id"], current["end"])
                    current = None
                if current and current["exe"] == exe and current["title"] == title:
                    current["end"] = now
                    if now - last_flush >= self.FLUSH_EVERY:
                        storage.update_end(conn, current["id"], now)
                        last_flush = now
                else:
                    start = now
                    if current:
                        # When going idle, the idle period began at the last input.
                        start = max(min(started, now), current.get("start", started))
                        storage.update_end(conn, current["id"], start)
                    row_id = storage.insert(conn, start, now, exe, title)
                    current = {"id": row_id, "exe": exe, "title": title, "start": start, "end": now}
                    last_flush = now
            except Exception as exc:  # never let the tracker die
                print("tracker error:", exc)
            self._stop.wait(self.SAMPLE_EVERY)
        if current:
            storage.update_end(conn, current["id"], time.time())
        conn.close()
