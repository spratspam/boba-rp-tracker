# ==========================================================
# BOBA RP TRACKER — DEV CHECKLIST
# ==========================================================

# ------------------------------
# PHASE 1 — CORE (COMPLETE)
# ------------------------------
# [x] App window (size, min size, title)
# [x] Theme system (Matcha / Thai Tea)
# [x] RP create/edit popup
# [x] Reply system (add/edit/delete)
# [x] JSON data persistence
# [x] Search + filter (basic)
# [x] RP detail window
# [x] Scrollable UI (main + replies)
# [x] Open URL button

# ------------------------------
# PHASE 2 — BUGS / FIXES
# ------------------------------

# --- ICON (EXE ISSUE) ---
# [ ] Fix EXE window icon not applying
# [ ] Handle sys._MEIPASS for PyInstaller
# [ ] Ensure .ico includes multiple sizes (16,32,48,256)
# [ ] Force icon after Tk() init in frozen mode

# --- DATA / SORTING ---
# [ ] Replace updated_at sorting
# [ ] Sort by oldest reply needing attention
# [ ] Prioritize threads where user owes reply
# [ ] Prevent newly added RP from jumping to top incorrectly

# --- FILTERING ---
# [ ] Add "Waiting on Me" filter
# [ ] Add "Waiting on Them" filter
# [ ] Add "Active only" filter
# [ ] Add "Needs Reply" smart filter

# ------------------------------
# PHASE 3 — CORE FEATURES
# ------------------------------

# --- PRIORITY SYSTEM ---
# [ ] Calculate last reply date
# [ ] Detect who replied last (Me / Them)
# [ ] Calculate "days waiting"
# [ ] Display priority indicator on card

# --- AUTO STATUS LOGIC ---
# [ ] Auto-update "last_turn" when reply added
# [ ] Auto-set status based on last reply
# [ ] Sync status with turn field

# --- REPLY IMPROVEMENTS ---
# [ ] Auto-fill reply date
# [ ] Add optional "draft" replies
# [ ] Quick-add reply from main card

# --- REMINDERS / POPUP ALERTS ---
# [ ] Add reminder date field to RP data
# [ ] Add reminder note / label field
# [ ] Show reminder date in RP detail window
# [ ] Show reminder indicator on RP card
# [ ] Highlight overdue reminders
# [ ] Add "Set Reminder" option when creating/editing RP
# [ ] Add "Clear Reminder" option
# [ ] Add "Reminders Due" filter
# [ ] Sort overdue reminders near top
# [ ] Add popup reminder on app launch for overdue reminders
# [ ] Add popup reminder when reminder date is today
# [ ] Add dismiss button for popup reminder
# [ ] Add "Remind Me Again Later" snooze option
# [ ] Add quick reminder buttons (Today / 3 Days / 1 Week)


# ------------------------------
# PHASE 4 — UI POLISH
# ------------------------------

# --- MAIN WINDOW ---
# [ ] Highlight selected RP
# [ ] Improve "Select" UX (less hidden)
# [ ] Clean spacing / alignment

# --- VISUAL FEEDBACK ---
# [ ] Stronger hover states
# [ ] Status color indicators
# [ ] Improve timestamp readability

# --- USABILITY ---
# [ ] Add keyboard shortcuts (Ctrl+N, Ctrl+F)
# [ ] Improve scroll behavior

# ------------------------------
# PHASE 5 — QUALITY OF LIFE
# ------------------------------

# --- DATA SAFETY ---
# [ ] Auto-backup JSON
# [ ] Export RPs (TXT / CSV)

# --- SEARCH ---
# [ ] Search inside replies
# [ ] Search by character
# [ ] Search by partner (played_by)

# --- QUICK ACTIONS ---
# [ ] Open URL from main card
# [ ] Add inline edit shortcut

# ------------------------------
# PHASE 6 — FUTURE IDEAS
# ------------------------------

# [ ] Tag system (angst, fluff, etc.)
# [ ] Pin favorite RPs
# [ ] Archive system
# [ ] Bulk import (from spreadsheet)
# [ ] Table-style export view

# ==========================================================


import json
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
from datetime import datetime
from pathlib import Path
from uuid import uuid4
import webbrowser

APP_NAME = "Boba RP Tracker"
APP_VERSION = "1.0.1"

DEFAULT_GEOMETRY = "470x720"
MIN_WIDTH = 420
MIN_HEIGHT = 560


def get_app_base_dir():
    import os
    app_name = "Boba RP Tracker"

    appdata = os.getenv("APPDATA")
    base_dir = Path(appdata) / app_name
    base_dir.mkdir(parents=True, exist_ok=True)

    return base_dir


BASE_DIR = get_app_base_dir()
DATA_DIR = BASE_DIR / "rp_tracker_data"
SETTINGS_PATH = DATA_DIR / "settings.json"
RPS_PATH = DATA_DIR / "rps.json"

ICON_ICO = BASE_DIR / "boba_matcha.ico" 

POSSIBLE_ICON_NAMES = [
    "boba_matcha.png",
    "boba_milk_tea.png",
    "bobaicon.png",
    "boba_icon.png",
    "boba.png",
]

MATCHA_THEME = {
    "name": "Matcha",
    "window_bg": "#efefea",
    "header_bg": "#dfe8cc",
    "header_inner": "#d0e1b8",
    "panel_bg": "#f7f9f1",
    "card_bg": "#dfeccf",
    "card_hover": "#d3e4bf",
    "border": "#9fbe7d",
    "text": "#31402f",
    "muted": "#5b6f56",
    "timestamp": "#73836e",
    "button_bg": "#b7d390",
    "button_hover": "#a4c57b",
    "button_text": "#2f402f",
    "accent": "#8fb85c",
    "accent_hover": "#7aa34a",
    "danger": "#b66b5b",
    "danger_hover": "#a55949",
    "white": "#ffffff",
    "entry_bg": "#ffffff",
    "menu_bg": "#f7f9f1",
    "menu_active": "#dceac7",
    "selected": "#cde0b9",
    "reply_left": "#edf4e3",
    "reply_right": "#d7e7c2",
}

THAI_TEA_THEME = {
    "name": "Thai Tea",
    "window_bg": "#fff6ee",
    "header_bg": "#f7d8ba",
    "header_inner": "#f4c99f",
    "panel_bg": "#fffaf4",
    "card_bg": "#f7dec3",
    "card_hover": "#f1d1ae",
    "border": "#d89a5b",
    "text": "#5b3418",
    "muted": "#8a5b35",
    "timestamp": "#9b6e47",
    "button_bg": "#f0b06d",
    "button_hover": "#e89b49",
    "button_text": "#4d2c14",
    "accent": "#f28a17",
    "accent_hover": "#dd780d",
    "danger": "#bc6a4d",
    "danger_hover": "#a6573d",
    "white": "#ffffff",
    "entry_bg": "#fffdfa",
    "menu_bg": "#fff8f1",
    "menu_active": "#f4dcc3",
    "selected": "#f2d5b4",
    "reply_left": "#fff3e6",
    "reply_right": "#f7dec3",
}

