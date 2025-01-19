# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['venv\\.RUN_ONLY\\CreateCaptcha.py'],
    pathex=[],
    binaries=[],
    datas=[('venv/.YOU_CAN_CHANGE/gennerated_imgs', 'gennerated_imgs'), ('./venv/.YOU_CAN_CHANGE/test_images', 'test_images'), ('./venv/.YOU_CAN_CHANGE/tokens.txt', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='CreateCaptcha',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
