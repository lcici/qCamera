#!/usr/bin/env bash

# Copy this file as .git/hooks/post-merge to automatically install
# updated files whenever a git merge is done (which happens
# automatically when a git pull is done!).

python setup.py install

