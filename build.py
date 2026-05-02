# -*- coding: utf-8 -*-
"""
Build script for Fasal Rin Automation Suite master launcher.

Usage:
    python build.py

Output:
    dist/FasalRinSuite.exe   (~10-20 MB)
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path

HERE = Path(__file__).parent


def main():
    print("=" * 60)
    print("  Building Fasal Rin Automation Suite Launcher")
    print("=" * 60)

    # Clean previous build
    for folder in ["build", "dist"]:
        p = HERE / folder
        if p.exists():
            shutil.rmtree(p)
            print(f"Cleaned: {folder}/")

    # Run PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--noconfirm",
        str(HERE / "FasalRinSuite.spec"),
    ]
    result = subprocess.run(cmd, cwd=str(HERE))

    if result.returncode != 0:
        print("\nBuild FAILED.")
        sys.exit(1)

    exe = HERE / "dist" / "FasalRinSuite.exe"
    if exe.exists():
        size_mb = exe.stat().st_size / 1_048_576
        print(f"\nBuild SUCCESS: {exe}")
        print(f"Size: {size_mb:.1f} MB")
        print("\nUpload dist/FasalRinSuite.exe to GitHub Releases.")
    else:
        print("\nBuild completed but EXE not found — check PyInstaller output.")


if __name__ == "__main__":
    main()
