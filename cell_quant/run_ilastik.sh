#!/bin/bash
for i in $(find /athena/listonlab/scratch/dje4001/FosTRAP2xThy1YFPH_TMT_titration_experiment_converted_images/ -type d -name '*MIP488*');
do
	echo $i
	ilp="488"
	sbatch --mem=50G --partition=scu-cpu  --job-name=ilastik_segment --wrap="bash ~/CellQuant/ilastik.sh '$i' $ilp"
done 

for i in $(find /athena/listonlab/scratch/dje4001/FosTRAP2xThy1YFPH_TMT_titration_experiment_converted_images/ -type d -name '*MIP594*');
do
        echo $i
        ilp="594"
        sbatch --mem=50G --partition=scu-cpu  --job-name=ilastik_segment --wrap="bash ~/CellQuant/ilastik.sh '$i' $ilp"
done

