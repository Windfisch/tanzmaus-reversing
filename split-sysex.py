#!/usr/bin/env python3

import sys

outprefix = sys.argv[1]

i=0

while True:
	b = sys.stdin.buffer.read(1)
	if len(b) == 0: break
	
	if b == b'\xf0':
		f = open(outprefix + "%03d.part" % i, "wb")
		i+=1
	
	if f is not None:
		f.write(b)
