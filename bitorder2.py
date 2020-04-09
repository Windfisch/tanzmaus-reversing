#!/usr/bin/env/python3

data=[0x00, 0x00, 0x01, 0x5c, 0x00, 0x15, 0xff, 0xc1, 0x1c, 0x01, 0xbf, 0x00, 0x00, 0x00, 0x01, 0x5c]

msbfirst = ''
lsbfirst = ''

for i in data:
    bits = ("%8s" % bin(i)[2:]).replace(' ','0')
    msbfirst += bits
    lsbfirst += bits[::-1]

print ("msbfirst: "+msbfirst)
print ("lsbfirst: "+lsbfirst)
