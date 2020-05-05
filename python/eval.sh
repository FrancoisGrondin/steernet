#!/bin/bash

audio="/media/fgrondin/Scratch/steernet/meta/dev_audio.meta"
json="json/features.json"
model_dir="/media/fgrondin/Scratch/steernet/model/"

for i in {0..100}
do
	
	model_src=$(printf "%s%03u.bin" $model_dir $i)

	eval_epochs=$(printf "python3 eval_epochs.py --audio %s --json %s --model_src %s" $audio $json $model_src)

	eval $eval_epochs

done
