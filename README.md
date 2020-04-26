0: bd.attack, sd.noisedec, cp.filter, tt.attack, sp1.tune, sp2.tune. all muted
1: bs.noisedecay, sd. noise, cp.decay, tt.decay, sp1.decay, sp2.decay+sp2.tune. sp2 unmuted
2: bd.decay, sd.tune, cp.data(distort), tt.pitch, sp1.data(attack?),
3: bd.noise, sd.data, tt.tune
4: bd.pitch, tt.data(pan)
5: bd.tune, then bd.data
6: bd with accent 4324324143243241

data layout:
bd: attack(0fff), decay(ff), 1?, pitch(03ff), tune(0fff). noise(1c), noisedecay(ff), snd(xx), data(e0)
sd: f4 noisedecay(fe), noise(0fff), tune(0fff), 00 00. TODO where is data?
cp: decay(0200-03ff), filter(0fff), data(03ff), 09 00
tt: decay(03ff) tune(03ff)  pitch(ff) ?? attack(0fff) data(ff) snd(xx)
#sp1: !! ?? decay(0fff) 00 !! tune(7f) 44 data(ff) 00 sampleOrAlt(01) 00
sp1: !! ?? decay(0fff) tune(44094000 - 457fe000)  data(ff) 00 sampleOrAlt(01) 00
sampleOrAlt is 00/01 for sp1 and 02/03 for sp2
!! is 00/01 for sp1 and 16/17 for sp2. sound idx?

accent is encoded as (4,3,2,1,notset) = (0fff, 0be8, 0800, 05dc, 0000)

7: 14, but cp last step = 15 instead of 16
8: shuffle = 10
9: bd.scale=5 not 3
10: bd: 5flam = 5. 13flam = 10. sp1= sound 1 and 2 alternating
11: bd snd1, snd8. tom 5,2

14 reference for 7: cp 1 3 5 9 11 13. bd 1 5 9 13
15: reference for 0-5

data layout:
	0000 - 01bf: step data (16 x 2 bytes A pattern + 16 x 2 bytes B pattern,
	             for BD, SD, RS, CP, TT, SP1, SP2 in that order)
	01c0 - 01c7: bitmirrored last step values. (what's the 8th value?!)
	01c8 - 01d0: mute state for bd, sd, rs, cp, tt, sp1, sp1alt, sp2, sp2alt (0x80 vs 00. no lfos)
	01d1 - 01d4: mute state for bdlfo, cplfo, ttlfo, sp1lfo (continued at 0d98)
	01d5 - 02b4: flam data
*	02b5 - 02b5: ??? one byte, wtf. always zero?
	02b6 - 0a75: knob data: (BD, SD, SP1, SP2, CP, TT in that order)
	0a76 - 0d95: LFO + ??? data (BD, CP, TT, SP1, SP2 in that order)
	0d96 - 0da1: ??? (xx xx 00 00 shuffle 00 00 00 ?? ?? 00 00)
	0d9a:        bitmirrored shuffle value
	0d97:        tempo multiplier / scale. 0x60=16ths, 0x30=8ths
	0d98:        sp2lfo mute (80 vs 00)
	


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
