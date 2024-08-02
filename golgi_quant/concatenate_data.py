# -*- coding: utf-8 -*-
"""Concatenate Data across excel sheets"""
import os,glob
import pandas as pd
import numpy as np
import xlrd

"""concatXLS class: loads data from xls files with similar sheets and concatonates the data
    output for each sheet name will be seperate xls file. """
class concatXLS:
    def __init__(self, excelfile_oh):
        xls = xlrd.open_workbook(excelfile_oh, on_demand=True)
        self.sheet_names=xls.sheet_names()
        print(self.sheet_names)
        self.all_xls={}
        for u in self.sheet_names:
            self.all_xls[u]=pd.DataFrame()
        self.counter=0

    def add_data(self, excelfile_oh):
        # Parse filename
        try:
            base,extension=excelfile_oh.split('.')
            cage, group, animal, brainside, slide, scan, region, neuron, layer = base.split('_')
            neuronid = cage+animal+slide+scan+region+neuron+layer
            xls=pd.ExcelFile(excelfile_oh)
        except:
            print("error with filename:" + excelfile_oh)
        
        # Add the data to sheet dataframe
        for sheet in self.sheet_names:
            try:
                df_oh=pd.read_excel(xls,sheet)
                
                #Add animal info to data
                df_animalinfo=pd.DataFrame({'cage':np.repeat(cage,df_oh.shape[0],0),
                                'group':np.repeat(group,df_oh.shape[0],0),
                                'animal':np.repeat(animal,df_oh.shape[0],0),
                                'neuronid':np.repeat(neuronid,df_oh.shape[0],0),
                                'layer':np.repeat(layer,df_oh.shape[0],0)})
                
                df_cat=pd.concat([df_oh,df_animalinfo],axis=1)
                self.all_xls[sheet]=pd.concat([self.all_xls[sheet],df_cat],axis=0)

            except:
                print(str(sheet)+" does not exist or something else went wrong")
                
    def output_data(self,output_directory):
        try:
            os.chdir(output_directory)
            for u in self.sheet_names:
                string=u+".xlsx"
                self.all_xls[u].to_excel(string)
            
        except:
            print("error with saving")
            
            
            
""" CONCATENATE CELL BODY DATA"""
os.chdir('F:\\LISTON_LAB\\DENDRITIC_SPINE_PROJECT\\neurolucida_anlaysis_golgi\\neurolucida_generated_data\\cellbody\\')
xls_files=glob.glob('*xls*')
data=concatXLS(xls_files[0])
        
for excelfile_oh in glob.glob('*xls*'):
    print(excelfile_oh)
    data.add_data(excelfile_oh)

data.output_data('F:\\LISTON_LAB\\DENDRITIC_SPINE_PROJECT\\neurolucida_anlaysis_golgi\\neurolucida_generated_data\\output\\cellbody\\')


""" CONCATENATE DENDRITE DATA """
os.chdir('F:\\LISTON_LAB\\DENDRITIC_SPINE_PROJECT\\neurolucida_anlaysis_golgi\\neurolucida_generated_data\\dendrites\\')
xls_files=glob.glob('*xls*')
data=concatXLS(xls_files[0])
        
for excelfile_oh in glob.glob('*xls*'):
    print(excelfile_oh)
    data.add_data(excelfile_oh)

data.output_data('F:\\LISTON_LAB\\DENDRITIC_SPINE_PROJECT\\neurolucida_anlaysis_golgi\\neurolucida_generated_data\\output\\dendrites\\')
        




