#!/bin/bash

for maxlen in 256 1024 2048 4096 6144 do
	for numfilter in 12 24 64 128 256 do
		for dense in 32 64 128 256 do
			for kernel in 4 8 16 24 64 128 do
				for pool in 4 16 24 64 256 do
					python main_reg.py $maxlen $numfilter $dense $kernel $pool
				done
			done
		done
	done
done