STATUS_OPTIONS = [
    "Active",
    "Waiting on Me",
    "Waiting on Them",
    "On Hold",
    "Complete",
    "Archived",
]

THREAD_TYPES = [
    "",
    "Thread",
    "Comm",
    "Chat",
    "Scene",
    "Other",
]

TURN_OPTIONS = [
    "",
    "Mine",
    "Theirs",
    "Complete",
]

WHO_OPTIONS = [
    "Me",
    "Them",
]


def now_display():
    return datetime.now().strftime("%m/%d/%Y %I:%M %p")


def now_iso():
    return datetime.now().isoformat()


def today_display():
    return datetime.now().strftime("%m/%d/%Y")


def reply_date_or_today(value):
    text = safe_text(value).strip()
    return text or today_display()


def safe_text(value):
    return value if isinstance(value, str) else ""


def compact(value, length=60):
    text = " ".join(safe_text(value).split())
    if not text:
        return ""
    return text[:length] + ("…" if len(text) > length else "")


def rounded_rect_points(x1, y1, x2, y2, r=18):
    return [
        x1 + r, y1,
        x2 - r, y1,
        x2, y1,
        x2, y1 + r,
        x2, y2 - r,
        x2, y2,
        x2 - r, y2,
        x1 + r, y2,
        x1, y2,
        x1, y2 - r,
        x1, y1 + r,
        x1, y1
    ]


class RoundedButton(tk.Canvas):
    def __init__(
        self,
        master,
        text,
        command,
        theme,
        width=120,
        height=36,
        bg_key="button_bg",
        hover_key="button_hover",
        text_key="button_text",
        border_key="border",
        radius=16,
    ):
        super().__init__(
            master,
            width=width,
            height=height,
            highlightthickness=0,
            bd=0,
            bg=master.cget("bg"),
            cursor="hand2",
        )
        self.command = command
        self.theme = theme
        self.width_v = width
        self.height_v = height
        self.text_v = text
        self.bg_key = bg_key
        self.hover_key = hover_key
        self.text_key = text_key
        self.border_key = border_key
        self.radius = radius
        self.hovered = False

        self.bind("<Button-1>", lambda e: self.command())
        self.bind("<Enter>", lambda e: self.set_hover(True))
        self.bind("<Leave>", lambda e: self.set_hover(False))
        self.redraw()

    def set_hover(self, value):
        self.hovered = value
        self.redraw()

    def redraw(self):
        self.delete("all")
        fill = self.theme[self.hover_key] if self.hovered else self.theme[self.bg_key]
        outline = self.theme[self.border_key]
        self.create_polygon(
            rounded_rect_points(2, 2, self.width_v - 2, self.height_v - 2, self.radius),
            smooth=True,
            fill=fill,
            outline=outline,
            width=1,
        )
        self.create_text(
            self.width_v / 2,
            self.height_v / 2,
            text=self.text_v,
            fill=self.theme[self.text_key],
            font=("Segoe UI", 9, "bold"),
        )

    def update_theme(self, theme):
        self.theme = theme
        self.configure(bg=self.master.cget("bg"))
        self.redraw()


