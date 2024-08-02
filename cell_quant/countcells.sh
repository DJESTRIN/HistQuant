#!/bin/bash
image_folder=$1
source ~/.bashrc
conda activate ~/anaconda3/envs/spyder
echo $image_folder
python ~/CellQuant/get_cell_coordinates.py --input_directory $image_folder

