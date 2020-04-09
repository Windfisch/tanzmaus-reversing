#!/usr/bin/env bash

../parse_bankdump.py ../all_instruments.syx 0 bd.bin
../parse_bankdump.py ../all_instruments.syx 1 bdlfo.bin
../parse_bankdump.py ../all_instruments.syx 2 sd.bin
../parse_bankdump.py ../all_instruments.syx 3 rs.bin
../parse_bankdump.py ../all_instruments.syx 4 cp.bin
../parse_bankdump.py ../all_instruments.syx 5 cplfo.bin
../parse_bankdump.py ../all_instruments.syx 6 tt.bin
../parse_bankdump.py ../all_instruments.syx 7 ttlfo.bin
../parse_bankdump.py ../all_instruments.syx 8 sp1.bin
../parse_bankdump.py ../all_instruments.syx 9 sp1alt.bin
../parse_bankdump.py ../all_instruments.syx 10 sp1lfo.bin
../parse_bankdump.py ../all_instruments.syx 11 sp2.bin
../parse_bankdump.py ../all_instruments.syx 12 sp2alt.bin
../parse_bankdump.py ../all_instruments.syx 13 sp2lfo.bin
../parse_bankdump.py ../all_instruments.syx 14 init.bin
../parse_bankdump.py ../all_instruments.syx 15 multi.bin

