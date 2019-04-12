#!/usr/bin/python

# import modules
import os
import sys
import json
import glob
import re

#takes one argument (path to multiecho folder)



multiecho_dir = sys.argv[1]
print('multi-echo corrector')
print(multiecho_dir)

#puts all json and nifti files in the folder into lists
json_files = sorted(glob.glob(multiecho_dir + "/*bold[0-9]*.json"))
nifti_files = sorted(glob.glob(multiecho_dir + "/*bold[0-9]*.nii.gz"))
print(json_files)
print(nifti_files)
for i,k in zip(json_files, nifti_files):
    
    #open and load json file    
    with open(i) as data_file:
        data = json.load(data_file)
    
    #in the case of echo-1, the EchoNumber tag does not exist in the json file    
    if ("EchoNumber" not in data) and ("_bold" in i):
        js_addEchoNum = re.sub("_bold", "_echo-01_bold", i)
        js_changeEnding = re.sub("bold.*", "bold.json", js_addEchoNum)
        print('renaming: '+i+' to '+js_changeEnding)
        os.rename(i, js_changeEnding)
        
        ni_addEchoNum = re.sub("_bold", "_echo-01_bold", k)
        ni_changeEnding = re.sub("bold.*", "bold.nii.gz", ni_addEchoNum)
        print('renaming: '+k+' to '+ni_changeEnding)
        os.rename(k, ni_changeEnding)
    
    #otherwise get EchoNumber value from json file and insert into filename
    elif "EchoNumber" in data:
        echonum = data["EchoNumber"]
        
        js_addEchoNum = re.sub("_bold", "_echo-" + str(echonum) + "_bold", i)
        js_changeEnding = re.sub("bold.*", "bold.json", js_addEchoNum)
        print('renaming: '+i+' to '+js_changeEnding)
        os.rename(i, js_changeEnding)
        
        ni_addEchoNum = re.sub("_bold", "_echo-" + str(echonum) + "_bold", k)
        ni_changeEnding = re.sub("bold.*", "bold.nii.gz", ni_addEchoNum)
        print('renaming: '+k+' to '+ni_changeEnding)
        os.rename(k, ni_changeEnding)
