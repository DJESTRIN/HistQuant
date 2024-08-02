#!/bin/python
"Dependencies"
import os
import openslide
import numpy as np
from PIL import Image
import argparse
import ipdb
import tqdm

def mrxstotiff(input_dir):

    # Define the input and output directories
    output_dir = input_dir

    # Define the size of the tiles
    tile_size = 1000

    # Loop through all the .mrxs files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.mrxs'):
            # Open the file using OpenSlide
            slide = openslide.open_slide(os.path.join(input_dir, filename))
            
            # Get the dimensions of the slide
            width, height = slide.dimensions
        
            # Calculate the number of tiles in each dimension
            num_tiles_x = int(np.ceil(width / tile_size))
            num_tiles_y = int(np.ceil(height / tile_size))
        
            # Loop through all the tiles and save them as individual images
            for i in tqdm.tqdm(range(num_tiles_x)):
                for j in range(num_tiles_y):
                    # Calculate the coordinates of the current tile
                    x = i * tile_size
                    y = j * tile_size
                
                    # Get the tile image
                    tile = slide.read_region((x, y), 0, (tile_size, tile_size))
                    tile=255-tile
                
                    # Save the tile as a TIFF file
                    tile_filename = f'{os.path.splitext(filename)[0]}_{i}_{j}.tiff'
                    fulldrop_path=output_dir+'/'+filename[:-5]+'tiled_images/'
                    fulldrop=fulldrop_path+tile_filename
                    #Generate an output subfolder for tiles
                    try:
                        os.mkdir(fulldrop_path)
                    except:
                        nothing=1
                    
                    tile.save(fulldrop, format='TIFF')
        
            # Close the slide file
            slide.close()
            
if __name__=="__main__":
    # Command line interface
    parser = argparse.ArgumentParser(description="Convert a .mrxs file to a 500 x 500 tile .TIFF file")
    parser.add_argument("--input", type=str, help="The directory containing the input mrxs files",required=True)
    #parser.add_argument("--output", type=str, help="The directory containing the output tiff files",required=False)
    args = parser.parse_args()
    mrxstotiff(args.input)
