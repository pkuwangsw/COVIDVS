# COVIDVS
Dataset and scripts for a COVID19-related Virtual Screening (COVIDVS) model. 

## Introduction
This virtual screening model is a trained Chemprop model with anti-beta-coronavirus actives/inactives collected from published papers. 
Chemprop is avaiable at https://github.com/chemprop/chemprop.

Users can reproducted this work by training Chemprop model with the following workflows.

### COVIDVS-1
This model was trained with dataset/trainset1.csv. Hyperparameter optimization was firstly made via Bayesian optimization. Then the model was trained with 20 different random splits of trainset. The "rdkit_2d_normalized" features were used. Finally, we ensembled all the 20 models to an ensembling model and the final results are the average scores of 20 models.

### COVIDVS-2
This model was obtained by fine-tuning COVIDVS-1 model with dataset/finetuneset1.csv. Because there are only 154 data in finetune set 1, we freezed the weights of encoder layers in the fine-tune process to reduce the parameter space. Similarly, we fine-tuned each of the 20 models in COVIDVS-1 and ensembled them as COVIDVS-2 model.

### COVIDVS-3
This model was obtained by fine-tuning COVIDVS-1 model with dataset/finetuneset2.csv. The training process is same to COVIDVS-2. 
