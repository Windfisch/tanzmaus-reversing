#!/bin/bash

TMP="tmp.common"
rm -rf "$TMP"
mkdir -p "$TMP"

for i in $@; do
	echo -n "$i: "
	for ((j=0; j<16; j++)); do
		echo -n "$j "
		./parse_bankdump.py $i $j "$TMP/$(basename "$i")_${j}.bin"
	done
	echo
done

./common.py "$TMP"/*.bin
