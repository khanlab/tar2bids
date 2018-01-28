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

    rest = create_key('sub-{subject}/func/sub-{subject}_task-rest_run-{item:02d}_bold')
    rest_sbref = create_key('sub-{subject}/func/sub-{subject}_task-rest_run-{item:02d}_sbref')

    rest_psf = create_key('sub-{subject}/func/sub-{subject}_task-rest_acq-psf_run-{item:02d}_bold')
    rest_psf_dico = create_key('sub-{subject}/func/sub-{subject}_task-rest_acq-psf_rec-dico_run-{item:02d}_bold')

    movie = create_key('sub-{subject}/func/sub-{subject}_task-movie_run-{item:02d}_bold')
    movie_sbref = create_key('sub-{subject}/func/sub-{subject}_task-movie_run-{item:02d}_sbref')

    fmap_PA = create_key('sub-{subject}/fmap/sub-{subject}_dir-PA_epi')
    fmap_PA_sbref = create_key('sub-{subject}/fmap/sub-{subject}_dir-PA_sbref')

    info[rest]=[]
    info[rest_sbref]=[]
    info[rest_psf]=[]
    info[rest_psf_dico]=[]
    info[movie]=[]
    info[movie_sbref]=[]
    info[fmap_PA]=[]
    info[fmap_PA_sbref]=[]

    for idx, s in enumerate(seqinfo):
       
        #rs func (incl opp phase enc)
        if ('Movie' in (s.series_description).strip()):
            if (s.dim4==1 and  'SBRef' in (s.series_description).strip()):
                    info[movie_sbref].append({'item': s.series_id})
            elif (s.dim4>1):
                    info[movie].append({'item': s.series_id})

        
        elif ('bold' in s.protocol_name):
            if ('mbep2d' in (s.series_description).strip() or 'ep_bold' in (s.series_description).strip() ):
                if (s.dim4==1 and  'SBRef' in (s.series_description).strip()):
                    info[rest_sbref].append({'item': s.series_id})
                elif (s.dim4>1):
                    info[rest].append({'item': s.series_id})
 
            if ('mi_ep2d' in (s.series_description).strip() and s.dim4>1):
                if ('DICO'  in (s.image_type[4].strip())):
                    info[rest_psf_dico].append({'item': s.series_id})
                else:
                    info[rest_psf].append({'item': s.series_id})
                    
            if ('PA' in (s.series_description).strip()):
                if (s.dim4==1):
                    if 'SBRef' in (s.series_description).strip():
                        info[fmap_PA_sbref].append({'item': s.series_id})
                    else:
                        info[fmap_PA].append({'item': s.series_id})


    return info
