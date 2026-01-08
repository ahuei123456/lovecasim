# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\trios\\.gemini\\antigravity\\scratch\\loveca-copy\\server.py'],
    pathex=[],
    binaries=[],
    datas=[('web_ui', 'web_ui'), ('data', 'data')],
    hiddenimports=['engineio.async_drivers.threading', 'eventlet', 'eventlet.hubs.epolls', 'eventlet.hubs.kqueue', 'eventlet.hubs.selects', 'dns'],
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
    name='LovecaSolo',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
