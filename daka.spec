# -*- mode: python -*-

# windows
# pyinstaller --add-data "./captcha/letter_cls;./captcha/letter_cls" --add-data "./captcha/letter;./captcha/letter" daka.py

# *nix
# pyinstaller --add-data "./captcha/letter_cls:./captcha/letter_cls" --add-data "./captcha/letter:./captcha/letter" daka.py


block_cipher = None


a = Analysis(['daka.py'],
             binaries=[],
             datas=[('./captcha/letter_cls', './captcha/letter_cls'), ('./captcha/letter', './captcha/letter')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='daka',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='daka')
