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
    # (D): DIS2D/DIS3D reconstruction incl
    # (#): multiples runs as run-#

    # MP2RAGE (D)
    # Sa2RAGE (D)
    # MEMP2RAGE 
    # T2 TSE (D,#)
    # multiband BOLD (#)
    # psf-dico BOLD (#)
    # diffusion (#)
    # EPI-PA field mapping
    # GRE field mapping
    # T2 SPACE (D)
    # TOF Angio (D)
    # ME GRE/susc  (D)
    # DIR T2 (D)

    #to do: 
        # add (D) for MEMP2RAGE


    #MP2RAGE

    t1w_mprage = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-MPRAGE_run-{item:02d}_T1w')
    DIS3D_t1w_mprage = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-MPRAGE_rec-DIS3D_run-{item:02d}_T1w')
    DIS2D_t1w_mprage = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-MPRAGE_rec-DIS2D_run-{item:02d}_T1w')

    inv1_mp2rage = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_inv-1_run-{item:02d}_MP2RAGE')
    inv2_mp2rage = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_inv-2_run-{item:02d}_MP2RAGE')
    t1map = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-MP2RAGE_run-{item:02d}_T1map')
    t1w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-MP2RAGE_run-{item:02d}_T1w')
    uni_mp2rage = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-UNI_run-{item:02d}_MP2RAGE')

        #Dist. corrected versions:
    DIS3D_inv1_mp2rage = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_inv-1_rec-DIS3D_run-{item:02d}_MP2RAGE')
    DIS3D_inv2_mp2rage = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_inv-2_rec-DIS3D_run-{item:02d}_MP2RAGE')
    DIS3D_t1map = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-MP2RAGE_rec-DIS3D_run-{item:02d}_T1map')
    DIS3D_t1w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-MP2RAGE_rec-DIS3D_run-{item:02d}_T1w')
    DIS3D_uni_mp2rage = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-UNI_rec-DIS3D_run-{item:02d}_MP2RAGE')

    DIS2D_inv1_mp2rage = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_inv-1_rec-DIS2D_run-{item:02d}_MP2RAGE')
    DIS2D_inv2_mp2rage = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_inv-2_rec-DIS2D_run-{item:02d}_MP2RAGE')
    DIS2D_t1map = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-MP2RAGE_rec-DIS2D_run-{item:02d}_T1map')
    DIS2D_t1w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-MP2RAGE_rec-DIS2D_run-{item:02d}_T1w')
    DIS2D_uni_mp2rage = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-UNI_rec-DIS2D_run-{item:02d}_MP2RAGE')


    inv_1_sa2rage = create_key('{bids_subject_session_dir}/fmap/{bids_subject_session_prefix}_inv-1_SA2RAGE')
    inv_2_sa2rage = create_key('{bids_subject_session_dir}/fmap/{bids_subject_session_prefix}_inv-2_SA2RAGE')
    b1map_sa2rage = create_key('{bids_subject_session_dir}/fmap/{bids_subject_session_prefix}_acq-b1map_SA2RAGE')
    b1Div_sa2rage = create_key('{bids_subject_session_dir}/fmap/{bids_subject_session_prefix}_acq-b1Div_SA2RAGE')

           #only calculated for DIS2D 
    DIS2D_inv_1_sa2rage = create_key('{bids_subject_session_dir}/fmap/{bids_subject_session_prefix}_inv-1_rec-DIS2D_SA2RAGE')
    DIS2D_inv_2_sa2rage = create_key('{bids_subject_session_dir}/fmap/{bids_subject_session_prefix}_inv-2_rec-DIS2D_SA2RAGE')
    DIS2D_b1Div_sa2rage = create_key('{bids_subject_session_dir}/fmap/{bids_subject_session_prefix}_acq-b1Div_rec-DIS2D_SA2RAGE')
    DIS2D_b1map_sa2rage = create_key('{bids_subject_session_dir}/fmap/{bids_subject_session_prefix}_acq-b1map_rec-DIS2D_SA2RAGE')
    DIS3D_b1map_sa2rage = create_key('{bids_subject_session_dir}/fmap/{bids_subject_session_prefix}_acq-b1map_rec-DIS3D_SA2RAGE')


    #T2w:
    #2D TSE
    t2_tse = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-TSE_run-{item:02d}_T2w')
    DIS2D_t2_tse = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-TSE_run-{item:02d}_rec-DIS2D_T2w')
    DIS3D_t2_tse = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-TSE_run-{item:02d}_rec-DIS3D_T2w')

    #2D TSE Transverse
    t2_tse_tra = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-TSEtra_run-{item:02d}_T2w')
    DIS2D_t2_tse_tra = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-TSEtra_rec-DIS2D_run-{item:02d}_T2w')
    DIS3D_t2_tse_tra = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-TSEtra_rec-DIS3D_run-{item:02d}_T2w')

    #2D TSE Coronal
    t2_tse_cor = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-TSEcor_run-{item:02d}_T2w')
    DIS2D_t2_tse_cor = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-TSEcor_rec-DIS2D_run-{item:02d}_T2w')
    DIS3D_t2_tse_cor = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-TSEcor_rec-DIS3D_run-{item:02d}_T2w')

    #PD:
    #2D TSE
    pd_tse = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-TSE_run-{item:02d}_PD')
    DIS2D_pd_tse = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-TSE_run-{item:02d}_rec-DIS2D_PD')
    DIS3D_pd_tse = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-TSE_run-{item:02d}_rec-DIS3D_PD')

    #2D TSE Transverse
    pd_tse_tra = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-TSEtra_run-{item:02d}_PD')
    DIS2D_pd_tse_tra = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-TSEtra_rec-DIS2D_run-{item:02d}_PD')
    DIS3D_pd_tse_tra = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-TSEtra_rec-DIS3D_run-{item:02d}_PD')

    #2D TSE Coronal
    pd_tse_cor = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-TSEcor_run-{item:02d}_PD')
    DIS2D_pd_tse_cor = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-TSEcor_rec-DIS2D_run-{item:02d}_PD')
    DIS3D_pd_tse_cor = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-TSEcor_rec-DIS3D_run-{item:02d}_PD')


    #combined PDT2
    #2D TSE
    pd_t2_tse = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_echo_acq-TSE_run-{item:02d}_PDT2')
    DIS2D_pd_t2_tse = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_echo_acq-TSE_run-{item:02d}_rec-DIS2D_PDT2')
    DIS3D_pd_t2_tse = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_echo_acq-TSE_run-{item:02d}_rec-DIS3D_PDT2')

    #2D TSE Transverse
    pd_t2_tse_tra = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_echo_acq-TSEtra_run-{item:02d}_PDT2')
    DIS2D_pd_t2_tse_tra = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_echo_acq-TSEtra_rec-DIS2D_run-{item:02d}_PDT2')
    DIS3D_pd_t2_tse_tra = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_echo_acq-TSEtra_rec-DIS3D_run-{item:02d}_PDT2')

    #2D TSE Coronal
    pd_t2_tse_cor = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_echo_acq-TSEcor_run-{item:02d}_PDT2')
    DIS2D_pd_t2_tse_cor = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_echo_acq-TSEcor_rec-DIS2D_run-{item:02d}_PDT2')
    DIS3D_pd_t2_tse_cor = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_echo_acq-TSEcor_rec-DIS3D_run-{item:02d}_PDT2')




    #Diffusion
    dwi = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_run-{item:02d}_dwi')
    
    #Hippo DWI
    dwi_hipp = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_acq-HIPPO_run-{item:02d}_dwi')
    dwi_hipp_ap = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_acq-HIPPO_dir-AP_run-{item:02d}_dwi')
    dwi_hipp_pa = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_acq-HIPPO_dir-PA_run-{item:02d}_dwi')

    #uFA
    dwi_ufa = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_acq-uFA_run-{item:02d}_dwi')
    dwi_ogse = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_run-{item:02d}_ogse')

    #Field Maps:

    #GRE phase diff 
    fmap_diff = create_key('{bids_subject_session_dir}/fmap/{bids_subject_session_prefix}_phasediff')
    fmap_magnitude = create_key('{bids_subject_session_dir}/fmap/{bids_subject_session_prefix}_magnitude')

    #T2 SPACE
    spc_T2w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-SPACE_run-{item:02d}_T2w')

    #Dist. corr. versions:
    DIS2D_spc_T2w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-SPACE_rec-DIS2D_run-{item:02d}_T2w')
    DIS3D_spc_T2w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-SPACE_rec-DIS3D_run-{item:02d}_T2w')

    #FLAIR
    spc_FLAIR = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-SPACE_run-{item:02d}_FLAIR')

    #Dist. corr. versions:
    DIS2D_spc_FLAIR = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-SPACE_rec-DIS2D_run-{item:02d}_FLAIR')
    DIS3D_spc_FLAIR = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-SPACE_rec-DIS3D_run-{item:02d}_FLAIR')


    #Time-of-flight Angio
    TOF_angio = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-TOF_angio')

    DIS2D_TOF_angio = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-TOF_rec-DIS2D_angio')
    DIS3D_TOF_angio = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-TOF_rec-DIS3D_angio')

    #MIPS
    DIS2D_TOF_SAG = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-TOF_rec-DIS2D_sagMIP')
    DIS2D_TOF_COR = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-TOF_rec-DIS2D_corMIP')
    DIS2D_TOF_TRA = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-TOF_rec-DIS2D_traMIP')

    #########################
    #### Multi-echo GRE #####
    #########################

    #Multi-echo GRE (Susc3D)
    mag_echo_GRE = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_part-mag_echo_GRE')
    phase_echo_GRE = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_part-phase_echo_GRE')

    DIS2D_mag_echo_GRE = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_part-mag_rec-DIS2D_echo_GRE')
    DIS2D_phase_echo_GRE = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_part-phase_rec-DIS2D_echo_GRE')
    DIS3D_mag_echo_GRE = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_part-mag_rec-DIS3D_echo_GRE')
    DIS3D_phase_echo_GRE = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_part-phase_rec-DIS3D_echo_GRE')

    #Derived T2 star - seem to only be calculated with DIS2D
    T2_star = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_T2star')
    DIS2D_T2_star = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_rec-DIS2D_T2star')
    DIS3D_T2_star = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_rec-DIS3D_T2star')

    #me-gre with compressed sensing
    mag_echo_CS_GRE = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-CS_run-{item:02d}_part-mag_echo_GRE')
    phase_echo_CS_GRE = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-CS_run-{item:02d}_part-phase_echo_GRE')    
    
    #aspire:
    DIS2D_aspire_mag_echo_GRE = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-ASPIRE_part-mag_rec-DIS2D_echo_GRE')
    DIS2D_aspire_phase_echo_GRE = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-ASPIRE_part-phase_rec-DIS2D_echo_GRE')
    DIS2D_aspire_T2_star_GRE = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-ASPIRE_rec-DIS2D_T2star')
    DIS2D_aspire_R2_star_GRE = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-ASPIRE_rec-DIS2D_R2star')
 

    # MEMP2RAGE #
    me_t1     = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_echo_acq-MP2RAGE_run-{item:02d}_T1w')
    me_t1map  = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_echo_acq-MP2RAGE_run-{item:02d}_T1map')
    me_t1inv1 = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_echo_inv-1_run-{item:02d}_MP2RAGE')
    me_t1inv2 = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_echo_inv-2_run-{item:02d}_MP2RAGE')
    me_t1uni  = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_echo_acq-UNI_run-{item:02d}_MP2RAGE')

    me_t1inv1_ce = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_inv-1_run-{item:02d}_MEMP2RAGE')
    me_t1_ce     = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-MEMP2RAGE_run-{item:02d}_T1w')
    me_t1inv2_ce = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_inv-2_run-{item:02d}_MEMP2RAGE')
    me_t1uni_ce  = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-UNI_run-{item:02d}_MEMP2RAGE')

    # DIR T2 #
    dir_t2       = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-DIR_T2w')
    DIS2D_dir_t2 = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-DIR_rec-DIS2D_T2w')

    #MT-on and MT-off GRE (magnetization transfer)
    mag_MT_on_GRE = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-MTon_run-{item:02d}_GRE')
    DIS2D_mag_MT_on_GRE = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-MTon_rec-DIS2D_run-{item:02d}_GRE')
    DIS3D_mag_MT_on_GRE = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-MTon_rec-DIS3D_run-{item:02d}_GRE')
    
    mag_MT_off_GRE = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-MToff_run-{item:02d}_GRE')
    DIS2D_mag_MT_off_GRE = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-MToff_rec-DIS2D_run-{item:02d}_GRE')
    DIS3D_mag_MT_off_GRE = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-MToff_rec-DIS3D_run-{item:02d}_GRE')


    movie = create_key('{bids_subject_session_dir}/func/{bids_subject_session_prefix}_task-movie_run-{item:02d}_bold')
    movie_sbref = create_key('{bids_subject_session_dir}/func/{bids_subject_session_prefix}_task-movie_run-{item:02d}_sbref')

    rest = create_key('{bids_subject_session_dir}/func/{bids_subject_session_prefix}_task-rest_run-{item:02d}_bold')
    rest_sbref = create_key('{bids_subject_session_dir}/func/{bids_subject_session_prefix}_task-rest_run-{item:02d}_sbref')


    info = { t1w_mprage:[], 
         DIS2D_t1w_mprage:[],
         DIS3D_t1w_mprage:[],
         inv1_mp2rage:[],t1map:[],t1w:[],uni_mp2rage:[],inv2_mp2rage:[],
         DIS2D_inv1_mp2rage:[],DIS2D_t1map:[],DIS2D_t1w:[],DIS2D_inv2_mp2rage:[],DIS2D_uni_mp2rage:[],
         DIS3D_inv1_mp2rage:[],DIS3D_t1map:[],DIS3D_t1w:[],DIS3D_inv2_mp2rage:[],DIS3D_uni_mp2rage:[],
         me_t1:[],me_t1map:[],me_t1inv1:[],me_t1inv1:[],me_t1inv2:[],me_t1uni:[],
         me_t1inv1_ce:[],me_t1_ce:[],me_t1inv2_ce:[],me_t1uni_ce:[],
         TOF_angio:[], DIS2D_TOF_SAG:[], DIS2D_TOF_COR:[], DIS2D_TOF_TRA:[], DIS2D_TOF_angio:[], DIS3D_TOF_angio:[],
         mag_echo_GRE:[],
         phase_echo_GRE:[],
         
         mag_echo_CS_GRE:[],
         phase_echo_CS_GRE:[],
    
         DIS2D_aspire_mag_echo_GRE:[],
         DIS2D_aspire_phase_echo_GRE:[],
         DIS2D_aspire_T2_star_GRE:[],
         DIS2D_aspire_R2_star_GRE:[],

        
         DIS2D_mag_echo_GRE:[],
         DIS2D_phase_echo_GRE:[],
         DIS3D_mag_echo_GRE:[],
         DIS3D_phase_echo_GRE:[],
         mag_MT_on_GRE:[],
         DIS2D_mag_MT_on_GRE:[],
         DIS3D_mag_MT_on_GRE:[],

         mag_MT_off_GRE:[],
         DIS2D_mag_MT_off_GRE:[],
         DIS3D_mag_MT_off_GRE:[],


         T2_star:[],
         DIS2D_T2_star:[],
         DIS3D_T2_star:[],

         spc_T2w:[], DIS2D_spc_T2w:[], DIS3D_spc_T2w:[],
         spc_FLAIR:[], DIS2D_spc_FLAIR:[], DIS3D_spc_FLAIR:[],
            
         inv_1_sa2rage:[],inv_2_sa2rage:[],b1Div_sa2rage:[],b1map_sa2rage:[],
         DIS2D_inv_1_sa2rage:[],DIS2D_inv_2_sa2rage:[],DIS2D_b1Div_sa2rage:[],DIS2D_b1map_sa2rage:[],
         DIS3D_b1map_sa2rage:[],

         t2_tse:[], DIS2D_t2_tse:[], DIS3D_t2_tse:[],
         t2_tse_tra:[], DIS2D_t2_tse_tra:[], DIS3D_t2_tse_tra:[],
         t2_tse_cor:[], DIS2D_t2_tse_cor:[], DIS3D_t2_tse_cor:[],

         pd_tse:[], DIS2D_pd_tse:[], DIS3D_pd_tse:[],
         pd_tse_tra:[], DIS2D_pd_tse_tra:[], DIS3D_pd_tse_tra:[],
         pd_tse_cor:[], DIS2D_pd_tse_cor:[], DIS3D_pd_tse_cor:[],

         pd_t2_tse:[], DIS2D_pd_t2_tse:[], DIS3D_pd_t2_tse:[],
         pd_t2_tse_tra:[], DIS2D_pd_t2_tse_tra:[], DIS3D_pd_t2_tse_tra:[],
         pd_t2_tse_cor:[], DIS2D_pd_t2_tse_cor:[], DIS3D_pd_t2_tse_cor:[],

         dwi:[],dwi_ufa:[],dwi_ogse:[],
         dwi_hipp:[],dwi_hipp_ap:[],dwi_hipp_pa:[],
         fmap_diff:[],fmap_magnitude:[],
         dir_t2:[], DIS2D_dir_t2:[]}

    info[rest]=[]
    info[rest_sbref]=[]
    info[movie]=[]
    info[movie_sbref]=[]

    for idx, s in enumerate(seqinfo):

    

    #memp2rage
        if ('memp2rage' in s.protocol_name):
            if ('UNI-DEN' in (s.series_description).strip()):
                if ('combEcho' in (s.series_description).strip()):
                    info[me_t1_ce].append({'item': s.series_id})
                else:
                    info[me_t1].append({'item': s.series_id})
            if ('INV1' in (s.series_description).strip()):
                if ('combEcho' in (s.series_description).strip()):
                    info[me_t1inv1_ce].append({'item': s.series_id})
                else:
                    info[me_t1inv1].append({'item': s.series_id})
            if ('INV2' in (s.series_description).strip()):
                if ('combEcho' in (s.series_description).strip()):
                    info[me_t1inv2_ce].append({'item': s.series_id})
                else:
                    info[me_t1inv2].append({'item': s.series_id})
            if ('UNI_Images' in (s.series_description).strip()):
                if ('combEcho' in (s.series_description).strip()):
                    info[me_t1uni_ce].append({'item': s.series_id})
                else:
                    info[me_t1uni].append({'item': s.series_id})
            if ('T1_Images' in (s.series_description).strip()):
                info[me_t1map].append({'item': s.series_id})



        #mp2rage
        if ('mp2rage' in s.series_description.lower()  and (not 'memp2rage' in s.series_description.lower() ) ):
            if ('INV1' in (s.series_description).strip()):
                if ('DIS2D' in (s.image_type[3].strip())):
                    info[DIS2D_inv1_mp2rage].append({'item': s.series_id})
                if ('DIS3D' in (s.image_type[3].strip())):
                    info[DIS3D_inv1_mp2rage].append({'item': s.series_id})
                if ('ND' in (s.image_type[3].strip())):
                    info[inv1_mp2rage].append({'item': s.series_id})
            if ('T1_Images' in (s.series_description).strip()):
                if ('DIS2D' in (s.image_type[3].strip())):
                    info[DIS2D_t1map].append({'item': s.series_id})                                
                if ('DIS3D' in (s.image_type[3].strip())):
                    info[DIS3D_t1map].append({'item': s.series_id})
                if ('ND' in (s.image_type[3].strip())):
                    info[t1map].append({'item': s.series_id})
            if ('UNI-DEN' in (s.series_description).strip()):
                if ('ND' in (s.image_type[3].strip())):
                    info[t1w].append({'item': s.series_id})
                elif ('DIS2D' in (s.image_type[4].strip())):
                    info[DIS2D_t1w].append({'item': s.series_id})
                elif ('DIS3D' in (s.image_type[4].strip())):
                    info[DIS3D_t1w].append({'item': s.series_id})
            if ('UNI_Images' in (s.series_description).strip()):
                if ('DIS2D' in (s.image_type[3].strip())):
                    info[DIS2D_uni_mp2rage].append({'item': s.series_id})
                if ('DIS3D' in (s.image_type[3].strip())):
                    info[DIS3D_uni_mp2rage].append({'item': s.series_id})
                if ('ND' in (s.image_type[3].strip())):
                    info[uni_mp2rage].append({'item': s.series_id})
            if ('_INV2' in (s.series_description).strip()):
                if ('DIS2D' in (s.image_type[3].strip())):
                    info[DIS2D_inv2_mp2rage].append({'item': s.series_id})
                if ('DIS3D' in (s.image_type[3].strip())):
                    info[DIS3D_inv2_mp2rage].append({'item': s.series_id})
                if ('ND' in (s.image_type[3].strip())):
                    info[inv2_mp2rage].append({'item': s.series_id})


        if ('mprage' in s.protocol_name or 'T1w' in s.protocol_name or 'MPRAGE' in s.protocol_name):
            if ('DIS2D' in (s.image_type[3].strip())):
                info[DIS2D_t1w_mprage].append({'item': s.series_id})
            if ('DIS3D' in (s.image_type[3].strip())):
                info[DIS3D_t1w_mprage].append({'item': s.series_id})
            if ('ND' in (s.image_type[3].strip())):
                info[t1w_mprage].append({'item': s.series_id})


    #double inversion recovery t2 space
    #note: for all distortion corrected data, no protocol name due to post-scan processing
    #      therfore, s.series_description is used instead
        if ('spc_dir' in (s.series_description).strip()):
            if ('DIS2D' in (s.series_description).strip()):
                info[DIS2D_dir_t2].append({'item': s.series_id})
            else:
                info[dir_t2].append({'item': s.series_id})


    #sa2rage
        if ('sa2rage' in s.series_description):
            if ('ND' in (s.image_type[3].strip())):
                if ('invContrast1' in s.series_description or 'INV1' in s.series_description):
                    info[inv_1_sa2rage] = [s.series_id]
                if ('invContrast2' in s.series_description or 'INV2' in s.series_description):
                    info[inv_2_sa2rage] = [s.series_id]
                if ('OTHER' in (s.image_type[2].strip())):
                    info[b1map_sa2rage] = [s.series_id]
                if ('b1DivImg' in s.series_description or 'UNI' in s.series_description):
                    info[b1Div_sa2rage] = [s.series_id]
            if ('DIS2D' in (s.image_type[3].strip())):
                if ('invContrast1' in s.series_description):
                    info[DIS2D_inv_1_sa2rage] = [s.series_id]
                if ('invContrast2' in s.series_description):
                    info[DIS2D_inv_2_sa2rage] = [s.series_id]
                if ('OTHER' in (s.image_type[2].strip())):
                    info[DIS2D_b1map_sa2rage] = [s.series_id]
                if ('b1DivImg' in s.series_description):
                    info[DIS2D_b1Div_sa2rage] = [s.series_id]
            if ('DIS3D' in (s.image_type[3].strip())):
                if ('OTHER' in (s.image_type[2].strip())):
                    info[DIS3D_b1map_sa2rage] = [s.series_id]

  
        #t2 tse
    #tse tra T2w


        if ('pd_t2_tse_tra' in s.series_description or 'pd+t2_tse_tra' in s.series_description): 
                if ('ND' in (s.image_type[3].strip())):
                    info[pd_t2_tse_tra].append({'item': s.series_id})
                if ('DIS3D' in (s.image_type[3].strip())):
                    info[DIS3D_pd_t2_tse_tra].append({'item': s.series_id})
                if ('DIS2D' in (s.image_type[3].strip())):
                    info[DIS2D_pd_t2_tse_tra].append({'item': s.series_id})


                #tse cor T2w
        elif ('pd_t2_tse_cor' in s.series_description or 'pd+t2_tse_cor' in s.series_description): 
                if ('ND' in (s.image_type[3].strip())):
                    info[pd_t2_tse_cor].append({'item': s.series_id})
                if ('DIS3D' in (s.image_type[3].strip())):
                    info[DIS3D_pd_t2_tse_cor].append({'item': s.series_id})
                if ('DIS2D' in (s.image_type[3].strip())):
                    info[DIS2D_pd_t2_tse_cor].append({'item': s.series_id})

        elif ('pd_t2_tse' in s.series_description or 'pd+t2_tse' in s.series_description): 
                if ('ND' in (s.image_type[3].strip())):
                    info[pd_t2_tse].append({'item': s.series_id})
                if ('DIS3D' in (s.image_type[3].strip())):
                    info[DIS3D_pd_t2_tse].append({'item': s.series_id})
                if ('DIS2D' in (s.image_type[3].strip())):
                    info[DIS2D_pd_t2_tse].append({'item': s.series_id})



        elif ('t2_tse_tra' in s.series_description): 
                if ('ND' in (s.image_type[3].strip())):
                    info[t2_tse_tra].append({'item': s.series_id})
                if ('DIS3D' in (s.image_type[3].strip())):
                    info[DIS3D_t2_tse_tra].append({'item': s.series_id})
                if ('DIS2D' in (s.image_type[3].strip())):
                    info[DIS2D_t2_tse_tra].append({'item': s.series_id})


                #tse cor T2w
        elif ('t2_tse_cor' in s.series_description): 
                if ('ND' in (s.image_type[3].strip())):
                    info[t2_tse_cor].append({'item': s.series_id})
                if ('DIS3D' in (s.image_type[3].strip())):
                    info[DIS3D_t2_tse_cor].append({'item': s.series_id})
                if ('DIS2D' in (s.image_type[3].strip())):
                    info[DIS2D_t2_tse_cor].append({'item': s.series_id})


        elif ('t2_tse' in s.series_description): 
                if ('ND' in (s.image_type[3].strip())):
                    info[t2_tse].append({'item': s.series_id})
                if ('DIS3D' in (s.image_type[3].strip())):
                    info[DIS3D_t2_tse].append({'item': s.series_id})
                if ('DIS2D' in (s.image_type[3].strip())):
                    info[DIS2D_t2_tse].append({'item': s.series_id})

        if ('pd_tse_tra' in s.series_description): 
                if ('ND' in (s.image_type[3].strip())):
                    info[pd_tse_tra].append({'item': s.series_id})
                if ('DIS3D' in (s.image_type[3].strip())):
                    info[DIS3D_pd_tse_tra].append({'item': s.series_id})
                if ('DIS2D' in (s.image_type[3].strip())):
                    info[DIS2D_pd_tse_tra].append({'item': s.series_id})


                #tse cor T2w
        elif ('pd_tse_cor' in s.series_description): 
                if ('ND' in (s.image_type[3].strip())):
                    info[pd_tse_cor].append({'item': s.series_id})
                if ('DIS3D' in (s.image_type[3].strip())):
                    info[DIS3D_pd_tse_cor].append({'item': s.series_id})
                if ('DIS2D' in (s.image_type[3].strip())):
                    info[DIS2D_pd_tse_cor].append({'item': s.series_id})


        elif ('pd_tse' in s.series_description): 
                if ('ND' in (s.image_type[3].strip())):
                    info[pd_tse].append({'item': s.series_id})
                if ('DIS3D' in (s.image_type[3].strip())):
                    info[DIS3D_pd_tse].append({'item': s.series_id})
                if ('DIS2D' in (s.image_type[3].strip())):
                    info[DIS2D_pd_tse].append({'item': s.series_id})



                          #gre field map   
        if ('field_mapping' in s.protocol_name):   
            if (s.dim4 == 1) and ('gre_field_mapping' == (s.series_description).strip()):
                if('P' in (s.image_type[2].strip()) ):
                    info[fmap_diff].append({'item': s.series_id})
                if('M' in (s.image_type[2].strip()) ):
                    info[fmap_magnitude].append({'item': s.series_id})

        #dwi
        if len(s.image_type) > 2 :
            if (('DIFFUSION' in s.image_type[2].strip()) and ('ORIGINAL' in s.image_type[0].strip())):
                if ('cb_ep2d_diff_C26' in s.series_description):
                    info[dwi_ogse].append({'item': s.series_id})
                elif ('UFA' in s.series_description ):
                    info[dwi_ufa].append({'item': s.series_id})
                elif ('HIPPO_DTI' in s.series_description ):
                    if ('_AP' in s.series_description):
                        info[dwi_hipp_ap].append({'item': s.series_id})
                    elif ('_PA' in s.series_description):
                        info[dwi_hipp_pa].append({'item': s.series_id})
                    else:
                        info[dwi_hipp].append({'item': s.series_id})
                else:
                    info[dwi].append({'item': s.series_id})

            elif ('Movie' in (s.series_description).strip()):
                if (s.dim4==1 and  'SBRef' in (s.series_description).strip()):
                    info[movie_sbref].append({'item': s.series_id})
                elif (s.dim4>1):
                    info[movie].append({'item': s.series_id})

            elif ('bold' in s.protocol_name or 'resting_state' in s.series_description or 'mbep2d' in (s.series_description).strip() or 'ep_bold' in (s.series_description).strip() ):
            
                if ('SBRef' in (s.series_description).strip()):
                    info[rest_sbref].append({'item': s.series_id})
                else: # greater than 1 timepoint:
                    info[rest].append({'item': s.series_id})
 
    
            
        #susceptibility ND multiecho
        if ('susc' in s.series_description or 'gre3d' in s.series_description or 't1_fl3d_p4_iso' in s.series_description ):
            if ('M' in (s.image_type[2].strip())):
                 if ('ND' in (s.image_type[3].strip())):
                    info[mag_echo_GRE] =  [s.series_id]
                 if ('DIS2D' in (s.image_type[3].strip())):
                    info[DIS2D_mag_echo_GRE] =  [s.series_id]
                 if ('DIS3D' in (s.image_type[3].strip())):
                    info[DIS3D_mag_echo_GRE] =  [s.series_id]

            if ('P' in (s.image_type[2].strip())):
                 if ('ND' in (s.image_type[3].strip())):
                    info[phase_echo_GRE] =  [s.series_id]
                 if ('DIS2D' in (s.image_type[3].strip())):
                    info[DIS2D_phase_echo_GRE] =  [s.series_id]
                 if ('DIS3D' in (s.image_type[3].strip())):
                    info[DIS3D_phase_echo_GRE] =  [s.series_id]

        #susceptibility ND multiecho
        if ('ASPIRE' in s.series_description ):
            if 'R2star' in s.series_description:
                 if ('DIS2D' in (s.image_type[3].strip())):
                    info[DIS2D_aspire_R2_star_GRE] =  [s.series_id]
            elif 'T2star' in s.series_description:
                  if ('DIS2D' in (s.image_type[3].strip())):
                    info[DIS2D_aspire_T2_star_GRE] =  [s.series_id]
            elif len(s.image_type) > 3 :
                if (('M' in (s.image_type[2].strip()) ) and ('ASPIRE' not in s.image_type )):
                     if ('DIS2D' in (s.image_type[3].strip())):
                        info[DIS2D_aspire_mag_echo_GRE] =  [s.series_id]
                if ('P' in (s.image_type[2].strip()) and len(s.image_type) >4):
                     if ('DIS2D' in (s.image_type[4].strip())):
                        info[DIS2D_aspire_phase_echo_GRE] =  [s.series_id]

           
        #multi-echo GRE with compressed sensing
        if ('gre_CS_C41' in s.series_description):
            if ('M' in (s.image_type[2].strip())):
                 if ('ND' in (s.image_type[3].strip())):
                    info[mag_echo_CS_GRE] =  [s.series_id]
                

            if ('P' in (s.image_type[2].strip())):
                 if ('ND' in (s.image_type[3].strip())):
                    info[phase_echo_CS_GRE] =  [s.series_id]
      

        # MTon GRE (excludes phase image since not needed)
        if ('gre_ptx_MT_On' in s.series_description ):
            if ('M' in (s.image_type[2].strip())):
                 if ('ND' in (s.image_type[3].strip())):
                    info[mag_MT_on_GRE].append({'item': s.series_id})
                 if ('DIS2D' in (s.image_type[3].strip())):
                    info[DIS2D_mag_MT_on_GRE].append({'item': s.series_id})
                 if ('DIS3D' in (s.image_type[3].strip())):
                    info[DIS3D_mag_MT_on_GRE].append({'item': s.series_id})
        #MToff GRE
        if ('gre_ptx_MT_Off' in s.series_description ):
            if ('M' in (s.image_type[2].strip())):
                 if ('ND' in (s.image_type[3].strip())):
                    info[mag_MT_off_GRE].append({'item': s.series_id})
                 if ('DIS2D' in (s.image_type[3].strip())):
                    info[DIS2D_mag_MT_off_GRE].append({'item': s.series_id})
                 if ('DIS3D' in (s.image_type[3].strip())):
                    info[DIS3D_mag_MT_off_GRE].append({'item': s.series_id})

                    

        #T2star
        if ('T2Star' in s.series_description):
            if ('ND' in (s.image_type[3].strip())):
                info[T2_star].append({'item': s.series_id})
            if ('DIS2D' in (s.image_type[3].strip())):
                info[DIS2D_T2_star].append({'item': s.series_id})
            if ('DIS3D' in (s.image_type[3].strip())):
                info[DIS3D_T2_star].append({'item': s.series_id})

        #spc T2w
        if ('spc_T2' in s.series_description or 'T2w_SPC' in s.series_description or 'T2w_space' in s.series_description or 't2_space' in s.series_description or 't2_spc' in s.series_description or 'T2_spc' in s.series_description ): 
            if ('dark-fluid' not in s.series_description ):
                if ('ND' in (s.image_type[3].strip())):
                    info[spc_T2w].append({'item': s.series_id})
                if ('DIS2D' in (s.image_type[3].strip())):
                    info[DIS2D_spc_T2w].append({'item': s.series_id})
                if ('DIS3D' in (s.image_type[3].strip())):
                    info[DIS3D_spc_T2w].append({'item': s.series_id})
    
        #spc T2w  
        if ('spc_flair' in s.series_description or 'dark-fluid' in s.series_description): 
            if ('ND' in (s.image_type[3].strip())):
                info[spc_FLAIR].append({'item': s.series_id})
            if ('DIS2D' in (s.image_type[3].strip())):
                info[DIS2D_spc_FLAIR].append({'item': s.series_id})
            if ('DIS3D' in (s.image_type[3].strip())):
                info[DIS3D_spc_FLAIR].append({'item': s.series_id})

        #TOF angio
        if ('3D_TOF' in s.series_description or 'tof_fl3d' in s.series_description): 
            if (s.dim3>1):
                if ('ND' in (s.image_type[3].strip())):
                    info[TOF_angio] = [s.series_id]
                if ('DIS2D' in (s.image_type[3].strip())):
                    info[DIS2D_TOF_angio] = [s.series_id]
                if ('DIS3D' in (s.image_type[3].strip())):
                    info[DIS3D_TOF_angio] = [s.series_id]
            if (s.dim4==1):
                if ('DIS2D' in (s.image_type[3].strip())):
                    if ('SAG' in (s.series_description).strip()):
                        info[DIS2D_TOF_SAG] = [s.series_id]
                    if ('COR' in (s.series_description).strip()):
                        info[DIS2D_TOF_COR] = [s.series_id]
                    if ('TRA' in (s.series_description).strip()):
                        info[DIS2D_TOF_TRA] = [s.series_id]

   
    return info
