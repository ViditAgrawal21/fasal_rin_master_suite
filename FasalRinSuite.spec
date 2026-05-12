# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec for the Fasal Rin Automation Suite master launcher.
Produces: FasalRinSuite.exe  (~10-20 MB — launcher only, no automation code)
"""

import os
from PyInstaller.utils.hooks import collect_all

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[os.path.abspath('.')],
    binaries=[],
    datas=[],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'requests',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'json',
        'threading',
        'subprocess',
        'pathlib',
        'webbrowser',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[
        'playwright',
        'pandas',
        'openpyxl',
        'cryptography',
        'numpy',
        'matplotlib',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='FasalRinSuite',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,         # No console window — GUI only
    icon=None,             # Add .ico path here if you have an icon
    onefile=True,
)
