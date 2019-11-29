#!/usr/bin/python

# import modules
import os
import sys
import json
import glob
import re

#takes one argument (path to sa2rage folder)



sa2rage_dir = sys.argv[1]
print('sa2rage corrector')
print(sa2rage_dir)

#puts all json and nifti files in the folder into lists
json_files = sorted(glob.glob(sa2rage_dir + "/*SA2RAGE[0-9]*.json"))
nifti_files = sorted(glob.glob(sa2rage_dir + "/*SA2RAGE[0-9]*.nii.gz"))
print(json_files)
print(nifti_files)
for js,ni in zip(json_files, nifti_files):
    
    #open and load json file    
    with open(js) as data_file:
        json_data = json.load(data_file)

    #need to make odd numbered SA2RAGE files as magnitude, and even as phase
    #get SA2RAGE number
    m=re.findall("(\d{1,2})(?:\.json)",js)
    if ( int(m[0]) % 2 == 0):
            js_renameComplex = re.sub("_inv-","_part-mag_inv-",js)
            ni_renameComplex = re.sub("_inv-","_part-mag_inv-",ni)
    else:
            js_renameComplex = re.sub("_inv-","_part-phase_inv-",js)
            ni_renameComplex = re.sub("_inv-","_part-phase_inv-",ni)
    js_changeEnding = re.sub("SA2RAGE.*", "SA2RAGE.json", js_renameComplex)
    ni_changeEnding = re.sub("SA2RAGE.*", "SA2RAGE.nii.gz", ni_renameComplex)

    print('renaming: '+js+' to '+js_changeEnding)
    print('renaming: '+ni+' to '+ni_changeEnding)
    os.rename(js,js_changeEnding)
    os.rename(ni,ni_changeEnding)


