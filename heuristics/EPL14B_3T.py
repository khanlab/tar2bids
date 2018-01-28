import os

def create_key(template, outtype=('nii.gz'), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return (template, outtype, annotation_classes)

def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """
    t1 = create_key('sub-{subject}/anat/sub-{subject}_T1w')

    t1map = create_key('sub-{subject}/anat/sub-{subject}_acq-MP2RAGE_T1map')
    t1inv1 = create_key('sub-{subject}/anat/sub-{subject}_inv-1_MP2RAGE')
    t1inv2 = create_key('sub-{subject}/anat/sub-{subject}_inv-2_MP2RAGE')
    t1uni = create_key('sub-{subject}/anat/sub-{subject}_acq-UNI_MP2RAGE')

    t2 = create_key('sub-{subject}/anat/sub-{subject}_FLAIR')
    rest = create_key('sub-{subject}/func/sub-{subject}_task-rest_bold')
    movie = create_key('sub-{subject}/func/sub-{subject}_task-hitchcock_bold')
    dwi_RL = create_key('sub-{subject}/dwi/sub-{subject}_acq-multibandRL_dwi')
    dwi_LR = create_key('sub-{subject}/dwi/sub-{subject}_acq-multibandLR_dwi')
    dwi_singleband = create_key('sub-{subject}/dwi/sub-{subject}_acq-singleband_dwi')

    info = {t1:[],t1map:[],t1inv1:[],t1inv2:[],t1uni:[],
		t2:[],rest:[],movie:[],
		dwi_RL:[],dwi_LR:[],dwi_singleband:[]}

    for idx, s in enumerate(seqinfo):
    
        #mp2rage
        if  ('MP2RAGE' in s.protocol_name):
            if ('UNI' in (s.series_description).strip()):
                info[t1uni].append({'item': s.series_id})
	    if ('T1_Images' in (s.series_description).strip()):
                info[t1map].append({'item': s.series_id})
	    if ('INV1' in (s.series_description).strip()):
                info[t1inv1].append({'item': s.series_id})
	    if ('INV2' in (s.series_description).strip()):
                info[t1inv2].append({'item': s.series_id})

	#T1w
        if  ('T1' in s.protocol_name):
                info[t1].append({'item': s.series_id})
	
	#t2 FLAIR
        if  ('FLAIR' in s.protocol_name):
                info[t2].append({'item': s.series_id})
	    
        #rs func (incl opp phase enc)
        if ('RS_fMRI' in s.protocol_name):
            info[rest].append({'item': s.series_id})

        if ('Movie' in s.protocol_name):
	    if ('Movie' == s.series_description):
                 info[movie].append({'item': s.series_id})


        #dwi
        if ('diff' in s.protocol_name):
            if ( s.dim4 > 1 and ('diff_mb3_140_b2600_RL' == (s.series_description).strip()) ) :
                info[dwi_RL].append({'item': s.series_id})
            if ( s.dim4 > 1 and ('diff_mb3_140_b2600_LR' == (s.series_description).strip()) ) :
		info[dwi_LR].append({'item': s.series_id})

        if ('DTI' in s.protocol_name):
            if ( s.dim4 > 1 and ('DTI_30' == (s.series_description).strip()) ) :
                info[dwi_singleband].append({'item': s.series_id})
           

   
    return info
