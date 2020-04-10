patterns 0..13 only have $instrument programmed at the following steps:
	1     3     5     7     9  10 11 12 13 14 15 16
	where $instrument is (in that order) BD, BDlfo, SD, RS, CP, CPlfo, TT,
	TTlfo, SP1, SP1alt, SP1lfo, SP2, SP2alt, SP2lfo

0d9e - 0d9f: checksum?

bd pattern:
	0000 - 001f  step data (00 00 unset / ff f0 set)
	02b6 - 0375 16 x 12 byte stuff?

sd pattern:
	0040 - 005f: step data
	0436 - 04b2: 16 x 8 byte stuff

rs pattern:
	0080 - 009f: step data

cp pattern:
	00c0 - 00df: step data
	0836 - 08b2: 16 x 8 byte stuff (alignment?)

tt pattern:
	0100 - 011f: step data
	0936 - 09d4: 16x 10 byte

sp1 pattern:
	0140 - 015f: step data
	0538 - 5f8: 16x 12 byte

sp1alt pattern: same as sp1, but some bits set in the 0538... block

sp2 pattern:
	0180 - 019f: step data
	06b6 - 775: 16x 12 byte

bd lfo pattern:
	0a76 - 0a85: step data (80 vs 00)
	02b6 - 02c5: ?? (random)
	0a96 - 0ab5: ?? 16x 2 byte

cp lfo pattern:
	0b16 - 0b25: step data (80 vs 00)
	0b36 - 0b55: 16x 2 byte

tt lfo pattern:
	0bb6 - 0bc5: step
	0bd6 - 0bf5: data

sp1 lfo:
	0c56 - 0c65: step
	0c76 - 0c85: data

sp2 lfo:
	0cf6 - 0d05: step
	0d16 - 0d35: data



the TT's 3ffc pattern becomes weird after byte 0x106: garbage from 0x106 - 0x109, then
a fff0 pattern from 0x10a. (fff0 == 3ffc << 2)

-> the payload size of one sysex is probably only 300
-> bd 0x2ba section suggests that each 
