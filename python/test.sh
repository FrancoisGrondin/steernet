#!/bin/bash

audio="file.meta"
json="json/features.json"
model="model.bin"
filtered="outputfolder/"

for i in {0..999}
do
	
	echo $i

	wave_dst=$(printf "%s%08u.wav" $filtered $i)

	test_sample=$(printf "python3 test_sample.py --audio %s --json %s --model_src %s --wave_dst %s --index %u" $audio $json $model $wave_dst $i)

	eval $test_sample

done
