#!/usr/bin/env python3

import sys
data = open(sys.argv[1], 'rb').read(99999999)
out = open(sys.argv[2], 'wb')
data = data[2:] # strip the first two bytes, which seem to be "pattern number" and "zero"

result = bytes()

for i in range(0, len(data)-7, 8):
	block = ""
	for j in range(0,8):
		bits = ("%7s" % bin(data[i+j])[2:]).replace(' ','0')
		bits_reversed = bits[::-1]
		block += bits_reversed
	assert(len(block)==56)
	
	result += bytes([int(block[j:j+8],2) for j in range(0,56,8)])

out.write(result)
