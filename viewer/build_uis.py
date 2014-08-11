"""Utility file for building Qt ui files."""

import sys
import os
from hashlib import md5
import json
from glob import glob

if 'win' in sys.platform:
    cmd = 'pyuic4.bat'
else:
    cmd = 'pyuic4'

hash_file = 'hashes.json'
try:
    hashes = json.load(open(hash_file, 'r'))
except:
    hashes = {}

for fname in glob('*.ui'):
    pre = fname.split('.')[0]
    ui_py_fname = 'ui_' + pre + '.py'
    new_hash = md5(open(fname).read()).hexdigest()
    if hashes.get(fname, None) != new_hash:
        full_cmd = cmd + ' ' + fname + ' -o ' + ui_py_fname
        print(full_cmd)
        os.system(full_cmd)
        hashes[fname] = new_hash

with open(hash_file, 'w') as output:
    json.dump(hashes, output, indent=4)
    