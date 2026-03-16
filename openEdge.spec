# openEdge.spec

# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

from pathlib import Path
import os

# Gunakan cwd karena __file__ tidak tersedia di .spec
project_dir = Path(os.getcwd()).resolve()

a = Analysis(
    ['openEdge.py'],
    pathex=[str(project_dir)],
    binaries=[
        # Driver masuk ke output folder: driver/
        (str(project_dir / "driver" / "msedgedriver.exe"), "driver"),
    ],
    datas=[
        # config.ini di root output
        (str(project_dir / "config.ini"), "."),
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='openEdge',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # False = tanpa console window
    icon=str(project_dir / "app.ico"),  # Ikon di root project
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='openEdge'
)