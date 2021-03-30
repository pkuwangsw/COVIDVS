# **COVIDVS**

This repository contains COVID-19-related Virtual Screening models (COVIDVS) for screening novel anti-SARS-CoV-2 drugs from large compound database.

## **Introduction**
COVIDVS models are Chemprop models trained with anti-beta-coronavirus actives/inactives collected from published papers and fine-tuned with anti-SARS-CoV-2 actives/inactives. 

## **Requirement**
COVIDVS model is a Python program developing with Ubuntu 18.04 operating system. RDKit package was used to deal with compounds and generate descriptors for molecules. Chemprop package was used to train COVIDVS model and make prediction for large compound libraries. GPU was recommended to speed the prediction process, especially for large compound libraries. 

Users can use the following commands to configure the environment:
```
conda install -c conda-forge rdkit
pip install git+https://github.com/bp-kelley/descriptastorus
pip install chemprop
```

More details about Chemprop can be found at: https://github.com/chemprop/chemprop.

\*Note: Instead of the chemprop package, we used the source codes of chemprop to develop our COVIDVS models, which can be found in: `chemprop` directory.

## **Dataset**
1. traindata.csv: A set of inhibitors against HCoV-OC43, SARS-CoV and MERS-CoV collected from literatures. All the inhibitors were identified by screening libraries including FDA-approved drugs and pharmacologically active compounds. This primary training dataset (Training Set 1) contains 90 positive data and 1862 negative data.

2. launched.csv: Contain 1417 launched drugs extracted from the Drug Repurposing Hub. There is no overlap with Training Set 1. 

3. finetunev1.csv: This dataset (Fine-tuning Set 1) contains 154 data collocted from literatures, including 70 positive data and 84 negative data. The molecular activities against SARS-CoV-2 of these molecules have been experimentally tested. 

4. testset.csv: This dataset (Test Set 1) was derived from Fine-tuning Set 1 by removing repeated molecules in Training Set 1. 

5. finetunev2.csv: This dataset (Fine-tuning Set 2) constructed by adding all the ReFRAME actives to the Fine-tuning Set 1. The ReFRAME actives were experimentally screened from ReFRAME library. 

6. drugRepurposingHub.csv: Drug Repurposing Hub library. This dataset was downloaded from https://clue.io/repurposing. Compounds overlapping with the training dataset were removed and the rest compounds were used to screen potential antivirals.

7. reframeactives.csv: Active compounds experimentally screened from the ReFRAME library. Molecules that already exist in training set or fine-tuning set have been removed. Data were collected from literature: "Discovery of SARS-CoV-2 antiviral drugs through large-scale compound repurposing". 

8. zinc_example.csv: A small library containing 10000 drug-like ZINC compounds. It can be used as an example to test our COVIDVS model.

All \*.npy files are pre-computed descriptors for each of the above dataset, which can accelerate the training and predicting process. "rdkit_2d_normalized" feature was used here. A python script `generatorFeatures.py` is provided to generate the descriptors from .csv file containing molecule information. 

If the .csv file only contains SMILES:
```
python generatorFeatures.py ../data/traindata.csv ../data/traindata-feat.npy 0
```
If the .csv file contains molecular name and SMILES:
```
python generatorFeatures.py ../data/reframeactives.csv ../data/reframeactives-feat.npy 1
```
## **Hyperparameter Optimization**
Hyperparameter optimization was run as:
```
python hyperparameter_optimization.py --gpu 0 --data_path ../data/traindata.csv --features_path ../data/traindata-feat.npy --no_features_scaling --dataset_type classification  --num_iters 20 --config_save_path hyperopt_it20.json 
```
The hyperparameters used in our work was saved in file: `hyperopt_it20.json`.

## **Train**
### COVIDVS-1
COVIDVS-1 model was trained with `traindata.csv` dataset: 
```
python train.py --gpu 0 --data_path ./dataset/traindata.csv --features_path ./dataset/traindata-feat.npy --no_features_scaling --save_dir covidvs1/ --dataset_type classification --split_sizes 0.9 0.1 0.0 --num_folds 20 --config_path hyperopt_it20.json 
```
The trained COVIDVS-1 model will be saved in the directory `covidvs1` and will be used for fine-tuning COVIDVS-2 and COVIDVS-3.

### COVIDVS-2
COVIDVS-2 model was obtained by fine-tuning COVIDVS-1 model with Fine-tuning Set 1. 
For example:
```
python finetune.py --gpu 0 --data_path ../data/finetunev1.csv --features_path ./dataset/finetunev1-feat.npy --save_dir covidvs2/ --checkpoint_path covidvs1/fold_0/model_0/model.pt --split_sizes 0.9 0.1 0.0 --config_path hyperopt_it20.json --dataset_type classification --init_lr 1e-4 --batch_size 20 --epochs 30
```
Because COVIDVS-1 is an ensemble of 20 models, the COVIDVS-2 model was actually fine-tuned through the below script:
```
#!/bin/bash
for i in `seq 0 19`
do
    python finetune.py --gpu 0 --data_path ./dataset/finetunev1.csv --features_path ./dataset/finetunev1-feat.npy --save_dir covidvs2/ftmodel_ffnlayer_fold_$i --seed $i --checkpoint_path covidvs1/fold_$i/model_0/model.pt --split_sizes 0.9 0.1 0.0 --config_path hyperopt_it20.json --dataset_type classification --init_lr 1e-4 --batch_size 20 --epochs 30 
done
```

### COVIDVS-3
COVIDVS-3 model was obtained by fine-tuning COVIDVS-1 model with Fine-tuning Set 2.
The training process is the same to COVIDVS-2.

## **Prediction**
We can applied our COVIDVS model to predict molecule's anti-SARS-CoV-2 activity. Users only need to prepare the input files that containing SMILES representation of molecules. For example:
```
python predict.py --gpu 0 --test_path ./dataset/launched.csv --features_path ./dataset/launched-feat.npy --preds_path preds_covidvs1_launched.csv --checkpoint_dir covidvs1/ --use_compound_names
```

The molecular features can be generated during the prediction process, for example:
```
python predict.py --gpu 0 --test_path ./dataset/zinc-druglike/zinc_druglike_1.csv --features_generator rdkit_2d_normalized --no_features_scaling --preds_path preds_covidvs3_zinc1.csv --checkpoint_dir covidvs3/ --use_compound_names
```
For large molecular library, for example ZINC15 database, we recommend users use the pre-computed descriptors to perform prediction process, which can be generated with `generatorFeatures.py`.

## **Acknowledgement**
This project incorporates code from the following repo:

+ https://github.com/chemprop/chemprop


