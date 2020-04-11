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
	["bd","step"], ["bd","data"], ["bdlfo","step"], ["bdlfo","data"],
	["sd","step"], ["sd","data"],
	["rs","step"],
	["cp","step"], ["cp","data"], ["cplfo","step"], ["cplfo","data"],
	["tt","step"], ["tt","data"], ["ttlfo","step"], ["ttlfo","data"],
	["sp1","step"], ["sp1","data"], ["sp1lfo","step"], ["sp1lfo","data"],
	["sp2","step"], ["sp2","data"], ["sp2lfo","step"], ["sp2lfo","data"] ]

BDSTEP,BDDATA,BDLFOSTEP,BDLFODATA=0,1,2,3
SDSTEP,SDDATA=4,5
RSSTEP=6
CPSTEP,CPDATA,CPLFOSTEP,CPLFODATA=7,8,9,10
TTSTEP,TTDATA,TTLFOSTEP,TTLFODATA=11,12,13,14
SP1STEP,SP1DATA,SP1LFOSTEP,SP1LFODATA=15,16,17,18
SP2STEP,SP2DATA,SP2LFOSTEP,SP2LFODATA=19,20,21,22

BD,SD,RS,CP,TT,SP1,SP2 = BDSTEP,SDSTEP,RSSTEP,CPSTEP,TTSTEP,SP1STEP,SP2STEP

for index,instr in enumerate([BD,SD,RS,CP,TT,SP1,SP2]):
	add(columns[instr], pattern[0x40*index : 0x40*(index+1)])

for instr, start, length in [(BD,0x2b6,12),(SD,0x436,8),(SP1,0x536,12),(SP2,0x6b6,12),(CP,0x836,8),(TT,0x936,10)]:
	add(columns[instr+1], pattern[start : start+32*length])

for index,instr in enumerate([BD,CP,TT,SP1,SP2]):
	base = 0xa76 + index*0xa0
	add(columns[instr+2], pattern[base : base+0x20])
	add(columns[instr+3], pattern[base+0x20 : base+0x40])

colprint(columns)


