#!/usr/bin/env python3

import sys
import numpy as np
import nibabel as nib
from glob import glob
import re
import os
import json

def usage():
  print('{}: <in_anat_dir> (containing part-imag and part-real images)'.format(sys.argv[0]))

if len(sys.argv)-1 < 1:
  usage()
  sys.exit(1)

in_anat_dir = sys.argv[1]


#get all imaginary images
imag_niis = sorted(glob(f'{in_anat_dir}/sub-*_part-imag_*.nii.gz'))
imag_jsons = [re.sub('(nii(.gz)*)','json',nii) for nii in imag_niis ]
real_niis = [re.sub('_part-imag_','_part-real_',nii) for nii in imag_niis ]

#make sure all niftis and json files exist
for in_file in imag_jsons + real_niis:
    if not os.path.exists(in_file):
        print(f'ERROR: {in_file} does not exist!')
        sys.exit(1)

#filename for output
phase_niis = [re.sub('_part-imag_','_part-phase_',nii) for nii in imag_niis ]
phase_jsons = [re.sub('_part-imag_','_part-phase_',json) for json in imag_jsons ]

for imag_nii,real_nii,imag_json,phase_nii,phase_json in zip(imag_niis, real_niis, imag_jsons,phase_niis,phase_jsons):

    imag_img = nib.load(imag_nii)
    real_img = nib.load(real_nii)

    print(f'Computing phase with Siemens dicom convention from {imag_nii} and {real_nii} as (arctan2(imag,real) / Pi +1 )*2048')
    phase = np.arctan2(imag_img.get_fdata(),real_img.get_fdata());
    phase = ((phase/np.pi) +1.0 )*2048;
    phase = nib.casting.float_to_int(phase, 'int16')

    print(f'Saving as {phase_nii}')
    phase_nib = nib.Nifti1Image(phase, real_img.affine, real_img.header)
    nib.save(phase_nib, phase_nii)

    print(f'Creating json from {imag_json}, replacing IMAGINARY with PHASE in image type, saving as {phase_json}')
    with open(imag_json) as f:
        json_dict = json.load(f)
    
    if 'ImageType' in json_dict:
        json_dict['ImageType'][5] = 'PHASE'

    with open(phase_json, 'w') as outfile:
        json.dump(json_dict, outfile,indent=4)



