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

    #Compatible with:

    # FLASH T1 
    # FLASH MT ON
    # FLASH MT OFF

    FLASH_T1 = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-T1_run-{item:02d}_FLASH')
    FLASH_MT_ON = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-MTon_run-{item:02d}_FLASH')
    FLASH_MT_OFF = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-MToff_run-{item:02d}_FLASH')
    dwi = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_acq-T1_run-{item:02d}_dwi')

    MP2RAGE_T1map = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-MP2RAGE_run-{item:02d}_T1map')
    MP2RAGE_invs = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-Inversions_run-{item:02d}_MP2RAGE')
    MP2RAGE_UNI = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-UNI_run-{item:02d}_T1w')

    MP2RAGE_T1map_l = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-LoResMP2RAGE_run-{item:02d}_T1map')
    MP2RAGE_invs_l = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-LoResInversions_run-{item:02d}_MP2RAGE')
    MP2RAGE_UNI_l = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-LoResUNI_run-{item:02d}_T1w')


    MEGRE_mag = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_part-mag_echo_run-{item:02d}_GRE')
    MEGRE_complex = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_part-complex_echo_run-{item:02d}_GRE')


    info = { FLASH_T1:[],FLASH_MT_ON:[],FLASH_MT_OFF:[],dwi:[],MP2RAGE_T1map:[],MP2RAGE_invs:[],MP2RAGE_UNI:[],MP2RAGE_T1map_l:[],MP2RAGE_invs_l:[],MP2RAGE_UNI_l:[],MEGRE_mag:[],MEGRE_complex:[]}

    for idx, s in enumerate(seqinfo):

    
        #FLASH
        if ('T1_FLASH' in s.protocol_name):
            info[FLASH_T1].append({'item': s.series_id})
        elif ('FLASH3D_MT' in s.protocol_name):
            if ('OFF' in s.series_description.strip()):
                info[FLASH_MT_OFF].append({'item': s.series_id})
            else:
                info[FLASH_MT_ON].append({'item': s.series_id})
                
        elif ('DTI' in s.protocol_name):
            info[dwi].append({'item': s.series_id})
        
        elif ('MP2RAGE' in s.series_description.strip()):
          if (s.dim1 > 64):
            if  ('0001' in s.dcm_dir_name.strip()):
                info[MP2RAGE_T1map].append({'item': s.series_id})
            elif  ('0002' in s.dcm_dir_name.strip()):
                info[MP2RAGE_invs].append({'item': s.series_id})
            else:
                info[MP2RAGE_UNI].append({'item': s.series_id})
          else:
            if  ('0001' in s.dcm_dir_name.strip()):
                info[MP2RAGE_T1map_l].append({'item': s.series_id})
            elif  ('0002' in s.dcm_dir_name.strip()):
                info[MP2RAGE_invs_l].append({'item': s.series_id})
            else:
                info[MP2RAGE_UNI_l].append({'item': s.series_id})

        elif ('T2star' in s.series_description.strip()):
            if (s.dim3 == 2 and s.dim4 < 12): #to cover the case when dim3=2 could refer to 2 echos, instead of real/imag..
                info[MEGRE_complex].append({'item': s.series_id})
            else:
                info[MEGRE_mag].append({'item': s.series_id})

   
    return info
