patterns 0..13 only have $instrument programmed at the following steps:
	1     3     5     7     9  10 11 12 13 14 15 16
	where $instrument is (in that order) BD, BDlfo, SD, RS, CP, CPlfo, TT,
	TTlfo, SP1, SP1alt, SP1lfo, SP2, SP2alt, SP2lfo

bd pattern:
	0000 - 001f  (00 00 unset / 3f fc set)
	02bd - 0381 16 x 12 byte stuff? (maybe wrong bit alignment)
	0106 - 010a: ??
	0429 - 042c: ??
	0dcf - 0dd6: ??

sd pattern:
	0040 - 005f: (0000 vs 3ffc)
	0445 - 04c4: 16 x 8 byte stuff (maybe wrong bit alignment)
	0106 - 010a: ??
	0535 - 0438: ??
	0dcf - 0dd6: ??

rs pattern:
	0080 - 009f: 3ffc
	0106 - 010a: ??
	0dcf - 0dd6: ??

cp pattern:
	00c0 - 00df: 3ffc
	0106 - 010a: ??
	085x:        ??
	0853 - 08d2: 16 x 8 byte stuff (alignment?)
	0966 - 0967: ??
	0dcf - 0dd6: ??

tt pattern:
	0100 - 0123: first 3ffc then wtf?!

the TT's 3ffc pattern becomes weird after byte 0x106: garbage from 0x106 - 0x109, then
a fff0 pattern from 0x10a. (fff0 == 3ffc << 2)

-> the payload size of one sysex is probably only 300
