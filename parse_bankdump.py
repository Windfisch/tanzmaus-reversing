#!/usr/bin/env python3

from util import *
import sys

data = readfile(open(sys.argv[1],'rb'))
pattern_id = int(sys.argv[2])
outfile = sys.argv[3]

# split into individual sysex messages
sysexes = split_sysexes(data)

# parse the patterns
patterns8 = parse_tanzmaus_sysex(sysexes)

open(outfile, 'wb').write(patterns8[pattern_id])
