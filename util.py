def readfile(f):
	CHUNKSIZE=4096
	result = bytes()
	while True:
		r = f.read(CHUNKSIZE)
		if len(r) == 0:
			return result
		result += r

def split_sysexes(data):
	return [b'\xf0' + trailing for trailing in data.split(b'\xf0')[1:]]

def hexdump(bs):
	r = ''
	for b in bs:
		h = hex(b)[2:]
		h = (2-len(h))*'0' + h
		r += h + ' '
	return r[0:-1]

def parse_tanzmaus_sysex(sysexes):
	pattern_data = []
	expected_part = 0
	expected_pattern = 0
	
	for bs in sysexes:
		if bs[0] != 0xf0:
			raise ValueError("%s does not start with F0 (begin sysex) but with %s" % (fn, hex(bs[0])[2:]))
		if bs[-1] != 0xf7:
			raise ValueError("%s does not end with F7 (end sysex) but with %s" % (fn, hex(bs[-1])[2:]))
		if bs[1:4] != b'\x00\x21\x0b':
			raise ValueError("%s does not appear to be a MFB sysex (starts with %s instead of %s)" % (fn, hexdump(bs[1:4]), "00 21 0b"))
		if bs[4:9] != b'\x04\x00\x03\x00\x00':
			raise ValueError("%s does not appear to be a tanzmaus sysex(%s instead of 04 00 03 00 00)" % (fn, hexdump(bs[5:10])))

		part = bs[9]
		if part != expected_part: raise ValueError("%s has unexpected part no %d instead of %d" % (fn, part, expected_part))
		expected_part += 1
		if expected_part > 0xd: expected_part = 0
		
		if part == 0:
			pattern = bs[10]
			if pattern != expected_pattern: raise ValueError("%s has unexpected pattern no %d instead of %d" % (fn, pattern, expected_pattern))
			expected_pattern += 1
			if bs[11] != 0: raise ValueError("unexpected byte after pattern no, expected 00 instead of %s" % hex(bs[11]))

			pattern_data.append(bytes())

		expected_len = 317 if part != 0xd else 84

		if len(bs) != expected_len:
			raise ValueError("%s has unexpected length (%d instead of %d)" % (fn, len(bs), expected_len))

		payload7 = bs[10:-1]
		payload7 = payload7[:-4]
		payload8 = convert_7to8(payload7)
		pattern_data[-1] += payload8

	for d in pattern_data: assert(d[1] == 0)
	pattern_data = [ d[2:] for d in pattern_data ] # strip the first 16 bits. 14 of these are the pattern id + 00 anyway. this makes the base drum step pattern start at position zero, which is probably good.

	return pattern_data

def convert_7to8(data):
	result = bytes()
	block = ""
	for i in range(0, len(data)):
		bits = ("%7s" % bin(data[i])[2:]).replace(' ','0')
		bits_reversed = bits[::-1]
		block += bits_reversed
	
		if len(block) >= 8:
			result += bytes([int(block[0:8],2)])
			block = block[8:]
	
	if block.find('1') != -1:
		raise ValueError("convert_7to8 with nonzero remainder!")

	return result
