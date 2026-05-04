# -*- coding: utf-8 -*-
"""
Home Screen — main window of the Fasal Rin Automation Suite launcher.

Shows 4 tool cards with:
  - Icon + name + description
  - Price (fetched live from Supabase)
  - Install status badge
  - Download / Open button with progress bar
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import webbrowser

from license_config import TOOLS, CURRENT_VERSION
import tool_manager as tm

# ── Colour palette ────────────────────────────────────────────────────────────
CLR_BG       = "#f4f6fb"
CLR_HEADER   = "#1a1a2e"
CLR_CARD     = "#ffffff"
CLR_BORDER   = "#d0d7e3"
CLR_GREEN    = "#27ae60"
CLR_BLUE     = "#2980b9"
CLR_ORANGE   = "#e67e22"
CLR_RED      = "#e74c3c"
CLR_GRAY     = "#95a5a6"
CLR_TEXT     = "#2c3e50"
CLR_SUBTEXT  = "#7f8c8d"


class HomeScreen:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Fasal Rin Automation Suite")
        self.root.geometry("860x680")
        self.root.minsize(780, 560)
        self.root.configure(bg=CLR_BG)

        self._cards = {}   # slug -> dict of widget refs
        self._build_ui()
        # Fetch prices + latest version info in background
        threading.Thread(target=self._load_all_tool_info, daemon=True).start()

    # ── UI Construction ───────────────────────────────────────────────────────

    def _build_ui(self):
        # Header
        hdr = tk.Frame(self.root, bg=CLR_HEADER, height=70)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        tk.Label(
            hdr,
            text="\U0001f33e  Fasal Rin Automation Suite",
            font=("Segoe UI", 18, "bold"),
            fg="white",
            bg=CLR_HEADER,
        ).pack(side="left", padx=24, expand=False)

        tk.Label(
            hdr,
            text=f"v{CURRENT_VERSION}",
            font=("Segoe UI", 9),
            fg="#aaa",
            bg=CLR_HEADER,
        ).pack(side="right", padx=16, anchor="s", pady=8)

        # Subtitle strip
        sub = tk.Frame(self.root, bg="#16213e", height=32)
        sub.pack(fill="x")
        sub.pack_propagate(False)
        tk.Label(
            sub,
            text="Select a tool below to download or open it.",
            font=("Segoe UI", 9),
            fg="#aaa",
            bg="#16213e",
        ).pack(side="left", padx=24)

        # Scrollable body
        body_wrap = tk.Frame(self.root, bg=CLR_BG)
        body_wrap.pack(fill="both", expand=True, pady=16, padx=16)

        canvas = tk.Canvas(body_wrap, bg=CLR_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(body_wrap, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self._inner = tk.Frame(canvas, bg=CLR_BG)
        win_id = canvas.create_window((0, 0), window=self._inner, anchor="nw")

        def _on_inner(e=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def _on_canvas(e=None):
            canvas.itemconfig(win_id, width=e.width)

        self._inner.bind("<Configure>", _on_inner)
        canvas.bind("<Configure>", _on_canvas)
        canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        self.root.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        # Build one card per tool
        for tool in TOOLS:
            self._build_card(self._inner, tool)

        # Footer
        footer = tk.Frame(self.root, bg=CLR_HEADER, height=36)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        tk.Label(
            footer,
            text="Fasal Rin Automation Suite  |  Support: contact admin",
            font=("Segoe UI", 8),
            fg="#888",
            bg=CLR_HEADER,
        ).pack(side="left", padx=16)

    def _build_card(self, parent: tk.Frame, tool: dict):
        slug = tool["slug"]

        card = tk.Frame(
            parent,
            bg=CLR_CARD,
            relief="flat",
            bd=0,
            highlightbackground=CLR_BORDER,
            highlightthickness=1,
        )
        card.pack(fill="x", pady=8, padx=4)

        # ── Left section: icon + text ─────────────────────────────────────────
        left = tk.Frame(card, bg=CLR_CARD)
        left.pack(side="left", fill="both", expand=True, padx=16, pady=14)

        # Icon + name row
        name_row = tk.Frame(left, bg=CLR_CARD)
        name_row.pack(fill="x")
        tk.Label(
            name_row, text=tool["icon"], font=("Segoe UI", 22), bg=CLR_CARD
        ).pack(side="left", padx=(0, 8))
        tk.Label(
            name_row,
            text=tool["name"],
            font=("Segoe UI", 13, "bold"),
            fg=CLR_TEXT,
            bg=CLR_CARD,
        ).pack(side="left")

        # Description
        tk.Label(
            left,
            text=tool["short_desc"],
            font=("Segoe UI", 9),
            fg=CLR_SUBTEXT,
            bg=CLR_CARD,
            wraplength=500,
            justify="left",
            anchor="w",
        ).pack(fill="x", pady=(4, 0))

        # ── Right section: status badge + button ─────────────────────────────
        right = tk.Frame(card, bg=CLR_CARD, width=160)
        right.pack(side="right", fill="y", padx=16, pady=14)
        right.pack_propagate(False)

        # Install status badge
        installed = tm.is_installed(slug, tool["exe_name"])
        status_var = tk.StringVar(value="Installed \u2705" if installed else "Not Downloaded")
        status_lbl = tk.Label(
            right,
            textvariable=status_var,
            font=("Segoe UI", 8, "bold"),
            fg=CLR_GREEN if installed else CLR_GRAY,
            bg=CLR_CARD,
        )
        status_lbl.pack(pady=(4, 6))

        # Action button
        btn_text = "Open" if installed else "Download"
        btn_color = CLR_GREEN if installed else CLR_BLUE
        btn = tk.Button(
            right,
            text=btn_text,
            font=("Segoe UI", 11, "bold"),
            bg=btn_color,
            fg="white",
            relief="flat",
            cursor="hand2",
            width=12,
        )
        btn.pack(pady=2)

        # Progress bar (hidden until download starts)
        prog = ttk.Progressbar(right, orient="horizontal", length=130, mode="determinate")
        prog_lbl = tk.Label(right, text="", font=("Segoe UI", 8), fg=CLR_SUBTEXT, bg=CLR_CARD)

        # Version label
        ver_var = tk.StringVar(value="")
        tk.Label(
            right,
            textvariable=ver_var,
            font=("Segoe UI", 7),
            fg=CLR_SUBTEXT,
            bg=CLR_CARD,
        ).pack(pady=(4, 0))

        # Store refs
        self._cards[slug] = {
            "status_var": status_var,
            "status_lbl": status_lbl,
            "btn": btn,
            "prog": prog,
            "prog_lbl": prog_lbl,
            "ver_var": ver_var,
            "installed": installed,
        }

        # Wire button
        btn.configure(command=lambda s=slug, t=tool: self._on_btn(s, t))

    # ── Data loading ──────────────────────────────────────────────────────────

    def _load_all_tool_info(self):
        """Background thread: fetch version info for all tools."""
        for tool in TOOLS:
            slug = tool["slug"]
            # Fetch latest version info
            info = tm.fetch_latest_info(slug)
            self.root.after(0, lambda s=slug, i=info: self._apply_tool_info(s, i))

    def _apply_tool_info(self, slug: str, info: dict):
        c = self._cards.get(slug)
        if not c:
            return
        try:
            latest = info.get("latest_version", "")
            if latest:
                installed_ver = tm.get_installed_version(slug)
                if installed_ver and installed_ver != latest:
                    c["ver_var"].set(f"Update available: v{latest}")
                    # Change button to "Update"
                    c["btn"].configure(text="Update", bg=CLR_ORANGE)
                    c["installed"] = True  # treat as needing re-download
                elif installed_ver:
                    c["ver_var"].set(f"v{installed_ver} (up to date)")
                else:
                    c["ver_var"].set(f"Latest: v{latest}")
        except tk.TclError:
            pass

    # ── Button handler ────────────────────────────────────────────────────────

    def _on_btn(self, slug: str, tool: dict):
        c = self._cards[slug]
        installed = tm.is_installed(slug, tool["exe_name"])

        if installed and c["btn"].cget("text") not in ("Download", "Update"):
            # Launch
            ok = tm.launch_tool(slug, tool["exe_name"])
            if not ok:
                messagebox.showerror(
                    "Launch Failed",
                    f"Could not launch {tool['name']}.\nTry re-downloading it.",
                    parent=self.root,
                )
        else:
            # Download / Update
            info = tm.fetch_latest_info(slug)
            download_url = info.get("download_url", "")
            if not download_url:
                messagebox.showerror(
                    "Not Available",
                    f"No download URL found for {tool['name']}.\n"
                    "Please contact the admin to set up the download link.",
                    parent=self.root,
                )
                return
            self._start_download(slug, tool, download_url, info.get("latest_version", ""))

    def _start_download(self, slug: str, tool: dict, url: str, version: str):
        c = self._cards[slug]
        c["btn"].configure(state="disabled", text="Downloading...", bg=CLR_GRAY)
        c["prog"].pack(pady=2)
        c["prog_lbl"].pack()
        c["prog"]["value"] = 0

        def _progress(downloaded: int, total: int):
            if total > 0:
                pct = int(downloaded / total * 100)
                mb_done = downloaded / 1_048_576
                mb_total = total / 1_048_576
                self.root.after(0, lambda p=pct, d=mb_done, t=mb_total: self._update_progress(slug, p, d, t))

        def _done(success: bool, error: str):
            self.root.after(0, lambda: self._on_download_done(slug, tool, version, success, error))

        tm.download_tool(slug, tool["exe_name"], url, _progress, _done)

    def _update_progress(self, slug: str, pct: int, mb_done: float, mb_total: float):
        c = self._cards.get(slug)
        if not c:
            return
        try:
            c["prog"]["value"] = pct
            c["prog_lbl"].configure(text=f"{mb_done:.1f} / {mb_total:.1f} MB  ({pct}%)")
        except tk.TclError:
            pass

    def _on_download_done(self, slug: str, tool: dict, version: str, success: bool, error: str):
        c = self._cards.get(slug)
        if not c:
            return
        try:
            c["prog"].pack_forget()
            c["prog_lbl"].pack_forget()
            if success:
                if version:
                    tm._save_version(slug, version)
                c["status_var"].set("Installed \u2705")
                c["status_lbl"].configure(fg=CLR_GREEN)
                c["btn"].configure(state="normal", text="Open", bg=CLR_GREEN)
                c["ver_var"].set(f"v{version} (up to date)" if version else "")
                messagebox.showinfo(
                    "Download Complete",
                    f"{tool['name']} is ready to use.\nClick Open to launch it.",
                    parent=self.root,
                )
            else:
                c["btn"].configure(state="normal", text="Download", bg=CLR_BLUE)
                messagebox.showerror(
                    "Download Failed",
                    f"Could not download {tool['name']}.\n\nError: {error}",
                    parent=self.root,
                )
        except tk.TclError:
            pass
