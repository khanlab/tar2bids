#!/usr/bin/python3

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
json_files = sorted(glob.glob(multiecho_dir + "/*magnitude?.json"))
nifti_files = sorted(glob.glob(multiecho_dir + "/*magnitude?.nii.gz"))
print(json_files)
print(nifti_files)
for i,k in zip(json_files, nifti_files):
    
    #open and load json file    
    with open(i) as data_file:
        data = json.load(data_file)

    #since need to swap names, first write to a diff file, then rename afterwards
    
    #in the case of echo-1, the EchoNumber tag does not exist in the json file    
    if ("EchoNumber" not in data):
        js_addEchoNum = re.sub("magnitude[1-9]", "magnitudetemp1", i)
        print('renaming: '+i+' to '+js_addEchoNum)
        os.rename(i, js_addEchoNum)
        
        ni_addEchoNum = re.sub("magnitude[1-9]", "magnitudetemp1", k)
        print('renaming: '+k+' to '+ni_addEchoNum)
        os.rename(k, ni_addEchoNum)

   
    #otherwise get EchoNumber value from json file and insert into filename
    else:
        echonum = data["EchoNumber"]
        
        js_addEchoNum = re.sub("magnitude[1-9]", "magnitudetemp" + str(echonum), i)
        print('renaming: '+i+' to '+js_addEchoNum)
        os.rename(i, js_addEchoNum)
        
        ni_addEchoNum = re.sub("magnitude[1-9]", "magnitudetemp" + str(echonum), k)
        print('renaming: '+k+' to '+ni_addEchoNum)
        os.rename(k, ni_addEchoNum)
       

#now with ordering corrected, rename from magnitudetemp to magnitude
json_files = sorted(glob.glob(multiecho_dir + "/*magnitudetemp?.json"))
nifti_files = sorted(glob.glob(multiecho_dir + "/*magnitudetemp?.nii.gz"))

for i,k in zip(json_files, nifti_files):
        js_fromtemp = re.sub("magnitudetemp", "magnitude", i)
        ni_fromtemp = re.sub("magnitudetemp", "magnitude", k)
        print('renaming: '+i+' to '+js_fromtemp)
        os.rename(i,js_fromtemp)
        print('renaming: '+k+' to '+ni_fromtemp)
        os.rename(k,ni_fromtemp)
