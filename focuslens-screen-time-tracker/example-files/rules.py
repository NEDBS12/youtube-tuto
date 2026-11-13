"""Turns a raw (exe, window title) into a named activity and a category.

Categories: productive, neutral, distracting. Everything is editable in
config.json (created on first run) or from the dashboard.
"""
import copy
import json
import os
import sys
import threading

BASE = os.path.dirname(sys.executable if getattr(sys, "frozen", False) else os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE, "config.json")
CATEGORIES = ("productive", "neutral", "distracting")
_lock = threading.Lock()

BROWSERS = {
    "chrome.exe": "Google Chrome", "msedge.exe": "Microsoft Edge", "firefox.exe": "Firefox",
    "brave.exe": "Brave", "opera.exe": "Opera", "opera_gx.exe": "Opera GX",
    "vivaldi.exe": "Vivaldi", "arc.exe": "Arc", "iexplore.exe": "Internet Explorer",
}

DEFAULT_CONFIG = {
    "settings": {
        "goal_hours": 6,            # daily productive-time goal
        "idle_minutes": 3,          # no input for this long = away
        "audio_idle_minutes": 240,  # while a video/call plays sound, stay "present" up to this long
    },
    # exe -> [display name, category]
    "apps": {
        "code.exe": ["VS Code", "productive"],
        "cursor.exe": ["Cursor", "productive"],
        "devenv.exe": ["Visual Studio", "productive"],
        "pycharm64.exe": ["PyCharm", "productive"],
        "idea64.exe": ["IntelliJ IDEA", "productive"],
        "webstorm64.exe": ["WebStorm", "productive"],
        "rider64.exe": ["Rider", "productive"],
        "datagrip64.exe": ["DataGrip", "productive"],
        "studio64.exe": ["Android Studio", "productive"],
        "sublime_text.exe": ["Sublime Text", "productive"],
        "notepad++.exe": ["Notepad++", "productive"],
        "windowsterminal.exe": ["Terminal", "productive"],
        "powershell.exe": ["PowerShell", "productive"],
        "pwsh.exe": ["PowerShell", "productive"],
        "cmd.exe": ["Command Prompt", "productive"],
        "wsl.exe": ["WSL", "productive"],
        "postman.exe": ["Postman", "productive"],
        "claude.exe": ["Claude", "productive"],
        "chatgpt.exe": ["ChatGPT", "productive"],
        "winword.exe": ["Word", "productive"],
        "excel.exe": ["Excel", "productive"],
        "powerpnt.exe": ["PowerPoint", "productive"],
        "onenote.exe": ["OneNote", "productive"],
        "notion.exe": ["Notion", "productive"],
        "obsidian.exe": ["Obsidian", "productive"],
        "figma.exe": ["Figma", "productive"],
        "photoshop.exe": ["Photoshop", "productive"],
        "illustrator.exe": ["Illustrator", "productive"],
        "acrobat.exe": ["Acrobat", "productive"],
        "acrord32.exe": ["Acrobat Reader", "productive"],
        "matlab.exe": ["MATLAB", "productive"],
        "rstudio.exe": ["RStudio", "productive"],
        "blender.exe": ["Blender", "productive"],
        "outlook.exe": ["Outlook", "neutral"],
        "olk.exe": ["Outlook", "neutral"],
        "ms-teams.exe": ["Teams", "neutral"],
        "teams.exe": ["Teams", "neutral"],
        "slack.exe": ["Slack", "neutral"],
        "zoom.exe": ["Zoom", "neutral"],
        "explorer.exe": ["File Explorer", "neutral"],
        "notepad.exe": ["Notepad", "neutral"],
        "systemsettings.exe": ["Settings", "neutral"],
        "taskmgr.exe": ["Task Manager", "neutral"],
        "spotify.exe": ["Spotify", "neutral"],
        "whatsapp.exe": ["WhatsApp", "distracting"],
        "telegram.exe": ["Telegram", "distracting"],
        "discord.exe": ["Discord", "distracting"],
        "steam.exe": ["Steam", "distracting"],
        "steamwebhelper.exe": ["Steam", "distracting"],
        "epicgameslauncher.exe": ["Epic Games", "distracting"],
        "vlc.exe": ["VLC", "distracting"],
        "netflix.exe": ["Netflix", "distracting"],
    },
    # Matched against browser tab titles (lower-case substring).
    "sites": [
        {"name": "GitHub", "keywords": ["github"], "category": "productive"},
        {"name": "Stack Overflow", "keywords": ["stack overflow"], "category": "productive"},
        {"name": "GitLab", "keywords": ["gitlab"], "category": "productive"},
        {"name": "ChatGPT", "keywords": ["chatgpt"], "category": "productive"},
        {"name": "Claude", "keywords": ["claude"], "category": "productive"},
        {"name": "Google Docs", "keywords": ["google docs", "- google docs"], "category": "productive"},
        {"name": "Google Sheets", "keywords": ["google sheets"], "category": "productive"},
        {"name": "Google Slides", "keywords": ["google slides"], "category": "productive"},
        {"name": "Notion", "keywords": ["notion"], "category": "productive"},
        {"name": "Figma", "keywords": ["figma"], "category": "productive"},
        {"name": "Jira", "keywords": ["jira"], "category": "productive"},
        {"name": "Confluence", "keywords": ["confluence"], "category": "productive"},
        {"name": "Docs & references", "keywords": ["mdn web docs", "w3schools", "documentation", " docs", "devdocs"], "category": "productive"},
        {"name": "Online courses", "keywords": ["coursera", "udemy", "edx", "khan academy", "linkedin learning"], "category": "productive"},
        {"name": "LeetCode", "keywords": ["leetcode"], "category": "productive"},
        {"name": "Overleaf", "keywords": ["overleaf"], "category": "productive"},
        {"name": "Localhost", "keywords": ["localhost", "127.0.0.1"], "category": "productive"},
        {"name": "Gmail", "keywords": ["gmail", "inbox ("], "category": "neutral"},
        {"name": "Outlook Web", "keywords": ["outlook"], "category": "neutral"},
        {"name": "Google Calendar", "keywords": ["google calendar"], "category": "neutral"},
        {"name": "Google Search", "keywords": ["- google search", "google search"], "category": "neutral"},
        {"name": "Google Translate", "keywords": ["google translate"], "category": "neutral"},
        {"name": "Wikipedia", "keywords": ["wikipedia"], "category": "neutral"},
        {"name": "LinkedIn", "keywords": ["linkedin"], "category": "neutral"},
        {"name": "Medium", "keywords": ["medium"], "category": "neutral"},
        {"name": "YouTube", "keywords": ["youtube"], "category": "distracting"},
        {"name": "Netflix", "keywords": ["netflix"], "category": "distracting"},
        {"name": "Prime Video", "keywords": ["prime video"], "category": "distracting"},
        {"name": "Disney+", "keywords": ["disney+"], "category": "distracting"},
        {"name": "Twitch", "keywords": ["twitch"], "category": "distracting"},
        {"name": "Facebook", "keywords": ["facebook"], "category": "distracting"},
        {"name": "Instagram", "keywords": ["instagram"], "category": "distracting"},
        {"name": "TikTok", "keywords": ["tiktok"], "category": "distracting"},
        {"name": "X / Twitter", "keywords": ["twitter", " / x"], "category": "distracting"},
        {"name": "Reddit", "keywords": ["reddit"], "category": "distracting"},
        {"name": "Pinterest", "keywords": ["pinterest"], "category": "distracting"},
        {"name": "Snapchat", "keywords": ["snapchat"], "category": "distracting"},
        {"name": "WhatsApp Web", "keywords": ["whatsapp"], "category": "distracting"},
        {"name": "Messenger", "keywords": ["messenger"], "category": "distracting"},
        {"name": "Online shopping", "keywords": ["amazon", "aliexpress", "shein", "temu", "jumia", "ebay", "zalando", "zara"], "category": "distracting"},
        {"name": "News", "keywords": ["bbc", "cnn", "news"], "category": "distracting"},
    ],
    # activity name -> category, set from the dashboard; wins over everything.
    "overrides": {},
}


