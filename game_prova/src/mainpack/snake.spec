# -*- mode: python -*-

block_cipher = None

a = Analysis(['main.py'],
             pathex=['C:\\Users\\simone.quaresmini\\Documents\\personali\\djangows\\provaexe\\game_prova\\src\\mainpack', 'C:\\Users\\simone.quaresmini\\AppData\\Local\\Programs\\Python\\Python35\\DLLs', 'C:\\Users\\simone.quaresmini\\AppData\\Local\\Programs\\Python\\Python35\\lib', 'C:\\Users\\simone.quaresmini\\AppData\\Local\\Programs\\Python\\Python35', 'C:\\Users\\simone.quaresmini\\AppData\\Local\\Programs\\Python\\Python35\\lib\\site-packages', 'C:\\Users\\simone.quaresmini\\AppData\\Local\\Programs\\Python\\Python35\\lib\\site-packages\\win32', 'C:\\Users\\simone.quaresmini\\AppData\\Local\\Programs\\Python\\Python35\\lib\\site-packages\\win32\\lib', 'C:\\Users\\simone.quaresmini\\AppData\\Local\\Programs\\Python\\Python35\\lib\\site-packages\\Pythonwin', 'C:\\Users\\simone.quaresmini\\Documents\\personali\\djangows\\provaexe\\game_prova\\src\\mainpack', 'C:\\Users\\simone.quaresmini\\AppData\\Local\\Programs\\Python\\Python35\\Lib\\site-packages\\pygame'],
             binaries=[('C:\\Users\\simone.quaresmini\\AppData\\Local\\Programs\\Python\\Python35\\Lib\\site-packages\\pygame\\*.dll','.')],
             datas=[],
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
          Tree('resources', prefix='resources'),
		  a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='snake',
		  onefile=True,
          debug=False,
          strip=False,
          upx=True,
          console=False )
