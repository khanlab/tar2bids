import os

# Adaptation of HCP-Lifespan protocol to the pediatric epilepsy imaging (LOBE) study
# Requires tar2bids > v0.0.5h for vNav clean-up

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

    t1w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-MPRvNav4eRMS_run-{item}_T1w')
    t1w_me = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-MPRvNav4e_run-{item}_T1w')
    t1w_norm = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-MPRvNavNorm4eRMS_run-{item}_T1w')
    t1w_me_norm = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-MPRvNavNorm4e_run-{item}_T1w')
    t1w_vnavs = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-MPRvNav_run-{item}_vNav')

    t2w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-SPCvNavRMS_run-{item}_T2w')
    t2w_norm = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-SPCvNavNormRMS_run-{item}_T2w')
    t2w_vnavs = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-SPCvNav_run-{item}_vNav')


    t1w_basic = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-MPRAGE_run-{item}_T1w')
    t2w_basic = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-SPACE_run-{item}_T2w')

    #Diffusion
    dwi_98_ap = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_acq-98_dir-AP_run-{item}_dwi')
    dwi_98_ap_sbref = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_acq-98_dir-AP_run-{item}_sbref')
    dwi_98_pa = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_acq-98_dir-PA_run-{item}_dwi')
    dwi_98_pa_sbref = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_acq-98_dir-PA_run-{item}_sbref')
    dwi_99_ap = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_acq-99_dir-AP_run-{item}_dwi')
    dwi_99_ap_sbref = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_acq-99_dir-AP_run-{item}_sbref')
    dwi_99_pa = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_acq-99_dir-PA_run-{item}_dwi')
    dwi_99_pa_sbref = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_acq-99_dir-PA_run-{item}_sbref')



    #Field Maps:
    fmap_spinecho_ap = create_key('{bids_subject_session_dir}/fmap/{bids_subject_session_prefix}_acq-spinecho_dir-AP_run-{item}_epi')
    fmap_spinecho_pa = create_key('{bids_subject_session_dir}/fmap/{bids_subject_session_prefix}_acq-spinecho_dir-PA_run-{item}_epi')

    movie_ap = create_key('{bids_subject_session_dir}/func/{bids_subject_session_prefix}_task-movie_acq-AP_run-{item}_bold')
    movie_ap_sbref = create_key('{bids_subject_session_dir}/func/{bids_subject_session_prefix}_task-movie_acq-AP_run-{item}_sbref')

    movie_pa = create_key('{bids_subject_session_dir}/func/{bids_subject_session_prefix}_task-movie_acq-PA_run-{item}_bold')
    movie_pa_sbref = create_key('{bids_subject_session_dir}/func/{bids_subject_session_prefix}_task-movie_acq-PA_run-{item}_sbref')

    rest_ap = create_key('{bids_subject_session_dir}/func/{bids_subject_session_prefix}_task-rest_acq-AP_run-{item}_bold')
    rest_ap_sbref = create_key('{bids_subject_session_dir}/func/{bids_subject_session_prefix}_task-rest_acq-AP_run-{item}_sbref')
    rest_pa = create_key('{bids_subject_session_dir}/func/{bids_subject_session_prefix}_task-rest_acq-PA_run-{item}_bold')
    rest_pa_sbref = create_key('{bids_subject_session_dir}/func/{bids_subject_session_prefix}_task-rest_acq-PA_run-{item}_sbref')



    info = {t1w_me:[],t1w_me_norm:[],t1w_vnavs:[],t1w:[],t1w_norm:[],
         t2w_vnavs:[],t2w:[],t2w_norm:[],
         t1w_basic:[],t2w_basic:[],
         rest_ap:[],rest_ap_sbref:[],
         rest_pa:[],rest_pa_sbref:[],
         movie_ap:[],movie_ap_sbref:[],
         movie_pa:[],movie_pa_sbref:[],
         dwi_98_ap:[],dwi_98_pa:[],dwi_98_ap_sbref:[],dwi_98_pa_sbref:[],
         dwi_99_ap:[],dwi_99_pa:[],dwi_99_ap_sbref:[],dwi_99_pa_sbref:[],
         fmap_spinecho_ap:[],fmap_spinecho_pa:[]}

    for idx, s in enumerate(seqinfo):


        # T1w images
        if 'T1w_MPR_vNav_setter' in s.series_description:
            if 'MOSAIC' in s.image_type:
                info[t1w_vnavs].append({'item': s.series_id})

        elif ('tfl_mgh_epinav_ABCD' in s.series_description):
            if 'OTHER' in s.image_type: 
                if 'NORM' in s.image_type:
                    info[t1w_norm].append({'item': s.series_id})
                else:
                    info[t1w].append({'item': s.series_id})
            if 'M' in s.image_type: 
                if 'NORM' in s.image_type:
                    info[t1w_me_norm].append({'item': s.series_id})
                else:
                    info[t1w_me].append({'item': s.series_id})
                
        elif ('T1w_MPR' in s.series_description):
            info[t1w_basic].append({'item': s.series_id})


        #T2w images
        if 'T2w_SPC_vNav_setter' in s.series_description:
            if 'MOSAIC' in s.image_type:
                info[t2w_vnavs].append({'item': s.series_id})
        elif ('T2w_SPC_800iso_vNav' in s.series_description):
            if 'NORM' in s.image_type:
                info[t2w_norm].append({'item': s.series_id}) 
            else:
                info[t2w].append({'item': s.series_id}) 
        elif ('T2w_SPC' in s.series_description):
            info[t2w_basic].append({'item': s.series_id})
    
        #spinecho field maps

        if ('SpinEchoFieldMap_AP' in s.series_description):   
            info[fmap_spinecho_ap].append({'item': s.series_id})

        if ('SpinEchoFieldMap_PA' in s.series_description):   
            info[fmap_spinecho_pa].append({'item': s.series_id})


        #dwi
        if 'dMRI_dir98_AP' in s.series_description:
            if 'DIFFUSION' in s.image_type:
                info[dwi_98_ap].append({'item': s.series_id})
            elif 'SBRef' in s.series_description:
                info[dwi_98_ap_sbref].append({'item': s.series_id})
        if 'dMRI_dir98_PA' in s.series_description:
            if 'DIFFUSION' in s.image_type:
                info[dwi_98_pa].append({'item': s.series_id})
            elif 'SBRef' in s.series_description:
                info[dwi_98_pa_sbref].append({'item': s.series_id})
        if 'dMRI_dir99_AP' in s.series_description:
            if 'DIFFUSION' in s.image_type:
                info[dwi_99_ap].append({'item': s.series_id})
            elif 'SBRef' in s.series_description:
                info[dwi_99_ap_sbref].append({'item': s.series_id})
        if 'dMRI_dir99_PA' in s.series_description:
            if 'DIFFUSION' in s.image_type:
                info[dwi_99_pa].append({'item': s.series_id})
            elif 'SBRef' in s.series_description:
                info[dwi_99_pa_sbref].append({'item': s.series_id})
                                 

        #rs func (incl opp phase enc)
        if 'rfMRI_REST_AP' in s.series_description:
            if (s.dim4==1 and 'SBRef' in s.series_description):
                info[rest_ap_sbref].append({'item': s.series_id})
            else:
                info[rest_ap].append({'item': s.series_id})
        if 'rfMRI_REST_PA' in s.series_description:
            if (s.dim4==1 and 'SBRef' in s.series_description):
                info[rest_pa_sbref].append({'item': s.series_id})
            else:
                info[rest_pa].append({'item': s.series_id})
 
        if 'movie_AP' in s.series_description:
            if (s.dim4==1 and 'SBRef' in s.series_description):
                info[movie_ap_sbref].append({'item': s.series_id})
            else:
                info[movie_ap].append({'item': s.series_id})
                
        if 'movie_PA' in s.series_description:
            if (s.dim4==1 and 'SBRef' in s.series_description):
                info[movie_pa_sbref].append({'item': s.series_id})
            else:
                info[movie_pa].append({'item': s.series_id})
  
             
    return info
