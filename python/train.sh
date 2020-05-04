#!/bin/bash

audio="/media/fgrondin/Scratch/steernet/meta/train_audio.meta"
json="json/features.json"
model_dir="/media/fgrondin/Scratch/steernet/model/"

model_dst=$(printf "%s000.bin" $model_dir)
train_init=$(printf "python3 train_init.py --json %s --model_dst %s" $json $model_dst)

eval $train_init

for i in {1..100}
do
	
	model_src=$(printf "%s%03u.bin" $model_dir $(($i-1)))
	model_dst=$(printf "%s%03u.bin" $model_dir $i)

	train_epochs=$(printf "python3 train_epochs.py --audio %s --json %s --model_src %s --model_dst %s" $audio $json $model_src $model_dst)

	eval $train_epochs

done
