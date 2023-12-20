#!/bin/bash
folder=$1
ilp=$2

if [ "$ilp" == "488" ]; then
	ilp_file=/athena/listonlab/scratch/dje4001/FosTRAP2xThy1YFPH_TMT_titration_experiment_converted_images/ch488.ilp
elif [ "$ilp" == "594" ]; then
	ilp_file=/athena/listonlab/scratch/dje4001/FosTRAP2xThy1YFPH_TMT_titration_experiment_converted_images/ch594.ilp
else
	echo "err, ilp file wrong"
fi

for image in $(find $folder -type f -name '*.tif*');
do 
	echo $image
	/home/fs01/dje4001/Downloads/ilastik-1.4.0-Linux/run_ilastik.sh --headless --project=$ilp_file --output_format=numpy $image
done
