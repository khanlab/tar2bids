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
json_files = sorted(glob.glob(multiecho_dir + "/*GRE[0-9]*.json"))
nifti_files = sorted(glob.glob(multiecho_dir + "/*GRE[0-9]*.nii.gz"))
print(json_files)
print(nifti_files)
for js,ni in zip(json_files, nifti_files):
    
    #open and load json file    
    with open(js) as data_file:
        json_data = json.load(data_file)

    #check if part-complex -- if so, then need to make odd numbered GRE files as real, and even as imag
    if ( "_part-complex_" in js ):
        #get GRE number
        m=re.findall("(\d{1,2})(?:\.json)",js)
        if ( int(m[0]) % 2 == 0):
            js_renameComplex = re.sub("_part-complex_","_part-imag_",js)
            ni_renameComplex = re.sub("_part-complex_","_part-imag_",ni)
        else:
            js_renameComplex = re.sub("_part-complex_","_part-real_",js)
            ni_renameComplex = re.sub("_part-complex_","_part-real_",ni)
        print('renaming: '+js+' to '+js_renameComplex)
        print('renaming: '+ni+' to '+ni_renameComplex)
        os.rename(js,js_renameComplex)
        os.rename(ni,ni_renameComplex)
        js=js_renameComplex
        ni=ni_renameComplex


    #in the case of echo-1, the EchoNumber tag does not exist in the json file    
    if ("EchoNumber" not in json_data) and ("_echo_" in js):
        js_addEchoNum = re.sub("_echo_", "_echo-1_", js)

        js_changeEnding = re.sub("_GRE[0-9]+\.json", "_GRE.json", js_addEchoNum)

        print('renaming: '+js+' to '+js_changeEnding)
        os.rename(js, js_changeEnding)
        
        ni_addEchoNum = re.sub("_echo_", "_echo-1_", ni)

        ni_changeEnding = re.sub("_GRE[0-9]+\.nii.gz", "_GRE.nii.gz", ni_addEchoNum)

        print('renaming: '+ni+' to '+ni_changeEnding)
        os.rename(ni, ni_changeEnding)
    
    #otherwise get EchoNumber value from json file and insert into filename
    elif "EchoNumber" in json_data:
        echonum = json_data["EchoNumber"]
        
        js_addEchoNum = re.sub("_echo_", "_echo-" + str(echonum) + "_", js)

        js_changeEnding = re.sub("_GRE[0-9]+\.json", "_GRE.json", js_addEchoNum)

        print('renaming: '+js+' to '+js_changeEnding)
        os.rename(js, js_changeEnding)
        
        ni_addEchoNum = re.sub("_echo_", "_echo-" + str(echonum) + "_", ni)

        ni_changeEnding = re.sub("_GRE[0-9]+\.nii.gz", "_GRE.nii.gz", ni_addEchoNum)

        print('renaming: '+ni+' to '+ni_changeEnding)
        os.rename(ni, ni_changeEnding)
