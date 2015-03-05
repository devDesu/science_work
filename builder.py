from cx_Freeze import *
import sys

includefiles = ['ffmpeg/', 'setup.bat']

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [
    Executable('col_detection.py', base=base, shortcutName="Color detection",
               shortcutDir="DesktopFolder")
]

setup(name='Color detection',
      version='0.2',
      description='Color detection tool',
      executables=executables,
      options={'build_exe': {'include_files': includefiles}}
      )