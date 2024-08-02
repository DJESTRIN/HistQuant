#!/bin/bash
cd C:/Users/Estrin/OneDrive/Desktop/LISTON_LAB/PL_ITBS/test/

for file_dir in *.{tif,tiff}
do
C:/Users/Estrin/Fiji.app/ImageJ-win64.exe --headless --console -macro C:/Users/Estrin/Fiji.app/preproc.ijm "$file_dir"
done
