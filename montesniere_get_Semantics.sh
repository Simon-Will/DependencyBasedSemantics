#!/bin/sh

if [ -z "$1" ]; then
	echo "Specify a conll-file in directory 'test' as argument"
	exit
fi

python3 initialize.py  "$1"


