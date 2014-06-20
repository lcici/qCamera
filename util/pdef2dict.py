#!/usr/bin/env python
"""Utility for converting a bunch of #defined (integer!) constants
into a Python dictionary

To use this, you'll want to create a new header file that just
contains lines such as::

  #define FOO 0

Every line that doesn't start with #define will be ignored.

"""

from __future__ import print_function

def convert(defines):
    """Convert the string defines into a dict."""
    constants = {}
    for line in defines:
        line = line.split()
        try:
            if line[0] != '#define':
                continue
            constants[line[1]] = int(line[2], base=0)
        except IndexError:
            pass
    return constants

if __name__ == "__main__":
    import sys, json
    
    try:
        fname = sys.argv[1]
        with open(fname, 'r') as f:
            constants = convert(f.readlines())
    except IndexError:
        print("Usage: python pdef2dict.py <filename>")
        sys.exit(1)
    with open('outfile.py', 'w') as outfile:
        out = json.dumps(constants, indent=4, sort_keys=True)
        outfile.write('constants = ' + out)

    