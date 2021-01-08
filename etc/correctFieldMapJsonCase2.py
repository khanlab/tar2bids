#! /usr/bin/env python
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

    phase1_json_file=os.path.join(sub_dir,'fmap','{}_phase1.json'.format(sub_prefix))
    phase2_json_file=os.path.join(sub_dir,'fmap','{}_phase2.json'.format(sub_prefix))
    mag1_json_file=os.path.join(sub_dir,'fmap','{}_magnitude1.json'.format(sub_prefix))
    mag2_json_file=os.path.join(sub_dir,'fmap','{}_magnitude2.json'.format(sub_prefix))

    #debug
    # print phase1_json_file
    # print mag1_json_file
    # print mag2_json_file

    #load json files
    with open(phase1_json_file, 'r') as f:
        phase1_json = json.load(f,object_pairs_hook=collections.OrderedDict)

    with open(phase2_json_file, 'r') as f:
        phase2_json = json.load(f,object_pairs_hook=collections.OrderedDict)
  
    with open(mag1_json_file, 'r') as f:
        mag1_json = json.load(f)

    with open(mag2_json_file, 'r') as f:
        mag2_json = json.load(f)


    # apply to all bold images
    cwd=os.getcwd()
    os.chdir(sub_root_dir)
    if ses:
        all_bold = glob.glob(os.path.join('{}'.format(ses),'func','{}_*_bold.nii.gz'.format(sub_prefix)))
    else:
        all_bold = glob.glob(os.path.join('func','{}_*_bold.nii.gz'.format(sub_prefix)))

    os.chdir(cwd)
    
    phase1_json["IntendedFor"]=all_bold

    #update json file
    os.system("chmod a+w {}".format(phase1_json_file))
    with open(phase1_json_file, 'w') as f:
         json.dump(phase1_json, f, indent=4, separators=(',', ': '))
    os.system("chmod a-w {}".format(phase1_json_file))

    phase2_json["IntendedFor"]=all_bold

    #update json file
    os.system("chmod a+w {}".format(phase2_json_file))
    with open(phase2_json_file, 'w') as f:
         json.dump(phase2_json, f, indent=4, separators=(',', ': '))
    os.system("chmod a-w {}".format(phase2_json_file))


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
