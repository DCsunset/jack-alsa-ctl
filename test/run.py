#!/usr/bin/python

import sys
from pathlib import Path

# Resolve symlink path as well
directory = Path(__file__).resolve().parent
# add the root path of this project
sys.path.insert(0, str(directory.parent))

from jack_alsa_ctl.cli import main

main()
