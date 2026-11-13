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
import uuid

import storage
import rules

user32 = ctypes.WinDLL("user32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
AUDIO_LEVEL = 0.002  # peak level above which sound counts as playing


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


def _guid(s):
    return (ctypes.c_byte * 16).from_buffer_copy(uuid.UUID(s).bytes_le)


def _com(ptr, index, *argtypes):
    """Method number `index` of a COM object's vtable."""
    vtbl = ctypes.cast(ptr, ctypes.POINTER(ctypes.POINTER(ctypes.c_void_p))).contents
    return ctypes.WINFUNCTYPE(ctypes.HRESULT, ctypes.c_void_p, *argtypes)(vtbl[index])


class AudioMeter:
    """Peak level of the default speakers/headphones (Windows Core Audio).

    Watching a lecture or a video produces sound but no mouse/keyboard input,
    so sound is the signal that someone is still in front of the screen.
    Create and use it from a single thread (it initialises COM there).
    """
    CLSID_ENUMERATOR = "BCDE0395-E52F-467C-8E3D-C4579291692E"
    IID_ENUMERATOR = "A95664D2-9614-4F35-A746-DE8DB63617E6"
    IID_METER = "C02216F6-8C67-4B5B-9D00-D008E73E0064"
    REFRESH_EVERY = 30  # the default device changes when headphones are plugged in

    def __init__(self):
        ctypes.oledll.ole32.CoInitialize(None)
        self._meter = None
        self._opened = 0.0

    def _release(self):
        if self._meter:
            _com(self._meter, 2)(self._meter)
            self._meter = None

    def _open(self):
        self._release()
        self._opened = time.time()
        ole32 = ctypes.oledll.ole32
        enum, device, meter = ctypes.c_void_p(), ctypes.c_void_p(), ctypes.c_void_p()
        ole32.CoCreateInstance(_guid(self.CLSID_ENUMERATOR), None, 23,  # CLSCTX_ALL
                               _guid(self.IID_ENUMERATOR), ctypes.byref(enum))
        try:
            # IMMDeviceEnumerator::GetDefaultAudioEndpoint(eRender, eMultimedia, &device)
            _com(enum, 4, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_void_p))(enum, 0, 1, ctypes.byref(device))
            try:
                # IMMDevice::Activate(IID_IAudioMeterInformation, CLSCTX_ALL, NULL, &meter)
                _com(device, 3, ctypes.c_void_p, wt.DWORD, ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p))(
                    device, ctypes.addressof(_guid(self.IID_METER)), 23, None, ctypes.byref(meter))
                self._meter = meter
            finally:
                _com(device, 2)(device)
        finally:
            _com(enum, 2)(enum)

    def peak(self):
        """0.0 (silence) to 1.0; 0.0 when there is no audio device."""
        try:
            if not self._meter or time.time() - self._opened > self.REFRESH_EVERY:
                self._open()
            value = ctypes.c_float()
            _com(self._meter, 3, ctypes.POINTER(ctypes.c_float))(self._meter, ctypes.byref(value))
            return value.value
        except OSError:
            self._meter = None
            return 0.0


class Tracker(threading.Thread):
    SAMPLE_EVERY = 1.0
    FLUSH_EVERY = 10.0

    def __init__(self, db_path):
        super().__init__(daemon=True)
        self.db_path = db_path
        self._stop = threading.Event()
        self._last_sound = 0.0

    def stop(self):
        self._stop.set()

    def _sample(self, cfg, meter):
        """Return (exe, title, started_at) for the current state."""
        now = time.time()
        exe, title = foreground_window()
        idle = idle_seconds()
        settings = cfg["settings"]
        # Sound from a browser, player or call counts as presence: you are watching
        # or listening. Short silences (a pause between two sentences) are fine.
        if exe and rules.plays_media(exe) and meter.peak() > AUDIO_LEVEL:
            self._last_sound = now
        if idle < settings["audio_idle_minutes"] * 60:
            idle = min(idle, now - self._last_sound)
        if exe in (None, "lockapp.exe", "logonui.exe") or idle >= settings["idle_minutes"] * 60:
            return storage.IDLE, "", now - idle
        return exe, title or "", now

    def run(self):
        conn = storage.connect(self.db_path)
        meter = AudioMeter()
        cfg = rules.load_config()
        cfg_loaded = time.time()
        current = None  # dict(id, exe, title, end)
        last_flush = 0.0
        while not self._stop.is_set():
            try:
                if time.time() - cfg_loaded > 30:
                    cfg, cfg_loaded = rules.load_config(), time.time()
                exe, title, started = self._sample(cfg, meter)
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
