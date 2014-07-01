"""Utility file for building Qt ui files."""

from __future__ import print_function
import sys
import os
from glob import glob

if 'win' in sys.platform:
    cmd = 'pyuic4.bat'
else:
    cmd = 'pyuic4'

for fname in glob('*.ui'):
    pre = fname.split('.')[0]
    full_cmd = cmd + ' ' + fname + ' -o ui_' + pre + '.py'
    print(full_cmd)
    os.system(full_cmd)
    
