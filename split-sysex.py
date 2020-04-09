#!/usr/bin/env python3

import sys
from util import readfile, split_sysexes

outprefix = sys.argv[1]
data = readfile(sys.stdin.buffer)

for i, sysex in enumerate(split_sysexes(data)):
	open(outprefix + "%03d.part" % i, "wb").write(sysex)
