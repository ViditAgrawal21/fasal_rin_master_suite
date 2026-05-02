# -*- coding: utf-8 -*-
"""
Fasal Rin Automation Suite — Master Launcher Entry Point

Startup flow:
  1. Check internet connectivity
  2. Check for master launcher update (non-blocking soft prompt)
  3. Open home screen
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
import threading
import webbrowser

# Ensure project root is on the path when running as a frozen EXE
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from license_config import CURRENT_VERSION
import tool_manager as tm
from home import HomeScreen


def _check_internet() -> bool:
    """Returns True if Supabase is reachable."""
    import requests
    try:
        requests.get(
            "https://oewdqhwdliaqmcqdsyll.supabase.co",
            timeout=5,
        )
        return True
    except Exception:
        return False


def _show_update_banner(root: tk.Tk, info: dict):
    """Show a non-blocking update notification strip at the top of the window."""
    version = info.get("latest_version", "")
    url = info.get("download_url", "")
    if not url:
        return

    banner = tk.Frame(root, bg="#e67e22")
    banner.place(relx=0, rely=0, relwidth=1, height=36)

    tk.Label(
        banner,
        text=f"\u26a0  New version v{version} available!",
        font=("Segoe UI", 9, "bold"),
        fg="white",
        bg="#e67e22",
    ).pack(side="left", padx=12)

    def _download():
        webbrowser.open(url)

    tk.Button(
        banner,
        text="Download Now",
        font=("Segoe UI", 9, "bold"),
        bg="white",
        fg="#e67e22",
        relief="flat",
        cursor="hand2",
        command=_download,
        padx=10,
    ).pack(side="left", padx=8)

    tk.Button(
        banner,
        text="\u00d7",
        font=("Segoe UI", 10),
        bg="#e67e22",
        fg="white",
        relief="flat",
        cursor="hand2",
        command=banner.destroy,
    ).pack(side="right", padx=8)


def launch():
    # ── 1. Splash / loading check ────────────────────────────────────────────
    splash = tk.Tk()
    splash.title("Fasal Rin Automation Suite")
    splash.geometry("380x160")
    splash.resizable(False, False)
    splash.configure(bg="#1a1a2e")
    splash.eval("tk::PlaceWindow . center")

    tk.Label(
        splash,
        text="\U0001f33e  Fasal Rin Automation Suite",
        font=("Segoe UI", 14, "bold"),
        fg="white",
        bg="#1a1a2e",
    ).pack(pady=(28, 6))

    status_var = tk.StringVar(value="Checking connectivity...")
    tk.Label(
        splash,
        textvariable=status_var,
        font=("Segoe UI", 9),
        fg="#aaa",
        bg="#1a1a2e",
    ).pack()

    ttk = __import__("tkinter.ttk", fromlist=["ttk"]).ttk
    bar = ttk.Progressbar(splash, mode="indeterminate", length=280)
    bar.pack(pady=12)
    bar.start(12)

    update_info = {}

    def _startup():
        # Internet check
        splash.after(0, lambda: status_var.set("Checking internet connection..."))
        online = _check_internet()
        if not online:
            splash.after(0, lambda: _no_internet(splash))
            return

        # Master update check (background, soft)
        splash.after(0, lambda: status_var.set("Checking for updates..."))
        info = tm.check_master_update(CURRENT_VERSION)
        if info:
            update_info.update(info)

        splash.after(0, lambda: status_var.set("Loading..."))
        splash.after(200, _open_home)

    def _no_internet(parent):
        bar.stop()
        messagebox.showerror(
            "No Internet Connection",
            "Fasal Rin Automation Suite requires an internet connection.\n"
            "Please connect and try again.",
            parent=parent,
        )
        parent.destroy()
        sys.exit(1)

    def _open_home():
        bar.stop()
        splash.destroy()
        root = tk.Tk()
        app = HomeScreen(root)
        # Show update banner if update available
        if update_info:
            root.after(800, lambda: _show_update_banner(root, update_info))
        root.mainloop()

    threading.Thread(target=_startup, daemon=True).start()
    splash.mainloop()


if __name__ == "__main__":
    launch()
