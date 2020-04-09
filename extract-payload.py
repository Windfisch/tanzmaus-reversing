#!/usr/bin/env python3

import sys

from util import hexdump, parse_tanzmaus_sysex, readfile

prefix = sys.argv[1]

sysexes = []
for fn in sys.argv[2:]:
	sysexes.append(readfile(open(fn,'rb')))

pattern_data = parse_tanzmaus_sysex(sysexes)

for i, data in enumerate(pattern_data):
	open(prefix+"_ptn%1X.raw" % i, "wb").write(data)
