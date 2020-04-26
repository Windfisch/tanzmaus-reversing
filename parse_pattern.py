#!/usr/bin/env python3

from util import *
import sys

data = readfile(open(sys.argv[1],'rb'))
pattern_id = int(sys.argv[2])

def colprint(columns):
	MAXWIDTH = 120
	DISTANCE = 4
	PAD = DISTANCE * " "

	def flush(p):
		for i,s in enumerate(p):
			if i>=2 and (i-2) % 8 == 0:
				print('')
			print(s.replace('00','..'))
		print()
		print()

	rows = len(columns[0])
	if any([ len(column) != rows for column in columns ]): raise ValueError("all columns must have the same amount of entries")

	page = rows*[""]
	pagewidth = 0
	for column in columns:
		width = max([len(c) for c in column])

		pagewidth += width + DISTANCE
		if pagewidth > MAXWIDTH:
			flush(page)
			page = rows*[""]
			pagewidth=0

		for row in range(rows):
			page[row] += ("%%%ds" % width) % column[row] + PAD
	
	flush(page)


def add(column, data):
	if len(data) % 32 != 0: raise ValueError("data length must be a multiple of 32!")
	step = int(len(data)/32)
	for i in range(32):
		column.append(hexdump(data[i*step : (i+1)*step]))

# split into individual sysex messages
sysexes = split_sysexes(data)

# parse the patterns
patterns = parse_tanzmaus_sysex(sysexes)

pattern = bitmirror(patterns[pattern_id])

columns = [
	["bd","step"], ["bd","data"], ["bdlfo","step"], ["bdlfo","data"], ["bdlfo","unk1"], ["bdlfo","unk2"], ["bdlfo","unk3"],
	["sd","step"], ["sd","data"],
	["rs","step"],
	["cp","step"], ["cp","data"], ["cplfo","step"], ["cplfo","data"], ["cplfo","unk1"], ["cplfo","unk2"], ["cplfo","unk3"],
	["tt","step"], ["tt","data"], ["ttlfo","step"], ["ttlfo","data"], ["ttlfo","unk1"], ["ttlfo","unk2"], ["ttlfo","unk3"],
	["sp1","step"], ["sp1","data"], ["sp1lfo","step"], ["sp1lfo","data"], ["sp1lfo","unk1"], ["sp1lfo","unk2"], ["sp1lfo","unk3"],
	["sp2","step"], ["sp2","data"], ["sp2lfo","step"], ["sp2lfo","data"], ["sp2lfo","unk1"], ["sp2lfo","unk2"], ["sp2lfo","unk3"]
]

BDSTEP,BDDATA,BDLFOSTEP,BDLFODATA=0,1,2,3
SDSTEP,SDDATA=7,8
RSSTEP=6
CPSTEP,CPDATA,CPLFOSTEP,CPLFODATA=7,8,9,10
TTSTEP,TTDATA,TTLFOSTEP,TTLFODATA=11,12,13,14
SP1STEP,SP1DATA,SP1LFOSTEP,SP1LFODATA=15,16,17,18
SP2STEP,SP2DATA,SP2LFOSTEP,SP2LFODATA=19,20,21,22

BD,SD,RS,CP,TT,SP1,SP2 = 0,7,9,10,17,24,31

for index,instr in enumerate([BD,SD,RS,CP,TT,SP1,SP2]):
	add(columns[instr], pattern[0x40*index : 0x40*(index+1)])

for instr, start, length in [(BD,0x2b6,12),(SD,0x436,8),(SP1,0x536,12),(SP2,0x6b6,12),(CP,0x836,8),(TT,0x936,10)]:
	add(columns[instr+1], pattern[start : start+32*length])

for index,instr in enumerate([BD,CP,TT,SP1,SP2]):
	base = 0xa76 + index*0xa0
	add(columns[instr+2], pattern[base : base+0x20])
	add(columns[instr+3], pattern[base+0x20 : base+0x40])
	add(columns[instr+4], pattern[base+0x40 : base+0x60])
	add(columns[instr+5], pattern[base+0x60 : base+0x80])
	add(columns[instr+6], pattern[base+0x80 : base+0xa0])
	unknown = pattern[base+0x40 : base+0xa0]
	for j in range(3):
		print("%4x: %s" % (base+0x40+0x20*j, hexdump(unknown[0x20*j:0x20*(j+1)]).replace('00','..')))

colprint(columns)


print("1c0 - 1c8 = %s" % hexdump(pattern[0x1c0:0x1c8]))
if any(b!=0 for b in pattern[0x1c8:0x2b6]):
	print("1c8 - 2b6 = %s" % hexdump(pattern[0x1c8:0x2b6]))

print(hexdump(pattern[0xd96:0xd9e]))

