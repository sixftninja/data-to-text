# Data-to-Text [![PWC](https://img.shields.io/endpoint.svg?url=https://paperswithcode.com/badge/a-hierarchical-model-for-data-to-text/data-to-text-generation-on-rotowire)]

## Install packages and create env
#### Debian Packages:
1. `sudo apt-get update`
2. `sudo apt-get install bzip2 git libxml2-dev`

#### Miniconda (To save disk space:)
1. `wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh`
2. `bash Miniconda3-latest-Linux-x86_64.sh`
3. `rm Miniconda3-latest-Linux-x86_64.sh`
4. `source .bashrc`


#### Conda environment:
1. `conda create --name <name_of_environment> python==3.7`
2. `conda activate <name_of_environment>`
3. `conda install pytorch=1.1.0 cudatoolkit=9.0 -c pytorch`
4. `pip install torchtext==0.4`
5. `pip install torchvision==0.3.0`
6. `pip install scikit-learn pandas jupyter ipython`
7. `pip install more-itertools`

## Load Data

1. Add your data folder to /data-to-text/data
2. Make changes to `make-dataset.py` to read your data
3. Be sure to change `ENT_SIZE`
4. Max `ENT_SIZE` tested is 244. You can try higher but I can't say where exactly it'll break.
5. Change the ENT_SIZE in `onmt/__init.py__`

`python data/make-dataset.py --folder data/ --dataset <your data folder name here>`

## Experiments
`python create-experiment.py --name exp-1`

## Preprocess
`python preprocess.py --config preprocess.cfg`

## Training
`python train.py --config train.cfg`

_(if you want to train for more than 30000 steps, modify lines 79 and 80 in train.cfg)_

_(for multiple GPUs modify line 64 in train.cfg)_

## Translation
#### Average Checkpoints:
`python average-checkpoints.py --folder exp-1 --steps 26000 27000 28000 29000 30000`

#### Translate
`python translate.py --config translate.cfg`

## Evaluation
You can get the BLUE score by running:

`cat experiments/exp-1/gens/test/predictions.txt | sacrebleu --force data/test_output.txt`




