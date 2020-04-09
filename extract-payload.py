#!/usr/bin/env python3

import sys

def die(s):
	print(s)
	exit(1)

def hexdump(bs):
	r = ''
	for b in bs:
		h = hex(b)[2:]
		h = (2-len(h))*'0' + h
		r += h + ' '
	return r[0:-1]


prefix = sys.argv[1]

expected_part = 0
expected_pattern = 0
for fn in sys.argv[2:]:
	bs = open(fn, 'rb').read(999999999)

	if bs[0] != 0xf0:
		die("%s does not start with F0 (begin sysex) but with %s" % (fn, hex(bs[0])[2:]))
	if bs[-1] != 0xf7:
		die("%s does not end with F7 (end sysex) but with %s" % (fn, hex(bs[-1])[2:]))
	if bs[1:4] != b'\x00\x21\x0b':
		die("%s does not appear to be a MFB sysex (starts with %s instead of %s)" % (fn, hexdump(bs[1:4]), "00 21 0b"))
	if bs[4:9] != b'\x04\x00\x03\x00\x00':
		die("%s does not appear to be a tanzmaus sysex(%s instead of 04 00 03 00 00)" % (fn, hexdump(bs[5:10])))

	part = bs[9]
	if part != expected_part: die("%s has unexpected part no %d instead of %d" % (fn, part, expected_part))
	expected_part += 1
	if expected_part > 0xd: expected_part = 0
	
	if part == 0:
		pattern = bs[10]
		if pattern != expected_pattern: die("%s has unexpected pattern no %d instead of %d" % (fn, pattern, expected_pattern))
		expected_pattern += 1

		outfile = open(prefix+"_ptn%1X.raw" % pattern, "wb")

	expected_len = 317 if part != 0xd else 84

	if len(bs) != expected_len:
		die("%s has unexpected length (%d instead of %d)" % (fn, len(bs), expected_len))

	payload = bs[10:-1]
	outfile.write(payload)

