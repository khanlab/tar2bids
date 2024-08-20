from heudiconv.utils import set_readonly, save_json
import json
import logging
from pybruker.jcamp import jcamp_read
import pydicom

lgr = logging.getLogger("heudiconv")

def create_key(template, outtype=('nii.gz',), annotation_classes=None):
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
    dwi = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_run-{item:02d}_dwi')

    MP2RAGE_invs = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-Inversions_run-{item:02d}_MP2RAGE')
    MP2RAGE_UNI = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-UNI_run-{item:02d}_T1w')

    MP2RAGE_invs_l = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-LoResInversions_run-{item:02d}_MP2RAGE')
    MP2RAGE_UNI_l = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-LoResUNI_run-{item:02d}_T1w')


    MEGRE_mag = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_part-mag_echo_run-{item:02d}_GRE')
    MEGRE_complex = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_part-complex_echo_run-{item:02d}_GRE')


    T2_TurboRARE = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-TurboRARE_run-{item:02d}_T2w')

    # where does bids_subject_session_prefix come from? or item? heudiconv special variables? can we get the task type (visual/audio) somehow?
    BLOCK_EPI =  create_key('{bids_subject_session_dir}/func/{bids_subject_session_prefix}_task-unknown_acq-BlockEPI_run-{item:02d}_bold')

    info = { FLASH_T1:[],FLASH_MT_ON:[],FLASH_MT_OFF:[],dwi:[],MP2RAGE_invs:[],MP2RAGE_UNI:[],MP2RAGE_invs_l:[],MP2RAGE_UNI_l:[],MEGRE_mag:[],MEGRE_complex:[],T2_TurboRARE:[],BLOCK_EPI:[]}

    for idx, s in enumerate(seqinfo):

    
        #FLASH
        if ('T1_FLASH' in s.protocol_name):
            info[FLASH_T1].append({'item': s.series_id})
        elif ('FLASH3D_MT' in s.protocol_name):
            if ('OFF' in s.series_description.strip()):
                info[FLASH_MT_OFF].append({'item': s.series_id})
            else:
                info[FLASH_MT_ON].append({'item': s.series_id})
                
        elif ('dti' in s.protocol_name.lower()):
            info[dwi].append({'item': s.series_id})
        
        elif ('cfmmMP2RAGE' in s.series_description.strip()):
          if (s.dim1 > 64):
            if  ('0001' in s.dcm_dir_name.strip()):
                info[MP2RAGE_invs].append({'item': s.series_id})
            elif  ('0002' in s.dcm_dir_name.strip()):
                info[MP2RAGE_UNI].append({'item': s.series_id})
          else:
            if  ('0001' in s.dcm_dir_name.strip()):
                info[MP2RAGE_invs_l].append({'item': s.series_id})
            elif  ('0002' in s.dcm_dir_name.strip()):
                info[MP2RAGE_UNI_l].append({'item': s.series_id})

        elif ('T2star' in s.series_description.strip()):
            if (s.dim3 == 2 and s.dim4 < 12): #to cover the case when dim3=2 could refer to 2 echos, instead of real/imag..
                info[MEGRE_complex].append({'item': s.series_id})
            else:
                info[MEGRE_mag].append({'item': s.series_id})
        elif ( 'T2_TurboRARE' in s.series_description.strip()):
            info[T2_TurboRARE].append({'item': s.series_id})
        elif ( 'blockEPI' in s.series_description.strip()):
            info[BLOCK_EPI].append({'item': s.series_id})
   
    return info

def custom_callable(outfile, outtype, infiles):
    dcm_filename = infiles[0]
    bruker_parameters_jcamp = pydicom.read_file(dcm_filename, stop_before_pixels=True).get((0x0177, 0x1100))
    if bruker_parameters_jcamp:
        jcamp_dict = jcamp_read(bruker_parameters_jcamp.value)
        scaninfo_filename = outfile + '.json'
        lgr.info(f"Adding bruker parameters to {scaninfo_filename}")
        with open(scaninfo_filename, 'r') as f:
            info_dict = json.load(f)
        info_dict['cfmm_bruker_parameters'] = jcamp_dict
        # if blockEPI then use bruker parameters to create events.tsv
        save_json(scaninfo_filename, info_dict)
        set_readonly(scaninfo_filename)
