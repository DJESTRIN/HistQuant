#!/bin/python
"Dependencies"
import os
import argparse
import ipdb

def delete_spaces(directory):
    os.chdir(directory)
    a=3
    path = os.getcwd()
    filenames = os.listdir(path)
    for filename in filenames:
        ipdb.set_trace()
        os.rename(os.path.join(path,filename),os.path.join(path,filename.replace(' ','')))
        
if __name__=="__main__":
   # Command line interface
  parser = argparse.ArgumentParser(description="Remove spaces from filenames and folders ")
  parser.add_argument("--input", type=str, help="The directory containing the input mrxs files ",required=True)
  args = parser.parse_args()
  delete_spaces(args.input)
    
