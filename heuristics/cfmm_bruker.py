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


    info = { FLASH_T1:[],FLASH_MT_ON:[],FLASH_MT_OFF:[]}

    for idx, s in enumerate(seqinfo):

    
        #FLASH
        if ('T1_FLASH' in s.protocol_name):
            info[FLASH_T1].append({'item': s.series_id})
        elif ('FLASH3D_MT' in s.protocol_name):
            if ('OFF' in s.series_description.strip()):
                info[FLASH_MT_OFF].append({'item': s.series_id})
            else:
                info[FLASH_MT_ON].append({'item': s.series_id})
                

            

   
    return info
