#!/bin/bash

if [ -z "$1" ]; then
	echo specify a conll-file in directory \'test\' as argument
	exit
fi

python3 initialize.py  $1


