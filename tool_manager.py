# -*- coding: utf-8 -*-
"""
Tool Manager — handles downloading, versioning, and launching individual tool EXEs.

Tools are stored in: %APPDATA%\FasalRinSuite\<slug>\<exe_name>
Version info cached in: %APPDATA%\FasalRinSuite\<slug>\version.json
"""

import os
import json
import requests
import subprocess
import threading
from pathlib import Path
from license_config import EDGE_BASE, SUPABASE_ANON_KEY, REQUEST_TIMEOUT


# ── Storage directory ─────────────────────────────────────────────────────────
INSTALL_DIR = Path(os.environ.get("APPDATA", os.path.expanduser("~"))) / "FasalRinSuite"
INSTALL_DIR.mkdir(parents=True, exist_ok=True)


def _headers() -> dict:
    return {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
        "Content-Type": "application/json",
    }


# ── Version / download URL resolution ────────────────────────────────────────

def _tool_dir(slug: str) -> Path:
    d = INSTALL_DIR / slug
    d.mkdir(parents=True, exist_ok=True)
    return d


def _version_file(slug: str) -> Path:
    return _tool_dir(slug) / "version.json"


def get_installed_version(slug: str) -> str | None:
    vf = _version_file(slug)
    if vf.exists():
        try:
            return json.loads(vf.read_text(encoding="utf-8")).get("version")
        except Exception:
            pass
    return None


def _save_version(slug: str, version: str) -> None:
    _version_file(slug).write_text(
        json.dumps({"version": version}), encoding="utf-8"
    )


def get_exe_path(slug: str, exe_name: str) -> Path:
    return _tool_dir(slug) / exe_name


def is_installed(slug: str, exe_name: str) -> bool:
    return get_exe_path(slug, exe_name).exists()


def fetch_latest_info(slug: str) -> dict:
    """
    Call check-version edge function for this tool.
    Returns dict with keys: latest_version, download_url, changelog, up_to_date, is_forced_update
    Returns {} on failure.
    """
    try:
        resp = requests.post(
            f"{EDGE_BASE}/check-version",
            headers=_headers(),
            json={"tool_slug": slug, "current_version": get_installed_version(slug) or "0.0.0"},
            timeout=REQUEST_TIMEOUT,
        )
        return resp.json()
    except Exception:
        return {}


def fetch_price(slug: str) -> int:
    """Fetch current admin-set price for a tool. Returns 0 on failure."""
    try:
        resp = requests.post(
            f"{EDGE_BASE}/get-payment-config",
            headers=_headers(),
            json={"tool_slug": slug},
            timeout=REQUEST_TIMEOUT,
        )
        return resp.json().get("price_inr", 0)
    except Exception:
        return 0


# ── Download ─────────────────────────────────────────────────────────────────

def download_tool(
    slug: str,
    exe_name: str,
    download_url: str,
    progress_cb=None,       # callable(downloaded_bytes, total_bytes)
    done_cb=None,           # callable(success: bool, error_msg: str)
):
    """
    Download tool EXE in a background thread.
    progress_cb(downloaded, total) called on each chunk.
    done_cb(True, "") or done_cb(False, "error message") when complete.
    """
    def _run():
        dest = get_exe_path(slug, exe_name)
        tmp = dest.with_suffix(".tmp")
        try:
            with requests.get(download_url, stream=True, timeout=300) as r:
                r.raise_for_status()
                total = int(r.headers.get("content-length", 0))
                downloaded = 0
                with open(tmp, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024 * 256):  # 256 KB chunks
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            if progress_cb:
                                progress_cb(downloaded, total)
            # Atomic replace
            if dest.exists():
                dest.unlink()
            tmp.rename(dest)
            if done_cb:
                done_cb(True, "")
        except Exception as e:
            if tmp.exists():
                tmp.unlink(missing_ok=True)
            if done_cb:
                done_cb(False, str(e))

    threading.Thread(target=_run, daemon=True).start()


# ── Launch ────────────────────────────────────────────────────────────────────

def launch_tool(slug: str, exe_name: str) -> bool:
    """
    Launch the installed tool EXE as a separate process.
    Returns True if launched successfully, False otherwise.
    """
    path = get_exe_path(slug, exe_name)
    if not path.exists():
        return False
    try:
        subprocess.Popen(
            [str(path)],
            cwd=str(path.parent),
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            if os.name == "nt" else 0,
        )
        return True
    except Exception:
        return False


# ── Master update check ───────────────────────────────────────────────────────

def check_master_update(current_version: str) -> dict | None:
    """
    Check if a new master launcher version is available.
    Returns dict {latest_version, download_url, changelog} or None if up to date / error.
    """
    try:
        resp = requests.post(
            f"{EDGE_BASE}/check-version",
            headers=_headers(),
            json={"tool_slug": "master", "current_version": current_version},
            timeout=REQUEST_TIMEOUT,
        )
        data = resp.json()
        if data.get("up_to_date"):
            return None
        return data
    except Exception:
        return None
