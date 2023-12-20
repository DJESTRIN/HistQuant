#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 13:16:06 2023

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
image="/athena/listonlab/scratch/dje4001/FosTRAP2xThy1YFPH_TMT_titration_experiment_converted_images/Cage_3713070_A_1004/Cage 3713070 A 1004_Alexa594_0.tif"
image_oh=Image.open(image)
_,image_oh,_=image_oh.split()
plt.imshow(image_oh,cmap="gray")