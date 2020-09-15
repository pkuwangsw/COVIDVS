#!/bin/bash
for i in `seq 0 19`
do
#	python train.py --gpu 1 --data_path dataset_canonical/finetunedatav3.csv --features_path dataset_canonical/finetunedatav3-feat.npy --save_dir ftmodelv3_ffnlayer_fold_$i --seed $i --save_smiles_splits --checkpoint_path model_finalcv20/fold_$i/model_0/model.pt --split_sizes 0.9 0.1 0.0 --config_path hyperopt_it20.json --dataset_type classification --init_lr 1e-4 --batch_size 20 --epochs 30
	python finetune.py --gpu 2 --data_path dataset_canonical/finetunedatav3.csv --features_path dataset_canonical/finetunedatav3-feat.npy --save_dir ftmodelv3_ffnlayer_try2/ftmodelv3_ffnlayer_fold_$i --seed $i --save_smiles_splits --checkpoint_path model_finalcv20/fold_$i/model_0/model.pt --split_sizes 0.9 0.1 0.0 --config_path hyperopt_it20.json --dataset_type classification --init_lr 1e-4 --batch_size 20 --epochs 30
done
