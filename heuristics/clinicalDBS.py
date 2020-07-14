# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 16:14:57 2018

@author: Greydon
"""

def create_key(template, outtype=('nii.gz'), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return (template, outtype, annotation_classes)

def get_unique(seqinfos, attr):
    """Given a list of seqinfos, which must have come from a single study
    get specific attr, which must be unique across all of the entries
    If not -- fail!
    """
    values = set(getattr(si, attr) for si in seqinfos)
#    assert (len(values) == 1)
    return values.pop()

def infotoids(seqinfos, outdir):
    
    subject = get_unique(seqinfos, 'example_dcm_file').split('_')[0]
    session = get_unique(seqinfos, 'example_dcm_file').split('_')[1]
    
    ids = {
    'locator': '',
    'session': session,
    'subject': subject,
    }
                
    return ids

def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """
    
    #2D TSE 
    # Transverse
    fse_tra_T2w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-FSEtra_run-{item:02d}_T2w')
    pd_tra_T1w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-PDtra_run-{item:02d}_T2w')
    flair_tra_T1w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-tra_run-{item:02d}_FLAIR')
    ssfse_tra_T1w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-SSFSEtra_run-{item:02d}_T1w')
    fse_tra_T2w_electrode = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-FSEtraELECTRODE_run-{item:02d}_T2w')
    pd_tra_T1w_electrode = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-PDtraELECTRODE_run-{item:02d}_T2w')
    flair_tra_T1w_electrode= create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-traELECTRODE_run-{item:02d}_FLAIR')
	
    #Coronal
    fse_cor_T2w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-FSEcor_run-{item:02d}_T2w')
    pd_cor_T1w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-PDcor_run-{item:02d}_T2w')
    flair_cor_T1w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-cor_run-{item:02d}_FLAIR')
    ssfse_cor_T1w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-SSFSEcor_run-{item:02d}_T1w')
    fse_cor_T2w_electrode = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-FSEcorELECTRODE_run-{item:02d}_T2w')
    pd_cor_T1w_electrode = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-PDcorELECTRODE_run-{item:02d}_T2w')
    flair_cor_T1w_electrode = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-corELECTRODE_run-{item:02d}_FLAIR')
    
    #Saggital
    fse_sag_T2w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-FSEsag_run-{item:02d}_T2w')
    pd_sag_T1w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-PDsag_run-{item:02d}_T2w')
    flair_sag_T1w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-sag_run-{item:02d}_FLAIR')
    ssfse_sag_T1w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-SSFSEsag_run-{item:02d}_T1w')
    
    #3D Stealth
    t1 = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-3D_run-{item:02d}_T1w')
    t1_electrode = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-3DELECTRODE_run-{item:02d}_T1w')
    t2_electrode = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-3DELECTRODE_run-{item:02d}_T2w')
    
    #T2 EPI
    epi_t2 = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-EPI_run-{item:02d}_T2w')
    epi_t2_electrode = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-EPIELECTRODE_run-{item:02d}_T2w')
    
    #Localizer
    loc_tra = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-tra_run-{item:02d}_loc')
    loc_cor = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-cor_run-{item:02d}_loc')
    loc_sag = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-sag_run-{item:02d}_loc')
    loc_3D = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-3D_run-{item:02d}_loc')
    loc_tra_electrode = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-traelectrode_run-{item:02d}_loc')
    loc_cor_electrode = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-corelectrode_run-{item:02d}_loc')
    loc_sag_electrode = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-sagelectrode_run-{item:02d}_loc')
    loc_3D_electrode = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-3Delectrode_run-{item:02d}_loc')
    
    #MPGR
    mpgr_electrode = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-MPGRELECTRODE_run-{item:02d}_T1w')
    mpgr_2D = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_mod-2D_acq-MPGR_run-{item:02d}_T1w')
    mpgr_3D = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_mod-3D_acq-MPGR_run-{item:02d}_T1w')
    
    #FSPGR
    fspgr = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-FSPGR_run-{item:02d}_T1w')
    fspgr_electrode = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-FSPGRELECTRODE_run-{item:02d}_T1w')
    
    #Diffusion
    trace = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_mod-TRACE_run-{item:02d}_T2w')
    trace_electrode = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_mod-TRACE_acq-ELECTRODE_run-{item:02d}_T2w')
    
    #Diffusion
    dwi = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_run-{item:02d}_dwi')
    dwi_electrode = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_acq-ELECTRODE_run-{item:02d}_dwi')
    
    avg_dc = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_mod-AVGDC_run-{item:02d}_T1w')
    avg_dc_electrode = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_mod-AVGDC_acq-ELECTRODE_run-{item:02d}_T1w')
    
    fa = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_run-{item:02d}_angio')
    fa_electrode = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_acq-ELECTRODE_run-{item:02d}_angio')
    
    #CT
    ct = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_run-{item:02d}_ct')
    ct_scout = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-ELECTRODE_run-{item:02d}_ctScout')
    ct_frame = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_run-{item:02d}_ctFrame')
    ct_frame_scout = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_run-{item:02d}_ctFrameScout')
    ct_electrode = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-ELECTRODE_run-{item:02d}_ct')
    ct_scout_electrode = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-ELECTRODE_run-{item:02d}_ctScout')

    #Fluoro Intra
    xr = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_xr')
    
    info = {fse_tra_T2w:[],
            pd_tra_T1w:[],
            flair_tra_T1w:[],
            fse_tra_T2w_electrode:[],
            pd_tra_T1w_electrode:[],
            flair_tra_T1w_electrode:[],
            fse_cor_T2w:[],
            pd_cor_T1w:[],
            flair_cor_T1w:[],
            fse_cor_T2w_electrode:[],
            pd_cor_T1w_electrode:[],
            flair_cor_T1w_electrode:[],
            fse_sag_T2w:[],
            pd_sag_T1w:[],
            flair_sag_T1w:[],
            t1:[], 
            t1_electrode:[],
            t2_electrode:[],
            epi_t2:[],
            epi_t2_electrode:[],
            loc_tra:[],
            loc_cor:[],
            loc_sag:[],
            loc_3D:[],
            loc_tra_electrode:[],
            loc_cor_electrode:[],
            loc_sag_electrode:[],
            loc_3D_electrode:[],
            mpgr_electrode:[],
            mpgr_2D:[],
            mpgr_3D:[],
            fspgr:[],
            fspgr_electrode:[],
            ssfse_tra_T1w:[],
            ssfse_cor_T1w:[],
            ssfse_sag_T1w:[],
            trace:[],
            trace_electrode:[],
            dwi:[], 
            dwi_electrode:[],
            avg_dc:[],
            avg_dc_electrode:[],
            fa:[],
            fa_electrode:[],
            ct:[],
            ct_scout:[],
            ct_frame:[],
            ct_frame_scout:[],
            ct_electrode:[],
            ct_scout_electrode:[],
            xr:[]}
    
    for idx, s in enumerate(seqinfo):
        if any(substring in s.study_description.upper() for substring in {'MR'}):
            
            if any(substring in s.series_description.upper() for substring in {'STEALTH','3D','STEREO'}):
                if 'SAR' in s.series_description.upper() or 'SAFE' in s.protocol_name:
                    if 'T2' in s.series_description.upper():
                        info[t2_electrode].append({'item': s.series_id})
                    else:
                        info[t1_electrode].append({'item': s.series_id})
                else:
                    info[t1].append({'item': s.series_id})
                    
            if 'EPI' in s.series_description.upper():
                if 'SAR' in s.series_description.upper() or 'SAFE' in s.protocol_name:
                    info[epi_t2_electrode].append({'item': s.series_id})
                elif 'T2' in s.series_description.upper():
                    info[epi_t2].append({'item': s.series_id})
                    
            if 'MPGR' in s.series_description.upper():
                if 'SAR' in s.series_description.upper() or 'SAFE' in s.protocol_name:
                    info[mpgr_electrode].append({'item': s.series_id})
                elif 'AX' in s.series_description.upper():
                    info[mpgr_2D].append({'item': s.series_id})
                else:
                    info[mpgr_3D].append({'item': s.series_id})
                    
            if any(substring in s.series_description.upper() for substring in {'IR_FSPGR','FSPGR'}):
                if not any(substring in s.series_description.upper() for substring in {'STEALTH','3D','STEREO'}):
                    if 'SAR' in s.series_description.upper() or 'SAFE' in s.protocol_name.upper():
                        info[fspgr_electrode].append({'item': s.series_id})
                    else:
                        info[fspgr].append({'item': s.series_id})
                    
            if 'AX' in s.series_description.upper() and '3D' not in s.series_description.upper():
                if 'SAR' in s.series_description.upper() or 'SAFE' in s.protocol_name.upper():
                    if any(substring in s.series_description.upper() for substring in {'T2','2D'}):
                        info[fse_tra_T2w_electrode].append({'item': s.series_id})
                    elif any(substring in s.series_description.upper() for substring in {'PD'}):
                        info[pd_tra_T1w_electrode].append({'item': s.series_id})
                    elif any(substring in s.series_description.upper() for substring in {'FLAIR'}):
                        info[flair_tra_T1w_electrode].append({'item': s.series_id})
                else:
                    if any(substring in s.series_description.upper() for substring in {'T2','2D'}):
                        info[fse_tra_T2w].append({'item': s.series_id})
                    elif any(substring in s.series_description.upper() for substring in {'PD'}):
                        info[pd_tra_T1w].append({'item': s.series_id})
                    elif any(substring in s.series_description.upper() for substring in {'FLAIR'}):
                        info[flair_tra_T1w].append({'item': s.series_id})
                    elif any(substring in s.series_description.upper() for substring in {'SSFSE'}):
                        info[ssfse_tra_T1w].append({'item': s.series_id})
                    
            if 'COR' in s.series_description.upper() and '3D' not in s.series_description.upper():
                if 'SAR' in s.series_description.upper() or 'SAFE' in s.protocol_name.upper():
                    if any(substring in s.series_description.upper() for substring in {'T2','2D'}):
                        info[fse_cor_T2w_electrode].append({'item': s.series_id})
                    elif any(substring in s.series_description.upper() for substring in {'PD'}):
                        info[pd_cor_T1w_electrode].append({'item': s.series_id})
                    elif any(substring in s.series_description.upper() for substring in {'FLAIR'}):
                        info[flair_cor_T1w_electrode].append({'item': s.series_id})
                else:
                    if any(substring in s.series_description.upper() for substring in {'T2','2D'}):
                        info[fse_cor_T2w].append({'item': s.series_id})
                    elif any(substring in s.series_description.upper() for substring in {'PD'}):
                        info[pd_cor_T1w].append({'item': s.series_id})
                    elif any(substring in s.series_description.upper() for substring in {'FLAIR'}):
                        info[flair_cor_T1w].append({'item': s.series_id})
                    elif any(substring in s.series_description.upper() for substring in {'SSFSE'}):
                        info[ssfse_cor_T1w].append({'item': s.series_id})
            
            if 'SAG' in s.series_description.upper() and '3D' not in s.series_description.upper():
                if 'SAR' in s.series_description.upper() or 'SAFE' in s.protocol_name.upper():
                    if any(substring in s.series_description.upper() for substring in {'T2','2D'}):
                        info[fse_sag_T2w].append({'item': s.series_id})
                    elif any(substring in s.series_description.upper() for substring in {'PD'}):
                        info[pd_sag_T1w].append({'item': s.series_id})
                    elif any(substring in s.series_description.upper() for substring in {'FLAIR'}):
                        info[flair_sag_T1w].append({'item': s.series_id})
                else:
                    if any(substring in s.series_description.upper() for substring in {'T2','2D'}):
                        info[fse_sag_T2w].append({'item': s.series_id})
                    elif any(substring in s.series_description.upper() for substring in {'PD'}):
                        info[pd_sag_T1w].append({'item': s.series_id})
                    elif any(substring in s.series_description.upper() for substring in {'FLAIR'}):
                        info[flair_sag_T1w].append({'item': s.series_id})
                    elif any(substring in s.series_description.upper() for substring in {'SSFSE'}):
                            info[ssfse_cor_T1w].append({'item': s.series_id})
                            
            if any(substring in s.series_description.upper() for substring in {'DWI','DIFFUSION'}):
                if 'SAR' in s.series_description.upper() or 'SAFE' in s.protocol_name.upper():
                    info[dwi_electrode].append({'item': s.series_id})
                else:
                    info[dwi].append({'item': s.series_id})
                    
            if 'TRACE' in s.series_description.upper():
                if 'SAR' in s.series_description.upper() or 'SAFE' in s.protocol_name.upper():
                    info[trace_electrode].append({'item': s.series_id})
                else:
                    info[trace].append({'item': s.series_id})
   
            if any(substring in s.series_description.upper() for substring in {'DC','AVERAGE'}):
                if 'SAR' in s.series_description.upper() or 'SAFE' in s.protocol_name.upper():
                    info[avg_dc_electrode].append({'item': s.series_id})
                else:
                    info[avg_dc].append({'item': s.series_id})
            
            if any(substring in s.series_description.upper() for substring in {'FRACTIONAL','ANSIO','ANSIO.'}):
                if 'SAR' in s.series_description.upper() or 'SAFE' in s.protocol_name.upper():
                    info[fa_electrode].append({'item': s.series_id})
                else:
                    info[fa].append({'item': s.series_id})
                       
        #   CT SCANS 
        elif any(substring in s.study_description.upper() for substring in {'CT','HEAD'}):
            electrode_list = {'OVER','UNDER', 'ELECTRODE','ROUTINE','F_U_HEAD','F/U_HEAD', 'ER_HEAD'}
            frame_list     = {'STEROTACTIC','STEREOTACTIC','STEALTH','CTA_COW'}
            
            if any(substring in s.protocol_name.upper() for substring in electrode_list):
                if 'SCOUT' not in s.series_description.upper():
                    info[ct_electrode].append({'item': s.series_id})
            elif any(substring in s.protocol_name.upper() for substring in frame_list):
                if 'SCOUT' not in s.series_description.upper():
                    info[ct_frame].append({'item': s.series_id})
            else:
                if 'SCOUT' not in s.series_description.upper():
                    info[ct].append({'item': s.series_id})
                
        # INTRAOP X-RAY 
        elif any(substring in s.study_description.upper() for substring in {'INTRAOPERATIVE','SKULL','OT','XA','RF'}):
            if 'CR' not in s.study_description.upper():
                info[xr].append({'item': s.series_id})
        elif any(substring.upper() in s.image_type for substring in {'SINGLE PLANE'}):
                info[xr].append({'item': s.series_id})
                
    return info
