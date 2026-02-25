# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for Lexloop.
# Build with: pyinstaller lexloop.spec

a = Analysis(
    ["app.py"],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="lexloop",
    debug=False,
    strip=False,
    upx=True,
    console=False,
)
