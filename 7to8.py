#!/usr/bin/env python3

import sys
from util import readfile, pattern_7to8
data = readfile(open(sys.argv[1], 'rb'))
open(sys.argv[2], 'wb').write(pattern_7to8(data))
