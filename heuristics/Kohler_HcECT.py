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



    task_intact = create_key('{bids_subject_session_dir}/func/{bids_subject_session_prefix}_task-intact_run-{item:02d}_bold')
    task_scrambled = create_key('{bids_subject_session_dir}/func/{bids_subject_session_prefix}_task-scrambled_run-{item:02d}_bold')
    task_soundcheck = create_key('sourcedata/soundcheck_bold/{bids_subject_session_dir}/func/{bids_subject_session_prefix}_task-soundcheck_run-{item:02d}_bold')


    discarded = create_key('sourcedata/discarded_bold/{bids_subject_session_dir}/func/{bids_subject_session_prefix}_task-{task}_run-{item:02d}_bold')



    info[task_intact]=[]
    info[task_scrambled]=[]
    info[task_soundcheck]=[]
    info[discarded]=[]

    for idx, s in enumerate(seqinfo):
       
        if ('bold' in s.protocol_name or 'tasking_state' in s.series_description or 'mbep2d' in (s.series_description).strip() or 'ep_bold' in (s.series_description).strip() and not ('diff' in s.protocol_name or 'DWI' in s.series_description )):
            
            if ('SBRef' in (s.series_description).strip()):
                print('skipping sbref')


            else:

                #check what task it is
                if ('soundcheck' in (s.series_description).strip().lower()):
                    taskname='soundcheck'
                    taskvols=40

                    if (s.dim4 < taskvols):
                        info[discarded].append({'item': s.series_id,'task': taskname})
                    elif (s.dim4 == taskvols): 
                        info[task_soundcheck].append({'item': s.series_id,'task': taskname})


                elif ('intact' in (s.series_description).strip().lower()):
                    taskname='intact'
                    taskvols=320

                    if (s.dim4 < taskvols):
                        info[discarded].append({'item': s.series_id,'task': taskname})
                    elif (s.dim4 == taskvols): 
                        info[task_intact].append({'item': s.series_id,'task': taskname})


                elif ('scrambled' in (s.series_description).strip().lower()):
                    taskname='scrambled'
                    taskvols=320


                    if (s.dim4 < taskvols):
                        info[discarded].append({'item': s.series_id,'task': taskname})
                    elif (s.dim4 == taskvols): 
                        info[task_scrambled].append({'item': s.series_id,'task': taskname})

                else:
                    continue

 
                  
    return info