def _merge_defaults(cfg):
    out = copy.deepcopy(DEFAULT_CONFIG)
    for key, value in cfg.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key].update(value)
        else:
            out[key] = value
    return out


def load_config():
    with _lock:
        if not os.path.exists(CONFIG_PATH):
            save_config(DEFAULT_CONFIG)
            return copy.deepcopy(DEFAULT_CONFIG)
        try:
            with open(CONFIG_PATH, encoding="utf-8") as f:
                return _merge_defaults(json.load(f))
        except (OSError, json.JSONDecodeError):
            return copy.deepcopy(DEFAULT_CONFIG)


def save_config(cfg):
    tmp = CONFIG_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
    os.replace(tmp, CONFIG_PATH)


def update_config(mutator):
    cfg = load_config()
    mutator(cfg)
    with _lock:
        save_config(cfg)
    return cfg


def _match_site(title, cfg):
    low = title.lower()
    for site in cfg["sites"]:
        if any(k in low for k in site["keywords"]):
            return site
    return None


# Apps where you watch or listen without touching the mouse: sound from them means you are present.
MEDIA_APPS = {
    "vlc.exe", "netflix.exe", "spotify.exe", "wmplayer.exe", "potplayer64.exe", "mpc-hc64.exe",
    "video.ui.exe", "microsoft.media.player.exe", "zoom.exe", "ms-teams.exe", "teams.exe",
    "slack.exe", "discord.exe", "whatsapp.exe", "telegram.exe",
}


def plays_media(exe):
    return exe in BROWSERS or exe in MEDIA_APPS


def _pretty_exe(exe):
    name = exe[:-4] if exe.endswith(".exe") else exe
    return name.replace("_", " ").replace("-", " ").title()


def classify(exe, title, cfg):
    """Return (activity, app, category)."""
    if exe in BROWSERS:
        app = BROWSERS[exe]
        site = _match_site(title, cfg)
        if site:
            activity, category = site["name"], site["category"]
        else:
            activity, category = "Web browsing", "neutral"
    elif exe in cfg["apps"]:
        app, category = cfg["apps"][exe]
        activity = app
    else:
        app = activity = _pretty_exe(exe)
        category = "neutral"
    category = cfg["overrides"].get(activity, category)
    return activity, app, category
