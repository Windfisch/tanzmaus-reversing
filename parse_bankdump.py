#!/usr/bin/env python3

from util import *
import sys

data = readfile(open(sys.argv[1],'rb'))
pattern_id = int(sys.argv[2])
outfile = sys.argv[3]

# split into individual sysex messages
sysexes = split_sysexes(data)

# parse the patterns and convert them from 7-bit MIDI encoding to 8-bit encoding.
patterns7 = parse_tanzmaus_sysex(sysexes)
patterns8 = [pattern_7to8(p7) for p7 in patterns7]

open(outfile, 'wb').write(patterns8[pattern_id])
