#!/usr/bin/python3

import os
import sys
import json
import glob
import re
import nibabel as nib
import numpy as np

#takes one argument 


bids_dir = sys.argv[1]


def zero_pad(m):
    number = m.group(1)
    return m.group(1) + m.group(2).zfill(4) + m.group(3)

#first, rename all vnav files to have leading zeros
for vnav in glob.glob(f'{bids_dir}/**/*_vNav[1-9]*.*',recursive=True):
    new_vnav = re.sub(r'(.*_vNav)([0-9]+)(\..+)',zero_pad,vnav)
    os.rename(vnav,new_vnav)
#    print(vnav)
#    print(new_vnav)



#now, we want to merge the nii.gz and json files
#find first vnav file for each run
for vnav in glob.glob(f'{bids_dir}/**/*_vNav0001.nii.gz',recursive=True):
     #get sorted list of all related vnav files:

    #regex to get the prefix
    # and use that to find all the files
    prefix = re.split('vNav0001',vnav)[0]
    all_nii = sorted(glob.glob(prefix+'vNav*.nii.gz'))
    N = len(all_nii)
    #print(all_nii)
    #print(N)

    vnav_4d = prefix + 'vNav.nii.gz'
    init_nib = nib.load(all_nii[0])
    vol_3d = init_nib.get_fdata() #1st nii is 2 vols 
    #print(vol_3d.shape)
    vol_4d = np.zeros((vol_3d.shape[0],vol_3d.shape[1],vol_3d.shape[2],N))
    #print(vol_4d.shape)

    for i,nii in enumerate(all_nii):
        #print(nii)
        #print(i)
        vol = nib.load(nii).get_fdata()
        if vol.ndim==4:
            vol_4d[:,:,:,i] = vol[:,:,:,0]
        else:
            vol_4d[:,:,:,i] = vol[:,:,:]
       
 
    #move all other files to sourcedata
    print('moving vnav files to sourcedata/vNav, replacing with:')
    print(vnav_4d)
    
    #create vNav folder in sourcedata:
    from pathlib import Path
    Path(os.path.join(bids_dir,'sourcedata','vNav')).mkdir(
        parents=True, exist_ok=True)

    for f in glob.glob(prefix + 'vNav????.*'):
        (head,tail) = os.path.split(f)
        os.rename(f,os.path.join(bids_dir,'sourcedata','vNav',tail))   
   
    #save new 4d file
    nib_4d = nib.nifti1.Nifti1Image(vol_4d, init_nib.affine)
    nib_4d.to_filename(vnav_4d)



