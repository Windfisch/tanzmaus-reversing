data layout:
	0000 - 01bf: step data (16 x 2 bytes A pattern + 16 x 2 bytes B pattern,
	             for BD, SD, RS, CP, TT, SP1, SP2 in that order)
	01c0 - 02b5: ??? (8x f0, then zeros)
	02b6 - 0a75: knob data: (BD, SD, SP1, SP2, CP, TT in that order)
	0a76 - 0d95: LFO + ??? data (BD, CP, TT, SP1, SP2 in that order)
	0d96 - 0da1: ??? (00 60 00 00 00 00 00 00 ?? ?? 00 00)
	


file: allinstrument.syx
	patterns 0..13 only have $instrument programmed at the following steps:
		1     3     5     7     9  10 11 12 13 14 15 16
		where $instrument is (in that order) BD, BDlfo, SD, RS, CP, CPlfo, TT,
		TTlfo, SP1, SP1alt, SP1lfo, SP2, SP2alt, SP2lfo

file: test2.syx:
	0: bd from allinstrument.syx copied to pattern B
	1: playing all instruments on the B pattern
	2: all instruments wiggle each knob (left to right. top to bottom)
	5: wiggling data, descending accent, flam on 5 and 9
	14: basedrum with slowly increasing tune

0d9e - 0d9f: checksum?

bd pattern:
	0000 - 003f step data (00 00 unset / ff f0 set) (first A, then B)
	02b6 - 0435 32 x 12 byte knob data: attack2, decay1, ?, tune, ?, ?, data1

sd pattern:
	0040 - 007f: step data
	0436 - 0535: 32 x 8 byte stuff

rs pattern:
	0080 - 00bf: step data

cp pattern:
	00c0 - 00ff: step data
	0836 - 0935: 32 x 8 byte stuff

tt pattern:
	0100 - 013f: step data
	0936 - 0a75: 32 x 10 byte

sp1 pattern:
	0140 - 017f: step data
	0536 - 06b5: 32 x 12 byte

sp1alt pattern: same as sp1, but some bits set in the 0538... block

sp2 pattern:
	0180 - 01bf: step data
	06b6 - 0835: 32 x 12 byte

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



BD with increasing tune value gives this:
```
   bd                                     bd
 step                                   data

3b a0    .. .. 1b .. 9f c0 .. .. 38 .. .. 05
3b a0    .. .. 1b .. 9f c0 .. .. 38 .. .. 05
3b a0    .. .. 1b .. 9f c0 .. .. 38 .. .. 05
3b a0    .. .. 1b .. 9f c0 d3 40 38 .. .. 05
3b a0    .. .. 1b .. 9f c0 d3 c0 38 .. .. 05
3b a0    .. .. 1b .. 9f c0 27 20 38 .. .. 05
3b a0    .. .. 1b .. 9f c0 c2 60 38 .. .. 05
3b a0    .. .. 1b .. 9f c0 3e e0 38 .. .. 05

3b a0    .. .. 1b .. 9f c0 3e 10 38 .. .. 05
3b a0    .. .. 1b .. 9f c0 2a 50 38 .. .. 05
3b a0    .. .. 1b .. 9f c0 09 d0 38 .. .. 05
3b a0    .. .. 1b .. 9f c0 29 30 38 .. .. 05
3b a0    .. .. 1b .. 9f c0 8b b0 38 .. .. 05
3b a0    .. .. 1b .. 9f c0 8b 70 38 .. .. 05
3b a0    .. .. 1b .. 9f c0 c9 f0 38 .. .. 05
3b a0    .. .. 1b .. 9f c0 2f f0 38 .. .. 05
                           ^^^^^
                      changing values
```

Note how the values change in a non-obvious way.
Viewing their binary representation yields this:

```
0000000000000000 = 0000
1101001101000000 = d340
1101001111000000 = d3c0
0010011100100000 = 2720
1100001001100000 = c260
0011111011100000 = 3ee0
0011110100010000 = 3d10
0010101001010000 = 2a50
0000100111010000 = 09d0
0010100100110000 = 2930
1000101110110000 = 8bb0
1000101101110000 = 8b70
1100100111110000 = c9f0
0010111111110000 = 2ff0
```

-> They seem to be bit-reversed.
