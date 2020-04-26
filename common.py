#!/usr/bin/env python3

import sys

args = sys.argv[1:]

bits = 8

if args[0] == '-b':
	bits = int(args[1])
	if bits not in [1,2,4,8]:
		print("ERROR: bits must be 1, 2, 4 or 8")
		exit(1)
	args = args[2:]

chunks = int(8/bits)

def tokenize(data, bits):
	result = []
	for d in data:
		for i in range(0,8,bits):
			result.append( (d >> (i*bits)) & ((1<<bits)-1) )
	return result

datalen = None
for fn in args:
	data = open(fn, 'rb').read(9999999)
	tokens = tokenize(data, bits)

	if datalen is None:
		datalen = len(data)
		accu = tokens
	else:
		if len(data) != datalen:
			print("ERROR: length of %s is %d which differs from %d" % (fn, len(data), datalen))
			exit(1)

		for i in range(len(tokens)):
			if tokens[i] != accu[i]:
				accu[i] = None

if bits >= 4: stride = 16
if bits == 2: stride = 8
if bits == 1: stride = 4

for i in range(0, datalen, stride):
	if any([ accu[k] is not None for k in range(i*chunks, min(i+stride,datalen)*chunks) ]):
		if bits == 8:
			result = [ "xx" if accu[k] is None else "%02X"%accu[k] for k in range(i*chunks, min(i+stride,datalen)*chunks) ]
		else:
			result = [ "x" if accu[k] is None else "%1X"%accu[k] for k in range(i*chunks, min(i+stride,datalen)*chunks) ]

		result = [ result[k:k+chunks] for k in range(0, len(result), chunks) ]
		result_str = " ".join( [ "".join(r) for r in result ] )
		print("%04x: %s" %(i, result_str))

#	for i in range(h, min(h+16, datalen)):
#
#		if any( [accu[chunks*i + k] is not None for j in range(chunks)] ):
#			print("0x%04x: " % i, end="")
#			for j in range(chunks):
#				print(("%02x " if bits==8 else "%01x") % accu[chunks*i + chunks - 1 - j])
