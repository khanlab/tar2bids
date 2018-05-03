import os
import numpy
from cfmm_base import infotodict as cfmminfodict
from cfmm_base import create_key

def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """

    # call cfmm for general labelling and get dictionary
    info = cfmminfodict(seqinfo)

    ContRecog = create_key('sub-{subject}/func/sub-{subject}_task-nback_run-{item:02d}_bold')
    ContRecog_sbref = create_key('sub-{subject}/func/sub-{subject}_task-nback_run-{item:02d}_sbref')


    info[ContRecog]=[]
    info[ContRecog_sbref]=[]


    for idx, s in enumerate(seqinfo):
 
        #func continuous recognition memory task
    	if ('cmrr_ep' in s.protocol_name and 'test' not in s.protocol_name):
	    if (s.dim4==1 and  'SBRef' in (s.series_description).strip()):
            	info[ContRecog_sbref].append({'item': s.series_id})
	    elif (s.dim4>1):
            	info[ContRecog].append({'item': s.series_id})


    return info
