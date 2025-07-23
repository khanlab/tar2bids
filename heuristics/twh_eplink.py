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

    t1w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_run-{item:02d}_T1w')
    flair = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_run-{item:02d}_FLAIR')


    #Diffusion
    dwi = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_run-{item:02d}_dwi')



    rest = create_key('{bids_subject_session_dir}/func/{bids_subject_session_prefix}_task-rest_run-{item:02d}_bold')
    movie = create_key('{bids_subject_session_dir}/func/{bids_subject_session_prefix}_task-movie_run-{item:02d}_bold')



    info = { t1w:[], 
            flair:[],
            dwi:[],
            movie:[],
            rest:[]}

    for idx, s in enumerate(seqinfo):

        #t1
        if ('SPGR' in s.series_description or 'T1w' in s.series_description):
            info[t1w].append({'item': s.series_id})

        #flair
        if ('flair' in s.series_description.lower() or 'dark-fluid' in s.series_description.lower()):
            info[flair].append({'item': s.series_id})

        #rsfmri
        elif ('rest' in s.series_description.lower()):
            info[rest].append({'item': s.series_id})
        #rsfmri
        elif ('movie' in s.series_description.lower()):
            info[rest].append({'item': s.series_id})


        #dwi
        if ('DTI' in s.series_description):

            if len(s.image_type) > 2 :
                if (('DIFFUSION' in s.image_type[2].strip()) and ('ORIGINAL' in s.image_type[0].strip())):
                    info[dwi].append({'item': s.series_id})
                elif (len(s.image_type) == 3) and ('PRIMARY' in s.image_type[1].strip()) and ('OTHER' in s.image_type[2].strip()) and ('ORIGINAL' in s.image_type[0].strip()):
                    info[dwi].append({'item': s.series_id})
            else:
                info[dwi].append({'item': s.series_id})
                

    
              
    return info
