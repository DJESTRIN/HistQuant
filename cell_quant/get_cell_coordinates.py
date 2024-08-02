#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Pasre ilastik output """

import argparse
import glob
import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label
from PIL import Image
import random
import tqdm
from multiprocessing import Pool
import ipdb
    
def main (np_path):
    #Import numpy array
    data=np.load(np_path)
    
    #Threshold cell body counts segmentation channel
    try:
        data=data[:,:,0]
    except:
        data=data[:,:]
        
    data[data<=0.8]=0
    data[data>0.8]=1
    print("finding blobs")
    blobs=label(data)
    return data,blobs


def plot_blobs(path_to_npy,blobs):
    """ Plot the orginal image along with defined blobs """
    print("Generating plot")
    im_path,_=path_to_npy.split('_Prob')
    filename=im_path+'output.pdf'
    im_path+='.tif'
    im_oh=np.asarray(Image.open(im_path))
    plt.figure(figsize=(10,10))
    plt.imshow(im_oh,cmap='gray')
    plt.imshow(blobs,cmap='nipy_spectral',alpha=0.5)
    plt.savefig(filename)
    return

def threshold_blobs(blobs,minthreshold,maxthreshold):
    print("Thresholding blob areas")
    areas=[]
    for hypo_cell in tqdm.tqdm(np.unique(blobs)[1:]):
        coordinates=np.where(blobs==hypo_cell)[0]
        area=len(coordinates)*len(coordinates)
        if area<minthreshold or area>maxthreshold:
            blobs[np.where(blobs==hypo_cell)]=0
        areas.append(area)
    return blobs,np.asarray(areas) 

def locate_cells(npy_path,blobs):
    """ Saves average cell coordinates to csv file"""
    cell_ids=np.unique(blobs)
    if len(cell_ids)<=1:
        return
    else:
        _,file=npy_path.split('Image_')
        x,_,y,_,_=file.split('_')
        x,y=float(x),float(y)
        corrected_coordinates=[]
        for cell in cell_ids[1:]:
            coords=np.where(blobs==cell)
            coords=np.asarray(coords)
            xoh,yoh=coords.mean(axis=1)
            xoh+=x
            yoh+=y
            corrected=np.array([xoh,yoh])
            corrected_coordinates.append(corrected)
        corrected_coordinates=np.asarray(corrected_coordinates)
        filename,_=npy_path.split('.npy')
        filename+='coordinates.npy'
        np.save(filename,corrected_coordinates)
        return

def sanity_check(search_path,searches,channel):
    """
    search path -- full path to npy files containing relevant wild cards
    searches -- the number of randomly pulled images plotted for validation
    """
    if '594'in channel:
        minthreshold=100000
        maxthreshold=1000000
    elif '488' in channel:
        minthreshold=100000
        maxthreshold=1000000
        
    npy_files=glob.glob(search_path)
    npy_files_oh=random.sample(npy_files,searches)
    for npy_path in npy_files_oh:
        image,blobs=main(npy_path)
        blobs,areas=threshold_blobs(blobs,minthreshold,maxthreshold)
        locate_cells(npy_path,blobs)
        plot_blobs(npy_path,blobs)
        
    return

def runit(search_path,channel):
    """
    search path -- full path to npy files containing relevant wild cards
    searches -- the number of randomly pulled images plotted for validation
    """
    if 'MIP594'in channel:
        minthreshold=100000
        maxthreshold=1000000
    elif 'MIP488' in channel:
        minthreshold=100000
        maxthreshold=1000000
        
    npy_files=glob.glob(search_path)
    for npy_path in npy_files:
        image,blobs=main(npy_path)
        blobs,areas=threshold_blobs(blobs,minthreshold,maxthreshold)
        locate_cells(npy_path,blobs) 
        plot_blobs(npy_path,blobs)
    return

#search_string="/athena/listonlab/scratch/dje4001/FosTRAP2xThy1YFPH_TMT_titration_experiment_converted_images/**/MIP594_tiled/*.npy"
#sanity_check(search_string,15,'MIP594')


#main function / command line interface
if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_directory", type=str)
    args = parser.parse_args()
    search_path=args.input_directory+'/*.npy'
    print(search_path)
    runit(search_path,args.input_directory)



