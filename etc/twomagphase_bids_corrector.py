#!/usr/bin/python

# import modules
import os
import sys
import json
import glob
import re

#takes one argument (path to fmap folder)



fmap_dir = sys.argv[1]
print('two magphase fieldmap corrector')
print(fmap_dir)

#puts all json and nifti files in the folder into lists
json_files = sorted(glob.glob(fmap_dir + "/*twomagphase?.json"))
nifti_files = sorted(glob.glob(fmap_dir + "/*twomagphase?.nii.gz"))
print(json_files)
print(nifti_files)
for i,k in zip(json_files, nifti_files):
    
    #open and load json file    
    with open(i) as data_file:
        data = json.load(data_file)

    if data['ImageType'][-1] == 'PHASE':
        imtype = 'phase'
    else:
        imtype = 'magnitude'

    echonum = data['EchoNumber']

    js_newname = re.sub("twomagphase[1-9]", "{imtype}{echonum}".format(imtype=imtype,echonum=echonum),i)
    print('renaming: '+i+' to '+js_newname)
    os.rename(i, js_newname)
        
    ni_newname = re.sub("twomagphase[1-9]", "{imtype}{echonum}".format(imtype=imtype,echonum=echonum),k)
    print('renaming: '+k+' to '+ni_newname)
    os.rename(k, ni_newname)

