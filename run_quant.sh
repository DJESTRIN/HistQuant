#!/bin/bash
image_folder=$1
source ~/.bashrc
conda activate ~/anaconda3/envs/spyder
python ~/CellQuant/TitrationHistology.py --input_directory $image_folder
