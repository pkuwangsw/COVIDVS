#!/bin/bash
for i in `seq 0 19`
do
    python finetune.py --gpu 0 --data_path ./dataset/finetunev1.csv --features_path ./dataset/finetunev1-feat.npy --save_dir covidvs2/ftmodel_ffnlayer_fold_$i --seed $i --checkpoint_path covidvs1/fold_$i/model_0/model.pt --split_sizes 0.9 0.1 0.0 --config_path hyperopt_it20.json --dataset_type classification --init_lr 1e-4 --batch_size 20 --epochs 30 
done