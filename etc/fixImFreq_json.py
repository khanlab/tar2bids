#!/usr/bin/python3

# import modules
import os
import sys
import json
import glob
import re

#takes two arguments: path to multiecho folder, and ImagingFrequency


multiecho_dir = sys.argv[1]
im_freq=sys.argv[2]



print('imfreq corrector')
print(multiecho_dir)

#puts all json and nifti files in the folder into lists
json_files = sorted(glob.glob(multiecho_dir + "/*GRE.json"))
print(json_files)



for i in json_files:
    
    #open and load json file    
    with open(i,'r') as data_file:
        data = json.load(data_file)
        data["ImagingFrequency"]=im_freq

    with open(i,'w') as data_file:
        json.dump(data,data_file,indent=4,ensure_ascii=False)
