#!/usr/bin/env python3

# import modules
import os
import sys
import json
import glob
import re
import nibabel as nib

#takes one argument (path to multiecho folder)



bids_dir = sys.argv[1]
multiecho_dir = glob.glob(f'{bids_dir}/**/anat',recursive=True)[0]
print('multi-echo corrector')
print(multiecho_dir)

#puts all json and nifti files in the folder into lists
json_files = sorted(glob.glob(multiecho_dir + "/*echo-*_*M*RAGE*.json"))
nifti_files = sorted(glob.glob(multiecho_dir + "/*echo-*_*M*RAGE*.nii.gz" ))
print(json_files)
print(nifti_files)
for i,k in zip(json_files, nifti_files):
    
    #open and load json file    
    with open(i) as data_file:
        data = json.load(data_file)
    
    #in the case of echo-1, the EchoNumber tag does not exist in the json file    
    if ("EchoNumber" not in data) and ("_echo_" in i):
        js_addEchoNum = re.sub("_echo_", "_echo-1_", i)
        js_changeEnding = re.sub("[0-9].json", ".json", js_addEchoNum)
        print('renaming: '+i+' to '+js_changeEnding)
        os.rename(i, js_changeEnding)
        
        ni_addEchoNum = re.sub("_echo_", "_echo-1_", k)
        ni_changeEnding = re.sub("[0-9].nii.gz", ".nii.gz", ni_addEchoNum)
        print('renaming: '+k+' to '+ni_changeEnding)
        os.rename(k, ni_changeEnding)
    
    #otherwise get EchoNumber value from json file and insert into filename
    elif "EchoNumber" in data:
        echonum = data["EchoNumber"]

        js_addEchoNum = re.sub("_echo_", "_echo-" + str(echonum) + "_", i)
        js_changeEnding = re.sub("[0-9].json", ".json", js_addEchoNum)
        print('renaming: '+i+' to '+js_changeEnding)
        os.rename(i, js_changeEnding)
        
        ni_addEchoNum = re.sub("_echo_", "_echo-" + str(echonum) + "_" , k)
        ni_changeEnding = re.sub("[0-9].nii.gz", ".nii.gz", ni_addEchoNum)
        print('renaming: '+k+' to '+ni_changeEnding)
        os.rename(k, ni_changeEnding)


#combine echos 1 and 2 for memprage
json_files = sorted(glob.glob(multiecho_dir + "/*echo-1_*MEMPRAGE.json"))
nifti_files_echo1 = sorted(glob.glob(multiecho_dir + "/*echo-1_*MEMPRAGE.nii.gz"))
nifti_files_echo2 = sorted(glob.glob(multiecho_dir + "/*echo-2_*MEMPRAGE.nii.gz"))

for i,in_json in enumerate(json_files):
    echo1 = nifti_files_echo1[i]
    echo2 = nifti_files_echo2[i]

    out_json = re.sub('_echo-[0-9]+_','_',in_json)
    out_json = re.sub('acq-([0-9a-zA-Z]+)4e_','acq-\g<1>AvgEcho12_',out_json)
    out_json = re.sub('_MEMPRAGE\.','_T1w.',out_json)
    out_nii = re.sub('\.json','.nii.gz',out_json)

   #open and load json file    
    with open(in_json) as data_file:
        data = json.load(data_file)

    #remove EchoNumber and EchoTime from JSON
    del data['EchoNumber']
    del data['EchoTime']
    data['EchoNumbers'] = [1,2]

    with open(out_json, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    #average the two niftis
    echo1_nib = nib.load(echo1)
    echo2_nib = nib.load(echo2)

    echo1_vol = echo1_nib.get_fdata()
    echo2_vol = echo2_nib.get_fdata()

    avg_vol = (echo1_vol + echo2_vol) * 0.5

    avg_nib = nib.Nifti1Image(avg_vol, echo1_nib.affine, echo1_nib.header)
    
    nib.save(avg_nib,out_nii)





     


