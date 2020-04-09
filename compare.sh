#!/usr/bin/env bash

hexdump -vC $1 > $1.hex
hexdump -vC $2 > $2.hex

vimdiff $1.hex $2.hex

rm $1.hex $2.hex
