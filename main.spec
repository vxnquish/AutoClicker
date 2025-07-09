# -*- mode: python; coding: utf-8 -*-
import os
block_cipher = None
project_path = os.path.abspath('.')  

a = Analysis(
    ['main.py'],
    pathex=[project_path],
    binaries=[],
    datas=[
        (os.path.join(project_path,'fonts','GmarketSansTTFBold.ttf'),   'fonts'),
        (os.path.join(project_path,'fonts','GmarketSansTTFLight.ttf'),  'fonts'),
        (os.path.join(project_path,'fonts','GmarketSansTTFMedium.ttf'), 'fonts'),
    ],
    hiddenimports=['keyboard','pyautogui'],   # ensure keyboard.py is bundled
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
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
    name='AutoClicker',     # change from 'main' to something clearer
    debug=False,
    strip=False,
    upx=False,               # disable UPX while debugging
    console=False,            # turn the console on so you can catch errors
)
