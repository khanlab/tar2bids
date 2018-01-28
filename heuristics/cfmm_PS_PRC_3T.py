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


    loc = create_key('sub-{subject}/func/sub-{subject}_task-loc_run-{item:02d}_bold')
    loc_sbref = create_key('sub-{subject}/func/sub-{subject}_task-loc_run-{item:02d}_sbref')

    loc_PA = create_key('sub-{subject}/func/sub-{subject}_task-loc_acq-PA_run-{item:02d}_bold')
    loc_PA_sbref = create_key('sub-{subject}/func/sub-{subject}_task-loc_acq-PA_run-{item:02d}_sbref')

    loc_AP = create_key('sub-{subject}/func/sub-{subject}_task-loc_acq-AP_run-{item:02d}_bold')
    loc_AP_sbref = create_key('sub-{subject}/func/sub-{subject}_task-loc_acq-AP_run-{item:02d}_sbref')

    nback = create_key('sub-{subject}/func/sub-{subject}_task-nback_run-{item:02d}_bold')
    nback_sbref = create_key('sub-{subject}/func/sub-{subject}_task-nback_run-{item:02d}_sbref')

    nback_PA = create_key('sub-{subject}/func/sub-{subject}_task-nback_acq-PA_run-{item:02d}_bold')
    nback_PA_sbref = create_key('sub-{subject}/func/sub-{subject}_task-nback_acq-PA_run-{item:02d}_sbref')

    nback_AP = create_key('sub-{subject}/func/sub-{subject}_task-nback_acq-AP_run-{item:02d}_bold')
    nback_AP_sbref = create_key('sub-{subject}/func/sub-{subject}_task-nback_acq-AP_run-{item:02d}_sbref')



    info[loc]=[]
    info[loc_sbref]=[]
    info[loc_PA]=[]
    info[loc_PA_sbref]=[]
    info[loc_AP]=[]
    info[loc_AP_sbref]=[]


    info[nback]=[]
    info[nback_sbref]=[]
    info[nback_PA]=[]
    info[nback_PA_sbref]=[]
    info[nback_AP]=[]
    info[nback_AP_sbref]=[]

    for idx, s in enumerate(seqinfo):
 
        #func localizer and nback tasks (incl opp phase enc)
        if ('loc' in (s.protocol_name).strip()):
            if ('_PA' in (s.series_description).strip()):
                if (s.dim4==1 and  'SBRef' in (s.series_description).strip()):
                    info[loc_PA_sbref].append({'item': s.series_id})
                elif (s.dim4>1):
                    info[loc_PA].append({'item': s.series_id})
            elif ('_AP' in (s.series_description).strip()):
                if (s.dim4==1 and  'SBRef' in (s.series_description).strip()):
                    info[loc_AP_sbref].append({'item': s.series_id})
                elif (s.dim4>1):
                    info[loc_AP].append({'item': s.series_id})
            else:
                if (s.dim4==1 and  'SBRef' in (s.series_description).strip()):
                    info[loc_sbref].append({'item': s.series_id})
                elif (s.dim4>1):
                    info[loc].append({'item': s.series_id})


        elif ('ep_bold' in s.protocol_name):
            if ('_PA' in (s.series_description).strip()):
                if (s.dim4==1 and  'SBRef' in (s.series_description).strip()):
                    info[nback_PA_sbref].append({'item': s.series_id})
                elif (s.dim4>1):
                    info[nback_PA].append({'item': s.series_id})
            elif ('_AP' in (s.series_description).strip()):
                if (s.dim4==1 and  'SBRef' in (s.series_description).strip()):
                    info[nback_AP_sbref].append({'item': s.series_id})
                elif (s.dim4>1):
                    info[nback_AP].append({'item': s.series_id})
            else:
                if (s.dim4==1 and  'SBRef' in (s.series_description).strip()):
                    info[nback_sbref].append({'item': s.series_id})
                elif (s.dim4>1):
                    info[nback].append({'item': s.series_id})


     
    return info
