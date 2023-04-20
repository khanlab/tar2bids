#! /usr/bin/env python3
'''
correct field map json
'''
 
import os
import sys
import json
import glob
import collections

def correctFieldMapJson(bids_dir,sub,ses=None):
    
    if ses: #ses not None
        sub_prefix = '{}_{}'.format(sub,ses)
        sub_path_prefix=os.path.join(sub,ses)
        sub_root = '{}'.format(sub)
    else:
        sub_prefix = '{}'.format(sub)
        sub_path_prefix = sub_prefix
        sub_root = '{}'.format(sub)
        
    sub_dir=os.path.join(bids_dir,sub_path_prefix)
    sub_root_dir=os.path.join(bids_dir,sub_root) #without session

    for fmri_json_file in glob(os.path.join(sub_dir,'fmap','{}_acq-EPI_dir-*_epi.json'.format(sub_prefix))):

        #debug
        print(fmri_json_file)

        #load json files
        with open(fmri_json_file, 'r') as f:
            fmri_json = json.load(f,object_pairs_hook=collections.OrderedDict)

        # apply to all bold images
        cwd=os.getcwd()
        os.chdir(sub_root_dir)
        if ses:
            all_bold = glob.glob(os.path.join('{}'.format(ses),'func','{}_*_bold.nii.gz'.format(sub_prefix)))
        else:
            all_bold = glob.glob(os.path.join('func','{}_*_bold.nii.gz'.format(sub_prefix)))

        os.chdir(cwd)
        
        fmri_json["IntendedFor"]=all_bold

        #update json file
        os.system("chmod a+w {}".format(fmri_json_file))
        with open(fmri_json_file, 'w') as f:
            json.dump(fmri_json, f, indent=4, separators=(',', ': '))
        os.system("chmod a-w {}".format(fmri_json_file))


if __name__=="__main__":
    if len(sys.argv)-1 < 2:
        print ("Usage: python " + os.path.basename(__file__)+  " 'bids_dir' 'sub' 'ses (optional)'")
        sys.exit()
    else:
        bids_dir = sys.argv[1]
        sub = sys.argv[2]
        if len(sys.argv)-1 > 2:
            ses=sys.argv[3]
            correctFieldMapJson(bids_dir,sub,ses)
        else:
            correctFieldMapJson(bids_dir,sub)

#test
#Usage: python correctFieldMapJson.py 'bids_dir' 'sub'
#python correctFieldMapJson.py '/mnt/hgfs/test/correct_fieldmap_json/topsy_7T' 'sub-005'
