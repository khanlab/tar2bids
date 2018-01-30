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
    t1 = create_key('sub-{subject}/anat/sub-{subject}_run-{item:02d}_T1w')

    fa18 = create_key('sub-{subject}/anat/sub-{subject}_acq-SPGR_flip-1_run-{item:02d}_DESPOT')
    fa4 = create_key('sub-{subject}/anat/sub-{subject}_acq-SPGR_flip-2_run-{item:02d}_DESPOT')
    irspgr = create_key('sub-{subject}/anat/sub-{subject}_acq-IRSPGR_run-{item:02d}_DESPOT')

    fa68p180 = create_key('sub-{subject}/anat/sub-{subject}_acq-SSFP_flip-1_phase-180_run-{item:02d}_DESPOT')
    fa68p0 = create_key('sub-{subject}/anat/sub-{subject}_acq-SSFP_flip-1_phase-0_run-{item:02d}_DESPOT')
    fa35p180 = create_key('sub-{subject}/anat/sub-{subject}_acq-SSFP_flip-2_phase-180_run-{item:02d}_DESPOT')
    fa15p180 = create_key('sub-{subject}/anat/sub-{subject}_acq-SSFP_flip-3_phase-180_run-{item:02d}_DESPOT')
    fa15p0 = create_key('sub-{subject}/anat/sub-{subject}_acq-SSFP_flip-3_phase-0_run-{item:02d}_DESPOT')

    rest = create_key('sub-{subject}/func/sub-{subject}_task-rest_run-{item:02d}_bold')

    dwi = create_key('sub-{subject}/dwi/sub-{subject}_run-{item:02d}_dwi')

    info = {t1:[],fa18:[],fa4:[],irspgr:[],fa68p180:[],fa68p0:[],fa35p180:[],fa15p180:[],rest:[],dwi:[]}

    for idx, s in enumerate(seqinfo):
    
	#T1w
        if  ('Accelerated Sag IR-FSPGR' in s.series_description):
                info[t1].append({'item': s.series_id})
	
        if  ('despot1_tr90_fa18' in s.series_description):
                info[fa18].append({'item': s.series_id})

	#despot1
	if  ('despot1_tr90_fa18' in s.series_description):
                info[fa18].append({'item': s.series_id})
	if  ('despot1_tr90_fa4' in s.series_description):
                info[fa4].append({'item': s.series_id})
	if  ('irspgr_tr88_fa5_ti450_pe82' in s.series_description):
                info[irspgr].append({'item': s.series_id})

	#despot2
	if  ('ssfp_tr61_fa68_phase180' in s.series_description):
                info[fa68p180].append({'item': s.series_id})
	if  ('ssfp_tr61_fa68_phase0' in s.series_description):
                info[fa68p0].append({'item': s.series_id})
	if  ('ssfp_tr61_fa35_phase180' in s.series_description):
                info[fa35p180].append({'item': s.series_id})
	if  ('ssfp_tr61_fa15_phase180' in s.series_description):
                info[fa15p180].append({'item': s.series_id})
	if  ('ssfp_tr61_fa15_phase180' in s.series_description):
                info[fa15p180].append({'item': s.series_id})

	   
        #rs func
        if ('RESTING STATE' in s.series_description):
            info[rest].append({'item': s.series_id})


        #dwi
        if ('Axial DTI' in s.series_description):
                info[dwi].append({'item': s.series_id})
          

   
    return info
