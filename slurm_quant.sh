#!/bin/bash
cd /athena/listonlab/scratch/dje4001/FosTRAP2xThy1YFPH_TMT_titration_experiment_converted_images
for i in $(find . -type d ! -name '*MIP*' -name '*_*'); do # Not recommended, will break on whitespace
    sbatch --mem=50G --partition=scu-cpu  --job-name=tile_images --wrap="bash ~/CellQuant/run_quant.sh '$i'"
done