class BasePopup(tk.Toplevel):
    def __init__(self, app, title, width=440, height=320):
        super().__init__(app.root)
        self.app = app
        self.theme = app.theme
        self.title(title)
        self.configure(bg=self.theme["window_bg"])
        self.transient(app.root)
        self.grab_set()
        self.geometry(f"{width}x{height}")
        self.minsize(width, height)

        if self.app.app_icon:
            try:
                self.iconphoto(True, self.app.app_icon)
            except Exception:
                pass

        self.outer = tk.Frame(self, bg=self.theme["window_bg"])
        self.outer.pack(fill="both", expand=True, padx=14, pady=14)

        self.container = tk.Frame(
            self.outer,
            bg=self.theme["panel_bg"],
            highlightthickness=1,
            highlightbackground=self.theme["border"],
            bd=0,
        )
        self.container.pack(fill="both", expand=True)

        self.bind("<Escape>", lambda e: self.destroy())
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.center_to_parent()

    def center_to_parent(self):
        self.update_idletasks()
        px = self.app.root.winfo_rootx()
        py = self.app.root.winfo_rooty()
        pw = self.app.root.winfo_width()
        ph = self.app.root.winfo_height()
        w = self.winfo_width()
        h = self.winfo_height()
        x = px + max((pw - w) // 2, 0)
        y = py + max((ph - h) // 2, 0)
        self.geometry(f"{w}x{h}+{x}+{y}")


class ConfirmPopup(BasePopup):
    def __init__(self, app, title, text, on_confirm):
        super().__init__(app, title, 360, 180)
        self.on_confirm = on_confirm

        tk.Label(
            self.container,
            text=title,
            bg=self.theme["panel_bg"],
            fg=self.theme["text"],
            font=("Segoe UI", 11, "bold"),
        ).pack(pady=(22, 8))

        tk.Label(
            self.container,
            text=text,
            bg=self.theme["panel_bg"],
            fg=self.theme["muted"],
            font=("Segoe UI", 9),
            justify="center",
        ).pack()

        row = tk.Frame(self.container, bg=self.theme["panel_bg"])
        row.pack(side="bottom", pady=18)

        self.cancel_btn = RoundedButton(row, "Cancel", self.destroy, self.theme, 100, 34)
        self.cancel_btn.pack(side="left", padx=6)

        self.delete_btn = RoundedButton(
            row,
            "Confirm",
            self.confirm,
            self.theme,
            100,
            34,
            bg_key="danger",
            hover_key="danger_hover",
            text_key="white",
        )
        self.delete_btn.pack(side="left", padx=6)

    def confirm(self):
        self.destroy()
        self.on_confirm()


class InfoPopup(BasePopup):
    def __init__(self, app, title, text, width=450, height=360):
        super().__init__(app, title, width, height)

        tk.Label(
            self.container,
            text=title,
            bg=self.theme["panel_bg"],
            fg=self.theme["text"],
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w", padx=16, pady=(14, 8))

        body = ScrolledText(
            self.container,
            wrap="word",
            font=("Segoe UI", 9),
            bg=self.theme["entry_bg"],
            fg=self.theme["text"],
            bd=0,
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.theme["border"],
            padx=10,
            pady=10,
        )
        body.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        body.insert("1.0", text)
        body.configure(state="disabled")


class ReplyEditorPopup(BasePopup):
    def __init__(self, app, rp_data, reply=None, on_save=None):
        title = "Edit Reply" if reply else "Add Reply"
        super().__init__(app, title, 620, 760)
        self.rp_data = rp_data
        self.reply = reply
        self.on_save = on_save

        content = reply["content"] if reply else ""
        who = reply["who"] if reply else "Me"
        date_written = reply["date_written"] if reply else datetime.now().strftime("%m/%d/%Y")
        label = reply["label"] if reply else ""

        tk.Label(
            self.container,
            text=title,
            bg=self.theme["panel_bg"],
            fg=self.theme["text"],
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w", padx=16, pady=(14, 10))

        form = tk.Frame(self.container, bg=self.theme["panel_bg"])
        form.pack(fill="x", padx=16)

        self.who_var = tk.StringVar(value=who)
        self.date_var = tk.StringVar(value=date_written)
        self.label_var = tk.StringVar(value=label)

        self._make_labeled_entry(form, "Whose reply", row=0)
        who_box = ttk.Combobox(
            form,
            textvariable=self.who_var,
            values=WHO_OPTIONS,
            state="readonly",
            width=16,
        )
        who_box.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=5)

        self._make_labeled_entry(form, "Reply date", row=1)
        tk.Entry(
            form,
            textvariable=self.date_var,
            bg=self.theme["entry_bg"],
            fg=self.theme["text"],
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.theme["border"],
            insertbackground=self.theme["text"],
        ).grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=5)

        self._make_labeled_entry(form, "Optional label", row=2)
        tk.Entry(
            form,
            textvariable=self.label_var,
            bg=self.theme["entry_bg"],
            fg=self.theme["text"],
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.theme["border"],
            insertbackground=self.theme["text"],
        ).grid(row=2, column=1, sticky="ew", padx=(10, 0), pady=5)

        form.grid_columnconfigure(1, weight=1)

        tk.Label(
            self.container,
            text="Reply text",
            bg=self.theme["panel_bg"],
            fg=self.theme["text"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", padx=16, pady=(12, 6))

        self.text = ScrolledText(
            self.container,
            wrap="word",
            height=14,
            font=("Segoe UI", 10),
            bg=self.theme["entry_bg"],
            fg=self.theme["text"],
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=self.theme["border"],
            padx=10,
            pady=10,
        )
        self.text.pack(fill="both", expand=True, padx=16, pady=(0, 10))
        self.text.insert("1.0", content)
        self.text.focus_set()

        button_row = tk.Frame(self.container, bg=self.theme["panel_bg"])
        button_row.pack(fill="x", side="bottom", padx=16, pady=(0, 14))

        self.save_btn = RoundedButton(
            button_row,
            "Save Reply",
            self.save_reply,
            self.theme,
            110,
            34,
            bg_key="accent",
            hover_key="accent_hover",
            text_key="white",
        )
        self.save_btn.pack(side="right")

    def _make_labeled_entry(self, master, text, row):
        tk.Label(
            master,
            text=text,
            bg=self.theme["panel_bg"],
            fg=self.theme["text"],
            font=("Segoe UI", 9, "bold"),
        ).grid(row=row, column=0, sticky="w", pady=5)

    def save_reply(self):
        content = self.text.get("1.0", "end-1c").strip()
        if not content:
            messagebox.showwarning("Reply text needed", "Please add some reply text first.")
            return

        reply_data = {
            "id": self.reply["id"] if self.reply else str(uuid4()),
            "who": self.who_var.get().strip() or "Me",
            "date_written": self.date_var.get().strip(),
            "label": self.label_var.get().strip(),
            "content": content,
            "created_at": self.reply["created_at"] if self.reply else now_iso(),
            "updated_at": now_iso(),
        }

        if self.on_save:
            self.on_save(reply_data)
        self.destroy()


class RPFormPopup(BasePopup):
    def __init__(self, app, rp_data=None, on_save=None):
        title = "Edit RP" if rp_data else "New RP"
        super().__init__(app, title, 620, 860)
        self.rp_data = rp_data
        self.on_save = on_save

        tk.Label(
            self.container,
            text=title,
            bg=self.theme["panel_bg"],
            fg=self.theme["text"],
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w", padx=16, pady=(14, 10))

        body = tk.Frame(self.container, bg=self.theme["panel_bg"])
        body.pack(fill="both", expand=True, padx=16, pady=(0, 14))

        self.vars = {
            "thread_title": tk.StringVar(value=safe_text(rp_data.get("thread_title")) if rp_data else ""),
            "turn": tk.StringVar(value=safe_text(rp_data.get("turn")) if rp_data else ""),
            "thread_type": tk.StringVar(value=safe_text(rp_data.get("thread_type")) if rp_data else ""),
            "status": tk.StringVar(value=safe_text(rp_data.get("status")) if rp_data else "Active"),
            "my_character": tk.StringVar(value=safe_text(rp_data.get("my_character")) if rp_data else ""),
            "their_character": tk.StringVar(value=safe_text(rp_data.get("their_character")) if rp_data else ""),
            "played_by": tk.StringVar(value=safe_text(rp_data.get("played_by")) if rp_data else ""),
            "ic_date": tk.StringVar(value=safe_text(rp_data.get("ic_date")) if rp_data else ""),
            "last_turn": tk.StringVar(value=safe_text(rp_data.get("last_turn")) if rp_data else ""),
            "url": tk.StringVar(value=safe_text(rp_data.get("url")) if rp_data else ""),
            "summary": tk.StringVar(value=safe_text(rp_data.get("summary")) if rp_data else ""),
        }

        fields = tk.Frame(body, bg=self.theme["panel_bg"])
        fields.pack(fill="x")

        self.make_entry(fields, "Thread Title", "thread_title", 0)
        self.make_combo(fields, "Turn", "turn", TURN_OPTIONS, 1)
        self.make_combo(fields, "Thread Type", "thread_type", THREAD_TYPES, 2)
        self.make_combo(fields, "Status", "status", STATUS_OPTIONS, 3)
        self.make_entry(fields, "My Character", "my_character", 4)
        self.make_entry(fields, "Their Character", "their_character", 5)
        self.make_entry(fields, "Played By", "played_by", 6)
        self.make_entry(fields, "IC Date", "ic_date", 7)
        self.make_entry(fields, "Last Turn", "last_turn", 8)
        self.make_entry(fields, "URL", "url", 9)
        self.make_entry(fields, "Short Summary", "summary", 10)

        tk.Label(
            body,
            text="Notes",
            bg=self.theme["panel_bg"],
            fg=self.theme["text"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", pady=(12, 6))

        self.notes_text = ScrolledText(
            body,
            wrap="word",
            height=10,
            font=("Segoe UI", 10),
            bg=self.theme["entry_bg"],
            fg=self.theme["text"],
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=self.theme["border"],
            insertbackground=self.theme["text"],
            padx=10,
            pady=10,
        )
        self.notes_text.pack(fill="both", expand=True)
        self.notes_text.insert("1.0", safe_text(rp_data.get("notes")) if rp_data else "")

        button_row = tk.Frame(self.container, bg=self.theme["panel_bg"])
        button_row.pack(fill="x", padx=16, pady=(0, 14))

        save_btn = RoundedButton(
            button_row,
            "Save RP",
            self.save_rp,
            self.theme,
            100,
            34,
            bg_key="accent",
            hover_key="accent_hover",
            text_key="white",
        )
        save_btn.pack(side="right")

    def make_entry(self, master, label, key, row):
        tk.Label(
            master,
            text=label,
            bg=self.theme["panel_bg"],
            fg=self.theme["text"],
            font=("Segoe UI", 9, "bold"),
        ).grid(row=row, column=0, sticky="w", pady=5)
        entry = tk.Entry(
            master,
            textvariable=self.vars[key],
            bg=self.theme["entry_bg"],
            fg=self.theme["text"],
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.theme["border"],
            insertbackground=self.theme["text"],
        )
        entry.grid(row=row, column=1, sticky="ew", padx=(10, 0), pady=5)
        master.grid_columnconfigure(1, weight=1)

    def make_combo(self, master, label, key, values, row):
        tk.Label(
            master,
            text=label,
            bg=self.theme["panel_bg"],
            fg=self.theme["text"],
            font=("Segoe UI", 9, "bold"),
        ).grid(row=row, column=0, sticky="w", pady=5)
        combo = ttk.Combobox(master, textvariable=self.vars[key], values=values, state="readonly")
        combo.grid(row=row, column=1, sticky="ew", padx=(10, 0), pady=5)
        master.grid_columnconfigure(1, weight=1)

    def save_rp(self):
        title = self.vars["thread_title"].get().strip()
        if not title:
            messagebox.showwarning("Thread title needed", "Please give the RP a thread title.")
            return

        old = self.rp_data or {}
        rp = {
            "id": old.get("id", str(uuid4())),
            "thread_title": title,
            "turn": self.vars["turn"].get().strip(),
            "thread_type": self.vars["thread_type"].get().strip(),
            "status": self.vars["status"].get().strip() or "Active",
            "my_character": self.vars["my_character"].get().strip(),
            "their_character": self.vars["their_character"].get().strip(),
            "played_by": self.vars["played_by"].get().strip(),
            "ic_date": self.vars["ic_date"].get().strip(),
            "last_turn": self.vars["last_turn"].get().strip(),
            "url": self.vars["url"].get().strip(),
            "summary": self.vars["summary"].get().strip(),
            "notes": self.notes_text.get("1.0", "end-1c").strip(),
            "replies": old.get("replies", []),
            "created_at": old.get("created_at", now_iso()),
            "updated_at": now_iso(),
        }

        if self.on_save:
            self.on_save(rp)
        self.destroy()


class ReplyCard(tk.Frame):
    def __init__(self, master, app, reply, on_edit=None, on_delete=None):
        bg = app.theme["reply_right"] if reply.get("who") == "Me" else app.theme["reply_left"]
        super().__init__(
            master,
            bg=bg,
            highlightthickness=1,
            highlightbackground=app.theme["border"],
            bd=0,
        )
        self.app = app
        self.reply = reply
        self.on_edit = on_edit
        self.on_delete = on_delete

        top = tk.Frame(self, bg=bg)
        top.pack(fill="x", padx=10, pady=(8, 4))

        who = reply.get("who", "Me")
        label = reply.get("label", "").strip()
        top_text = who if not label else f"{who} • {label}"

        tk.Label(
            top,
            text=top_text,
            bg=bg,
            fg=app.theme["text"],
            font=("Segoe UI", 9, "bold"),
        ).pack(side="left")

        tk.Label(
            top,
            text=reply.get("date_written", ""),
            bg=bg,
            fg=app.theme["timestamp"],
            font=("Segoe UI", 8),
        ).pack(side="right")

        content = tk.Label(
            self,
            text=reply.get("content", ""),
            justify="left",
            anchor="w",
            wraplength=700,
            bg=bg,
            fg=app.theme["text"],
            font=("Segoe UI", 9),
        )
        content.pack(fill="x", padx=10, pady=(0, 6))

        bottom = tk.Frame(self, bg=bg)
        bottom.pack(fill="x", padx=10, pady=(0, 8))

        edit = tk.Label(
            bottom,
            text="Edit",
            bg=bg,
            fg=app.theme["muted"],
            cursor="hand2",
            font=("Segoe UI", 8, "underline"),
        )
        edit.pack(side="left")
        edit.bind("<Button-1>", lambda e: self.on_edit() if self.on_edit else None)

        delete = tk.Label(
            bottom,
            text="Delete",
            bg=bg,
            fg=app.theme["muted"],
            cursor="hand2",
            font=("Segoe UI", 8, "underline"),
        )
        delete.pack(side="left", padx=(12, 0))
        delete.bind("<Button-1>", lambda e: self.on_delete() if self.on_delete else None)


class RPDetailWindow(tk.Toplevel):
    def __init__(self, app, rp_id):
        super().__init__(app.root)
        self.app = app
        self.rp_id = rp_id
        self.theme = app.theme
        self.title(f"{APP_NAME} — RP Details")
        self.geometry("980x840")
        self.minsize(860, 640)
        self.configure(bg=self.theme["window_bg"])

        if self.app.app_icon:
            try:
                self.iconphoto(True, self.app.app_icon)
            except Exception:
                pass

        outer = tk.Frame(self, bg=self.theme["window_bg"])
        outer.pack(fill="both", expand=True, padx=14, pady=14)

        header = tk.Frame(
            outer,
            bg=self.theme["header_bg"],
            highlightthickness=1,
            highlightbackground=self.theme["border"],
        )
        header.pack(fill="x", pady=(0, 12))

        self.header_title = tk.Label(
            header,
            text="RP Details",
            bg=self.theme["header_bg"],
            fg=self.theme["text"],
            font=("Segoe UI", 12, "bold"),
        )
        self.header_title.pack(side="left", padx=14, pady=12)

        header_buttons = tk.Frame(header, bg=self.theme["header_bg"])
        header_buttons.pack(side="right", padx=12)

        self.edit_btn = RoundedButton(
            header_buttons,
            "Edit RP",
            self.edit_rp,
            self.theme,
            90,
            34,
        )
        self.edit_btn.pack(side="left", padx=4)

        self.open_url_btn = RoundedButton(
            header_buttons,
            "Open URL",
            self.open_url,
            self.theme,
            95,
            34,
            bg_key="accent",
            hover_key="accent_hover",
            text_key="white",
        )
        self.open_url_btn.pack(side="left", padx=4)

        content = tk.Frame(outer, bg=self.theme["window_bg"])
        content.pack(fill="both", expand=True)

        left = tk.Frame(
            content,
            bg=self.theme["panel_bg"],
            highlightthickness=1,
            highlightbackground=self.theme["border"],
            width=480,
        )
        left.pack(side="left", fill="both", expand=True, padx=(0, 6))
        left.pack_propagate(False)

        right = tk.Frame(
            content,
            bg=self.theme["panel_bg"],
            highlightthickness=1,
            highlightbackground=self.theme["border"],
            width=500,
        )
        right.pack(side="left", fill="both", expand=True, padx=(6, 0))
        right.pack_propagate(False)

        self.build_left(left)
        self.build_right(right)
        self.refresh()

    def build_left(self, parent):
        tk.Label(
            parent,
            text="RP Info",
            bg=self.theme["panel_bg"],
            fg=self.theme["text"],
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w", padx=14, pady=(14, 8))

        self.info_holder = tk.Frame(parent, bg=self.theme["panel_bg"])
        self.info_holder.pack(fill="x", padx=14)

        tk.Label(
            parent,
            text="Notes",
            bg=self.theme["panel_bg"],
            fg=self.theme["text"],
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w", padx=14, pady=(14, 6))

        self.notes_box = ScrolledText(
            parent,
            wrap="word",
            font=("Segoe UI", 9),
            bg=self.theme["entry_bg"],
            fg=self.theme["text"],
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=self.theme["border"],
            padx=10,
            pady=10,
            height=18,
        )
        self.notes_box.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        self.notes_box.configure(state="disabled")

    def build_right(self, parent):
        top = tk.Frame(parent, bg=self.theme["panel_bg"])
        top.pack(fill="x", padx=14, pady=(14, 8))

        tk.Label(
            top,
            text="Replies",
            bg=self.theme["panel_bg"],
            fg=self.theme["text"],
            font=("Segoe UI", 11, "bold"),
        ).pack(side="left")

        self.add_reply_btn = RoundedButton(
            top,
            "+ Add Reply",
            self.add_reply,
            self.theme,
            105,
            34,
            bg_key="accent",
            hover_key="accent_hover",
            text_key="white",
        )
        self.add_reply_btn.pack(side="right")

        list_wrap = tk.Frame(parent, bg=self.theme["panel_bg"])
        list_wrap.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        self.reply_canvas = tk.Canvas(
            list_wrap,
            bg=self.theme["panel_bg"],
            highlightthickness=0,
            bd=0,
        )
        self.reply_scroll = tk.Scrollbar(list_wrap, orient="vertical", command=self.reply_canvas.yview)
        self.reply_inner = tk.Frame(self.reply_canvas, bg=self.theme["panel_bg"])

        self.reply_inner.bind(
            "<Configure>",
            lambda e: self.reply_canvas.configure(scrollregion=self.reply_canvas.bbox("all"))
        )

        self.reply_canvas.create_window((0, 0), window=self.reply_inner, anchor="nw")
        self.reply_canvas.configure(yscrollcommand=self.reply_scroll.set)

        self.reply_canvas.pack(side="left", fill="both", expand=True)
        self.reply_scroll.pack(side="right", fill="y")

        self.reply_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        try:
            self.reply_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except Exception:
            pass

    def get_rp(self):
        return self.app.get_rp_by_id(self.rp_id)

    def refresh(self):
        rp = self.get_rp()
        if not rp:
            self.destroy()
            return

        self.header_title.configure(text=rp.get("thread_title", "RP Details"))

        for child in self.info_holder.winfo_children():
            child.destroy()

        rows = [
            ("Turn", rp.get("turn", "")),
            ("Thread Type", rp.get("thread_type", "")),
            ("Status", rp.get("status", "")),
            ("My Character", rp.get("my_character", "")),
            ("Their Character", rp.get("their_character", "")),
            ("Played By", rp.get("played_by", "")),
            ("IC Date", rp.get("ic_date", "")),
            ("Last Turn", rp.get("last_turn", "")),
            ("URL", rp.get("url", "")),
            ("Summary", rp.get("summary", "")),
        ]

        for i, (label, value) in enumerate(rows):
            tk.Label(
                self.info_holder,
                text=label,
                bg=self.theme["panel_bg"],
                fg=self.theme["muted"],
                font=("Segoe UI", 8, "bold"),
                anchor="w",
            ).grid(row=i, column=0, sticky="nw", pady=4)
            tk.Label(
                self.info_holder,
                text=value or "—",
                bg=self.theme["panel_bg"],
                fg=self.theme["text"],
                font=("Segoe UI", 9),
                anchor="w",
                justify="left",
                wraplength=280,
            ).grid(row=i, column=1, sticky="nw", padx=(10, 0), pady=4)

        self.info_holder.grid_columnconfigure(1, weight=1)

        self.notes_box.configure(state="normal")
        self.notes_box.delete("1.0", "end")
        self.notes_box.insert("1.0", rp.get("notes", ""))
        self.notes_box.configure(state="disabled")

        for child in self.reply_inner.winfo_children():
            child.destroy()

        replies = sorted(
            rp.get("replies", []),
            key=lambda r: (r.get("updated_at", ""), r.get("created_at", "")),
            reverse=True,
        )

        if not replies:
            tk.Label(
                self.reply_inner,
                text="No replies logged yet.\nUse + Add Reply to start tracking both sides.",
                bg=self.theme["panel_bg"],
                fg=self.theme["muted"],
                font=("Segoe UI", 10),
                justify="center",
            ).pack(fill="both", expand=True, pady=30)
        else:
            for reply in replies:
                card = ReplyCard(
                    self.reply_inner,
                    self.app,
                    reply,
                    on_edit=lambda r=reply: self.edit_reply(r),
                    on_delete=lambda r=reply: self.delete_reply(r),
                )
                card.pack(fill="x", padx=2, pady=6)

        self.reply_canvas.update_idletasks()
        self.reply_canvas.configure(scrollregion=self.reply_canvas.bbox("all"))

    def add_reply(self):
        rp = self.get_rp()
        if not rp:
            return

        def save_reply(reply_data):
            rp["replies"].append(reply_data)
            self.app.sync_rp_from_replies(rp)
            self.app.save_data()
            self.refresh()
            self.app.refresh_rp_list()

        ReplyEditorPopup(self.app, rp, reply=None, on_save=save_reply)

    def edit_reply(self, reply):
        rp = self.get_rp()
        if not rp:
            return

        def save_reply(reply_data):
            for i, existing in enumerate(rp["replies"]):
                if existing["id"] == reply["id"]:
                    rp["replies"][i] = reply_data
                    break
            self.app.sync_rp_from_replies(rp)
            self.app.save_data()
            self.refresh()
            self.app.refresh_rp_list()

        ReplyEditorPopup(self.app, rp, reply=reply, on_save=save_reply)

    def delete_reply(self, reply):
        rp = self.get_rp()
        if not rp:
            return

        def do_delete():
            rp["replies"] = [r for r in rp["replies"] if r["id"] != reply["id"]]
            self.app.sync_rp_from_replies(rp)
            self.app.save_data()
            self.refresh()
            self.app.refresh_rp_list()

        ConfirmPopup(self.app, "Delete reply?", "This reply will be removed.", do_delete)

    def edit_rp(self):
        rp = self.get_rp()
        if not rp:
            return

        def save_rp(updated_rp):
            self.app.upsert_rp(updated_rp)
            self.refresh()

        RPFormPopup(self.app, rp_data=rp, on_save=save_rp)

    def open_url(self):
        rp = self.get_rp()
        if not rp:
            return
        url = rp.get("url", "").strip()
        if not url:
            messagebox.showinfo("No URL", "This RP does not have a URL yet.")
            return
        webbrowser.open(url)


class RPCard(tk.Frame):
    def __init__(self, master, app, rp_data, width=380, height=138):
        super().__init__(master, bg=app.theme["panel_bg"], bd=0, highlightthickness=0)
        self.app = app
        self.rp = rp_data
        self.width_v = width
        self.height_v = height
        self.hovered = False

        self.canvas = tk.Canvas(
            self,
            width=width,
            height=height,
            bg=app.theme["panel_bg"],
            highlightthickness=0,
            bd=0,
            cursor="hand2",
        )
        self.canvas.pack(fill="x", expand=True)

        self.canvas.bind("<Enter>", lambda e: self.set_hover(True))
        self.canvas.bind("<Leave>", lambda e: self.set_hover(False))
        self.canvas.bind("<Button-1>", self.handle_click)
        self.redraw()

    def set_hover(self, value):
        self.hovered = value
        self.redraw()

    def status_color(self):
        status = self.rp.get("status", "")
        if status == "Complete":
            return self.app.theme["button_bg"]
        if status == "Waiting on Me":
            return self.app.theme["danger"]
        if status == "Waiting on Them":
            return self.app.theme["accent"]
        return self.app.theme["border"]

    def redraw(self):
        t = self.app.theme
        self.canvas.delete("all")

        self.canvas.create_polygon(
            rounded_rect_points(4, 4, self.width_v - 4, self.height_v - 4, 20),
            smooth=True,
            fill=t["card_hover"] if self.hovered else t["card_bg"],
            outline=t["border"],
            width=1.2,
        )

        self.canvas.create_rectangle(12, 14, 20, self.height_v - 14, fill=self.status_color(), outline="")

        title = compact(self.rp.get("thread_title", ""), 38) or "Untitled RP"
        summary = compact(self.rp.get("summary", ""), 70)
        my_char = self.rp.get("my_character", "") or "—"
        their_char = self.rp.get("their_character", "") or "—"
        played_by = self.rp.get("played_by", "") or "—"
        status = self.rp.get("status", "") or "—"
        replies_count = len(self.rp.get("replies", []))
        turn = self.rp.get("turn", "") or "—"
        thread_type = self.rp.get("thread_type", "") or "—"
        last_turn = self.rp.get("last_turn", "") or "—"

        self.canvas.create_text(
            32, 14,
            anchor="nw",
            text=title,
            fill=t["text"],
            font=("Segoe UI", 10, "bold"),
            width=self.width_v - 80,
        )

        info_line = f"{turn} • {thread_type} • {status}"
        self.canvas.create_text(
            32, 38,
            anchor="nw",
            text=info_line,
            fill=t["muted"],
            font=("Segoe UI", 8, "bold"),
        )

        self.canvas.create_text(
            32, 60,
            anchor="nw",
            text=f"{my_char} × {their_char}",
            fill=t["text"],
            font=("Segoe UI", 9),
            width=self.width_v - 52,
        )

        self.canvas.create_text(
            32, 82,
            anchor="nw",
            text=f"Played by: {played_by}",
            fill=t["muted"],
            font=("Segoe UI", 8),
            width=self.width_v - 52,
        )

        extra = summary if summary else f"Replies: {replies_count} • Last Turn: {last_turn}"
        self.canvas.create_text(
            32, 100,
            anchor="nw",
            text=extra,
            fill=t["text"],
            font=("Segoe UI", 8),
            width=self.width_v - 52,
        )

        self.canvas.create_text(
            self.width_v - 16,
            self.height_v - 14,
            anchor="se",
            text=f"{replies_count} repl{'y' if replies_count == 1 else 'ies'}",
            fill=t["timestamp"],
            font=("Segoe UI", 8),
        )

        if self.hovered:
            self.canvas.create_text(
                self.width_v - 16,
                16,
                anchor="ne",
                text="✎",
                fill=t["muted"],
                font=("Segoe UI", 10),
                tags=("edit",),
            )

    def handle_click(self, _event=None):
        current = self.canvas.find_withtag("current")
        if current:
            tags = self.canvas.gettags(current[0])
            if "edit" in tags:
                self.app.open_edit_rp_popup(self.rp["id"])
                return
        self.app.open_rp_detail(self.rp["id"])


class RPTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_NAME} {APP_VERSION}")
        self.root.geometry(DEFAULT_GEOMETRY)
        self.root.minsize(MIN_WIDTH, MIN_HEIGHT)

        DATA_DIR.mkdir(parents=True, exist_ok=True)

        self.theme_key = "matcha"
        self.theme = MATCHA_THEME
        self.settings = {}
        self.rps = []
        self.app_icon = None
        self.header_icon = None
        self.detail_windows = {}

        self.load_settings()
        self.load_data()
        self.load_icon()
        self.build_ui()
        self.apply_theme()

    def load_icon(self):
        try:
            if ICON_ICO.exists():
                self.root.iconbitmap(str(ICON_ICO))
        except Exception:
            pass
        chosen = None
        for name in POSSIBLE_ICON_NAMES:
            path = BASE_DIR / name
            if path.exists():
                chosen = path
                break

        if chosen:
            try:
                self.app_icon = tk.PhotoImage(file=str(chosen))
                self.root.iconphoto(True, self.app_icon)
                self.header_icon = self.app_icon.subsample(10, 10)
            except Exception:
                self.app_icon = None
                self.header_icon = None

    def load_settings(self):
        if SETTINGS_PATH.exists():
            try:
                self.settings = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
            except Exception:
                self.settings = {}

        self.theme_key = self.settings.get("theme", "matcha")
        self.theme = MATCHA_THEME if self.theme_key == "matcha" else THAI_TEA_THEME

    def save_settings(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.settings["theme"] = self.theme_key
        SETTINGS_PATH.write_text(json.dumps(self.settings, indent=2), encoding="utf-8")

    def starter_rp(self):
        return {
            "id": str(uuid4()),
            "thread_title": "Starter RP",
            "turn": "Mine",
            "thread_type": "Thread",
            "status": "Active",
            "my_character": "Your Character",
            "their_character": "Their Character",
            "played_by": "Partner Alias",
            "ic_date": "",
            "last_turn": datetime.now().strftime("%m/%d/%Y"),
            "url": "",
            "summary": "Click to open the full tracker window.",
            "notes": (
                "Use this app like a compact RP hub.\n\n"
                "• Main screen stays small and tidy.\n"
                "• Click an RP to open the full detail window.\n"
                "• Save plot notes, URLs, dates, and tracker details.\n"
                "• Log both sides of replies in order.\n"
                "• Change theme from the three-dot menu."
            ),
            "replies": [
                {
                    "id": str(uuid4()),
                    "who": "Me",
                    "date_written": datetime.now().strftime("%m/%d/%Y"),
                    "label": "Example",
                    "content": "You can keep starter snippets, last responses, or quick draft notes here.",
                    "created_at": now_iso(),
                    "updated_at": now_iso(),
                }
            ],
            "created_at": now_iso(),
            "updated_at": now_iso(),
        }

    def load_data(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if RPS_PATH.exists():
            try:
                payload = json.loads(RPS_PATH.read_text(encoding="utf-8"))
                self.rps = payload.get("rps", [])
            except Exception:
                self.rps = []

        if not self.rps:
            self.rps = [self.starter_rp()]
            self.save_data()

    def save_data(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        payload = {"rps": self.rps}
        RPS_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    def build_ui(self):
        self.outer = tk.Frame(self.root, bg=self.theme["window_bg"])
        self.outer.pack(fill="both", expand=True)

        self.header = tk.Frame(self.outer, bg=self.theme['header_bg'], height=80)
        self.header.pack(fill='x', side='top')
        self.header.pack_propagate(False)

        self.header_inner = tk.Frame(self.header, bg=self.theme['header_inner'])
        self.header_inner.pack(fill='x', padx=14, pady=10)

        self.title_row = tk.Frame(self.header_inner, bg=self.theme['header_inner'])
        self.title_row.pack(fill='x', padx=10, pady=12)

        self.icon_label = tk.Label(self.title_row, bg=self.theme['header_inner'], bd=0)
        #self.icon_label.pack(side='left', padx=(0, 8))

        self.title_label = tk.Label(
        self.title_row,
        text='🧋',
        font=('Segoe UI Emoji', 20),
        bd=0,
        bg=self.theme['header_inner'],
        fg=self.theme['text']
     )
        self.title_label.pack(side='left', padx=(190, 0), pady=4)

        self.menu_button = tk.Button(
        self.title_row,
    text='Menu', 
    font=('Verdana', 8,),
    bd=0,
    relief='flat',
    width=8,
    cursor='hand2',
    command=self.show_menu
)
        self.menu_button.pack(side='right')

        self.controls = tk.Frame(self.outer, bg=self.theme["window_bg"])
        self.controls.pack(fill="x", padx=16, pady=(14, 8))

        self.filter_var = tk.StringVar(value="All")
        self.search_var = tk.StringVar()

        tk.Label(
            self.controls,
            text="Filter",
            bg=self.theme["window_bg"],
            fg=self.theme["text"],
            font=("Segoe UI", 9, "bold"),
        ).pack(side="left")

        self.filter_combo = ttk.Combobox(
            self.controls,
            textvariable=self.filter_var,
            values=["All"] + STATUS_OPTIONS,
            state="readonly",
            width=16,
        )
        self.filter_combo.pack(side="left", padx=(8, 10))
        self.filter_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_rp_list())

        tk.Label(
            self.controls,
            text="Search",
            bg=self.theme["window_bg"],
            fg=self.theme["text"],
            font=("Segoe UI", 9, "bold"),
        ).pack(side="left")

        self.search_entry = tk.Entry(
            self.controls,
            textvariable=self.search_var,
            bg=self.theme["entry_bg"],
            fg=self.theme["text"],
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.theme["border"],
            insertbackground=self.theme["text"],
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(8, 0))
        self.search_var.trace_add("write", lambda *args: self.refresh_rp_list())

        self.main = tk.Frame(self.outer, bg=self.theme["window_bg"])
        self.main.pack(fill="both", expand=True, padx=16, pady=(0, 12))

        self.list_shell = tk.Frame(
            self.main,
            bg=self.theme["panel_bg"],
            highlightthickness=1,
            highlightbackground=self.theme["border"],
        )
        self.list_shell.pack(fill="both", expand=True)

        self.list_canvas = tk.Canvas(
            self.list_shell,
            bg=self.theme["panel_bg"],
            highlightthickness=0,
            bd=0,
        )
        self.list_scroll = tk.Scrollbar(self.list_shell, orient="vertical", command=self.list_canvas.yview)
        self.list_inner = tk.Frame(self.list_canvas, bg=self.theme["panel_bg"])

        self.list_inner.bind(
            "<Configure>",
            lambda e: self.list_canvas.configure(scrollregion=self.list_canvas.bbox("all"))
        )

        self.list_canvas.create_window((0, 0), window=self.list_inner, anchor="nw")
        self.list_canvas.configure(yscrollcommand=self.list_scroll.set)

        self.list_canvas.pack(side="left", fill="both", expand=True)
        self.list_scroll.pack(side="right", fill="y")

        self.button_row = tk.Frame(self.outer, bg=self.theme["window_bg"])
        self.button_row.pack(fill="x", padx=16, pady=(0, 16))

        self.new_rp_btn = RoundedButton(
            self.button_row,
            "+ New RP",
            self.open_new_rp_popup,
            self.theme,
            126,
            38,
            bg_key="accent",
            hover_key="accent_hover",
            text_key="white",
        )
        self.new_rp_btn.pack(side="left")

        self.delete_btn = RoundedButton(
            self.button_row,
            "Delete RP",
            self.delete_selected_prompt,
            self.theme,
            110,
            38,
            bg_key="danger",
            hover_key="danger_hover",
            text_key="white",
        )
        self.delete_btn.pack(side="right")

        self.selected_rp_id = None
        self.list_canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def on_mousewheel(self, event):
        try:
            self.list_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except Exception:
            pass

    def apply_theme(self):
        t = self.theme
        self.root.configure(bg=t["window_bg"])
        self.outer.configure(bg=t["window_bg"])
        self.header.configure(bg=t["header_bg"])
        self.header_inner.configure(bg=t["header_inner"])
        self.title_row.configure(bg=t["header_inner"])
        self.title_label.configure(bg=t["header_inner"], fg=t["text"])
        self.menu_button.configure(
        bg=t['button_bg'],
        fg=t['text'],
        activebackground=t['button_hover'],
       activeforeground=t['text'],
        relief='flat',
        padx=6,
        pady=2
    )
        self.controls.configure(bg=t["window_bg"])
        self.main.configure(bg=t["window_bg"])
        self.list_shell.configure(bg=t["panel_bg"], highlightbackground=t["border"])
        self.list_canvas.configure(bg=t["panel_bg"])
        self.list_inner.configure(bg=t["panel_bg"])
        self.button_row.configure(bg=t["window_bg"])
        self.search_entry.configure(
            bg=t["entry_bg"],
            fg=t["text"],
            highlightbackground=t["border"],
            insertbackground=t["text"],
        )

        for widget in self.controls.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(bg=t["window_bg"], fg=t["text"])

        self.new_rp_btn.update_theme(t)
        self.delete_btn.update_theme(t)

        if self.header_icon:
            self.icon_label.configure(image=self.header_icon, text="", bg=t["header_inner"])
            self.icon_label.image = self.header_icon
        else:
            self.icon_label.configure(text="🧋", image="", font=("Segoe UI Emoji", 13), bg=t["header_inner"], fg=t["text"])

        for win in list(self.detail_windows.values()):
            try:
                win.destroy()
            except Exception:
                pass
        self.detail_windows.clear()

        self.refresh_rp_list()

    def change_theme(self, theme_key):
        self.theme_key = theme_key
        self.theme = MATCHA_THEME if theme_key == "matcha" else THAI_TEA_THEME
        self.save_settings()
        self.apply_theme()

    def show_menu(self):
        menu = tk.Menu(
            self.root,
            tearoff=0,
            bg=self.theme["menu_bg"],
            fg=self.theme["text"],
            activebackground=self.theme["menu_active"],
            activeforeground=self.theme["text"],
            relief="flat",
            bd=1,
            font=("Segoe UI", 9),
        )

        theme_menu = tk.Menu(
            menu,
            tearoff=0,
            bg=self.theme["menu_bg"],
            fg=self.theme["text"],
            activebackground=self.theme["menu_active"],
            activeforeground=self.theme["text"],
            relief="flat",
            bd=1,
            font=("Segoe UI", 9),
        )
        theme_menu.add_command(label="Matcha", command=lambda: self.change_theme("matcha"))
        theme_menu.add_command(label="Thai Tea", command=lambda: self.change_theme("thai_tea"))

        menu.add_command(label="Help", command=self.show_help)
        menu.add_command(label="About", command=self.show_about)
        menu.add_separator()
        menu.add_cascade(label="Change Theme", menu=theme_menu)

        menu.tk_popup(
            self.menu_button.winfo_rootx(),
            self.menu_button.winfo_rooty() + self.menu_button.winfo_height(),
        )

    def show_help(self):
        text = (
            "How to use the RP Tracker:\n\n"
            "• The main window is the compact overview.\n"
            "• Click + New RP to add a new thread.\n"
            "• Click any RP card to open the full detail window.\n"
            "• The detail window stores all the tracker info, notes, and replies.\n"
            "• Use replies to keep both sides' posts in order.\n"
            "• Search and filter from the main window.\n"
            "• Open URL will launch the saved thread link in your browser.\n\n"
            "This version keeps the main screen small on purpose so the actual long stuff lives inside each RP window."
        )
        InfoPopup(self, "Help", text, 470, 360)

    def show_about(self):
        text = (
            f"{APP_NAME} {APP_VERSION}\n\n"
            "A small desktop RP tracker made in a cozy BobaNote-style layout.\n"
            "Compact outside. Detailed inside.\n\n"
            "Built to track:\n"
            "• thread info\n"
            "• notes and summaries\n"
            "• both parties' replies\n"
            "• links and dates"
        )
        InfoPopup(self, "About", text, 420, 280)

    def get_rp_by_id(self, rp_id):
        return next((rp for rp in self.rps if rp["id"] == rp_id), None)

    def get_last_reply(self, rp):
        replies = rp.get("replies", [])
        if not replies:
            return None
        return max(replies, key=lambda r: (r.get("updated_at", ""), r.get("created_at", "")))

    def sync_rp_from_replies(self, rp):
        rp["updated_at"] = now_iso()
        last_reply = self.get_last_reply(rp)
        if not last_reply:
            return

        who = safe_text(last_reply.get("who")).strip() or "Me"
        rp["last_turn"] = reply_date_or_today(last_reply.get("date_written"))

        current_status = safe_text(rp.get("status")).strip()
        if current_status not in {"Archived", "On Hold", "Complete"}:
            if who == "Me":
                rp["status"] = "Waiting on Them"
                rp["turn"] = "Theirs"
            else:
                rp["status"] = "Waiting on Me"
                rp["turn"] = "Mine"

    def upsert_rp(self, rp_data):
        existing = self.get_rp_by_id(rp_data["id"])
        if existing:
            idx = self.rps.index(existing)
            self.rps[idx] = rp_data
        else:
            self.rps.insert(0, rp_data)

        self.save_data()
        self.refresh_rp_list()

        if rp_data["id"] in self.detail_windows:
            window = self.detail_windows[rp_data["id"]]
            try:
                window.refresh()
            except Exception:
                pass

    def open_new_rp_popup(self):
        RPFormPopup(self, rp_data=None, on_save=self.upsert_rp)

    def open_edit_rp_popup(self, rp_id):
        rp = self.get_rp_by_id(rp_id)
        if not rp:
            return
        RPFormPopup(self, rp_data=rp, on_save=self.upsert_rp)

    def open_rp_detail(self, rp_id):
        self.selected_rp_id = rp_id
        if rp_id in self.detail_windows:
            try:
                self.detail_windows[rp_id].lift()
                self.detail_windows[rp_id].focus_force()
                self.detail_windows[rp_id].refresh()
                return
            except Exception:
                self.detail_windows.pop(rp_id, None)

        win = RPDetailWindow(self, rp_id)
        self.detail_windows[rp_id] = win

        def cleanup():
            self.detail_windows.pop(rp_id, None)
            try:
                win.destroy()
            except Exception:
                pass

        win.protocol("WM_DELETE_WINDOW", cleanup)

    def filtered_rps(self):
        query = self.search_var.get().strip().lower()
        filter_status = self.filter_var.get().strip()

        rps = self.rps[:]
        if filter_status == "Archived":
            rps = [rp for rp in rps if rp.get("status", "") == "Archived"]
        elif filter_status and filter_status != "All":
            rps = [rp for rp in rps if rp.get("status", "") == filter_status and rp.get("status", "") != "Archived"]
        else:
            rps = [rp for rp in rps if rp.get("status", "") != "Archived"]

        if query:
            def matches(rp):
                hay = " ".join([
                    rp.get("thread_title", ""),
                    rp.get("my_character", ""),
                    rp.get("their_character", ""),
                    rp.get("played_by", ""),
                    rp.get("summary", ""),
                    rp.get("notes", ""),
                ]).lower()
                return query in hay

            rps = [rp for rp in rps if matches(rp)]

        rps.sort(key=lambda rp: rp.get("updated_at", ""), reverse=True)
        return rps

    def refresh_rp_list(self):
        for child in self.list_inner.winfo_children():
            child.destroy()

        rps = self.filtered_rps()
        if not rps:
            tk.Label(
                self.list_inner,
                text="No RPs matched this filter.\nTry a different search or make a new one.",
                bg=self.theme["panel_bg"],
                fg=self.theme["muted"],
                font=("Segoe UI", 10),
                justify="center",
            ).pack(fill="both", expand=True, pady=30)
            return

        for rp in rps:
            row = tk.Frame(self.list_inner, bg=self.theme["panel_bg"])
            row.pack(fill="x", padx=10, pady=6)

            card = RPCard(row, self, rp, width=410, height=138)
            card.pack(fill="x")

            select_row = tk.Frame(row, bg=self.theme["panel_bg"])
            select_row.pack(fill="x", pady=(4, 0))

            select_label = tk.Label(
                select_row,
                text="Select",
                bg=self.theme["panel_bg"],
                fg=self.theme["muted"],
                cursor="hand2",
                font=("Segoe UI", 8, "underline"),
            )
            select_label.pack(anchor="e")
            select_label.bind("<Button-1>", lambda e, rp_id=rp["id"]: self.select_rp(rp_id))

        self.list_canvas.update_idletasks()
        self.list_canvas.configure(scrollregion=self.list_canvas.bbox("all"))

    def select_rp(self, rp_id):
        self.selected_rp_id = rp_id
        rp = self.get_rp_by_id(rp_id)
        if rp:
            self.root.title(f"{APP_NAME} {APP_VERSION} — Selected: {rp.get('thread_title', 'RP')}")

    def delete_selected_prompt(self):
        if not self.selected_rp_id:
            messagebox.showinfo("No RP selected", "Use the small Select link under a card first.")
            return

        rp = self.get_rp_by_id(self.selected_rp_id)
        if not rp:
            messagebox.showinfo("Not found", "That RP could not be found.")
            return

        def do_delete():
            self.rps = [item for item in self.rps if item["id"] != self.selected_rp_id]
            self.save_data()
            if self.selected_rp_id in self.detail_windows:
                try:
                    self.detail_windows[self.selected_rp_id].destroy()
                except Exception:
                    pass
                self.detail_windows.pop(self.selected_rp_id, None)
            self.selected_rp_id = None
            self.root.title(f"{APP_NAME} {APP_VERSION}")
            self.refresh_rp_list()

        ConfirmPopup(self, "Delete RP?", f'"{rp.get("thread_title", "This RP")}" will be removed.', do_delete)


def main():
    root = tk.Tk()
    app = RPTrackerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()