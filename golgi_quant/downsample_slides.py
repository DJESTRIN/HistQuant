#!/usr/bin/env python3

''' this code downscales images using
openslide thumbnail feature '''

from openslide import open_slide
import openslide
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import os
import glob
#from openslide.deepzoom import DeepZoomGenerator
#import tqdm
import argparse
#import ipdb

def main(path):
    if path[-1]!="/":
        path=path+"/"
    #list of files that need to be downscaled
    files = glob.glob(path + '*.mrxs')
    #create new directory to add all the downscaled images
    directory = "downsampled_images_openslide"
    new_path = os.path.join(path, directory)
    if os.path.exists(new_path)==False:
        os.mkdir(new_path)
     
    #iterates through all the files
    for file in files:
        #opens the file
        slide = open_slide(file)
        
        # code can be changed so that the dimensions are scaled by a certain factor
        # the 600,600 size was temporary for testing
        
        # gets thumbnail of the image
        slide_downscaled = slide.get_thumbnail(size=(600,600))
        slide_downscaled_numpy = np.array(slide_downscaled)
        
        # creating file name
        filename = file.split('.')
        filename_new = filename[0].split('/')
        name = len(filename_new) - 1
        filename_final = filename_new[name] + "_downscaled"
        
        # saving the file
        plt.imsave(new_path + '/' + filename_final + ".tiff", slide_downscaled_numpy)
    
if __name__=='__main__':
    # command line interface
    parser = argparse.ArgumentParser(description="downscale .mrxs images to .tiff")
    parser.add_argument("input", type=str, help="the directory containing the input .mrxs files ")
    args = parser.parse_args()
    main(args.input)
