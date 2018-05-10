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

    # create functional keys
    bold_mag = create_key('{bids_subject_session_dir}/func/{bids_subject_session_prefix}_task-rest_part-mag_run-{item:02d}_bold')
    bold_phase = create_key('{bids_subject_session_dir}/func/{bids_subject_session_prefix}_task-rest_part-phase_run-{item:02d}_bold')
    bold_sbref = create_key('{bids_subject_session_dir}/func/{bids_subject_session_prefix}_task-rest_run-{item:02d}_sbref')

    # add functional keys to the dictionary
    info[bold_mag]=[]
    info[bold_phase]=[]
    info[bold_sbref]=[]

    for idx, s in enumerate(seqinfo):
        #bold
        if ('bold' in s.protocol_name):
            if ( s.dim4 > 2 and ('M' in s.image_type[2].strip()) ):
                info[bold_mag].append({'item': s.series_id})
            if ( s.dim4 > 2 and ('P' in s.image_type[2].strip()) ):
                info[bold_phase].append({'item': s.series_id})
            if ( s.dim4 <= 2 and 'SBRef' in (s.series_description).strip() ):
                info[bold_sbref].append({'item': s.series_id})

    return info
