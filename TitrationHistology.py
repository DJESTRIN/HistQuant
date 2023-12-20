#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 11:46:01 2023

@author: dje4001
"""

import os,glob
import skimage.io
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import ipdb
import tqdm
import argparse
Image.MAX_IMAGE_PIXELS=10000000000

def tile_MIP(array,block_size,save_dir):
    nrow,ncol=np.shape(array)
    xs=range(0,nrow-nrow%block_size,block_size)
    ys=range(0,ncol-ncol%block_size,block_size)
    for start_x, stop_x in zip(xs[:-1],xs[1:]):
        for start_y, stop_y in zip(ys[:-1],ys[1:]):
            tiled_image=array[start_x:stop_x,start_y:stop_y]
            filename=save_dir+"Image_"+str(start_x)+"_"+str(stop_x)+"_"+str(start_y)+"_"+str(stop_y)+".tif"
            img_oh=Image.fromarray(tiled_image)
            img_oh.save(filename)

def main(input_directory):
    #Max Inensity Projection GFP
    search_string=input_directory+"/*488*.tif"
    images=glob.glob(search_string)
    for i,image in tqdm.tqdm(enumerate(images),total=len(images)):
        image_oh=Image.open(image).convert('L')
        image_oh=np.asarray(image_oh)
        if i==0:
            max_image=image_oh
        else:
            max_image=np.maximum(max_image,image_oh) 
    
    #Tile the MIP for ilastik
    tiled_dir=input_directory+"/MIP488_tiled/"
    if not os.path.exists(tiled_dir):
        os.mkdir(tiled_dir)
    tile_MIP(max_image,10000,tiled_dir)
    
    #Max Inensity Projection tdtomato
    search_string=input_directory+"/*594*.tif"
    images=glob.glob(search_string)
    for i,image in tqdm.tqdm(enumerate(images),total=len(images)):
        image_oh=Image.open(image).convert('L')
        image_oh=np.asarray(image_oh)
        if i==0:
            max_image=image_oh
        else:
            max_image=np.maximum(max_image,image_oh) 
    
    #Tile the MIP for ilastik
    tiled_dir=input_directory+"/MIP594_tiled/"
    if not os.path.exists(tiled_dir):
        os.mkdir(tiled_dir)
    tile_MIP(max_image,10000,tiled_dir)
    

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('--input_directory',type=str)
    args=parser.parse_args()
    main(args.input_directory)