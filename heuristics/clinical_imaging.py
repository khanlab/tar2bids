# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 22:57:55 2019

@author: Greydon
"""

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
	
	#Anat
	t1w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_run-{item:02d}_T1w')
	t1w_acq = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-{acq}_run-{item:02d}_T1w')
	t2w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-{acq}_run-{item:02d}_T2w')
	t1w_pd = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-{acq}_run-{item:02d}_PD')
	t1w_flair = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-{acq}_run-{item:02d}_FLAIR')
	fa = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_run-{item:02d}_angio')
	fa_acq = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-{acq}_run-{item:02d}_angio')
	
	#fmap
	fmap = create_key('{bids_subject_session_dir}/fmap/{bids_subject_session_prefix}_run-{item:02d}_epi')
	fmap_acq = create_key('{bids_subject_session_dir}/fmap/{bids_subject_session_prefix}_acq-{acq}_run-{item:02d}_epi')

	#Diffusion
	dwi = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_run-{item:02d}_dwi')
	dwi_acq = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_acq-{acq}_run-{item:02d}_dwi')
	
	#CT
	ct = create_key('{bids_subject_session_dir}/ct/{bids_subject_session_prefix}_run-{item:02d}_ct')
	ct_acq = create_key('{bids_subject_session_dir}/ct/{bids_subject_session_prefix}_acq-{acq}_run-{item:02d}_ct')
	
	info = {t1w:[],
			t1w_acq:[],
			t2w:[],
			t1w_pd:[],
			t1w_flair:[],
			fmap:[],
			fmap_acq:[],
			dwi:[],
			dwi_acq:[],
			fa:[],
			fa_acq:[],
			ct:[],
			ct_acq:[]}
	
	for idx, s in enumerate(seqinfo):
		if any(substring in s.study_description.upper() for substring in {'MR'}):
			postop = False
			if 'SAR' in s.series_description.upper() or any(x in s.protocol_name.upper() for x in {'SAFE', 'STIMULATOR', 'STIM SAFE', 'POST', 'POST OP','POST-OP'}):
				if 'POST' in s.protocol_name.upper():
					if 'GAD' not in s.series_description.upper():
						postop = True
				else:
					postop = True
				
			if any(substring in s.series_description.upper() for substring in {'STEALTH','3D','STEREO'}) and not any(substring in s.series_description.upper() for substring in {'IR_FSPGR', 'FSPGR'}):
				if any(substring in s.series_description.upper() for substring in {'IR_FSPGR', 'FSPGR', 'IR-FSPGR'}):
					if postop:
						info[t1w_acq].append({'item': s.series_id, 'acq': 'ElectrodeFSPGR'})
					else:
						info[t1w_acq].append({'item': s.series_id, 'acq': 'FSPGR'})
				elif 'MPGR' in s.series_description.upper():
					if postop:
						info[t1w_acq].append({'item': s.series_id, 'acq': 'ElectrodeMPGR'})
					elif 'AX' in s.series_description.upper():
						info[t1w_acq].append({'item': s.series_id, 'acq': 'MPGR2D'})
					else:
						info[t1w_acq].append({'item': s.series_id, 'acq': 'MPGR3D'})
				else:
					if postop:
						if 'T2' in s.series_description.upper():
							info[t2w].append({'item': s.series_id, 'acq': 'Electrode3D'})
						else:
							info[t1w_acq].append({'item': s.series_id, 'acq': 'Electrode3D'})
					else:
						info[t1w].append({'item': s.series_id})
					
			elif 'EPI' in s.series_description.upper():
				if postop:
					info[fmap_acq].append({'item': s.series_id, 'acq': 'Electrode'})
				elif 'T2' in s.series_description.upper():
					info[fmap].append({'item': s.series_id})
					
			elif 'MPGR' in s.series_description.upper():
				if postop:
					info[t1w_acq].append({'item': s.series_id, 'acq': 'ElectrodeMPGR'})
				elif 'AX' in s.series_description.upper():
					info[t1w_acq].append({'item': s.series_id, 'acq': 'MPGR2D'})
				else:
					info[t1w_acq].append({'item': s.series_id, 'acq': 'MPGR3D'})
					
			elif any(substring in s.series_description.upper() for substring in {'IR_FSPGR', 'FSPGR','IR-FSPGR'}):
				if postop:
					info[t1w_acq].append({'item': s.series_id, 'acq': 'ElectrodeFSPGR'})
				else:
					info[t1w_acq].append({'item': s.series_id, 'acq': 'FSPGR'})
			
			elif any(substring in s.series_description.upper() for substring in {'AX', 'COR','SAG'}) and ('3D' not in s.series_description.upper()):
				if ('AX' in s.series_description.upper()):
					orientation = 'Tra'
				elif ('COR' in s.series_description.upper()):
					orientation = 'Cor'
				elif ('SAG' in s.series_description.upper()):
					orientation = 'Sag'
				
				if postop:
					if any(substring in s.series_description.upper() for substring in {'T2', '2D'}):
						info[t2w].append({'item': s.series_id, 'acq': 'Electrode' + orientation})
					elif any(substring in s.series_description.upper() for substring in {'PD'}):
						info[t1w_pd].append({'item': s.series_id, 'acq': 'Electrode' + orientation})
					elif any(substring in s.series_description.upper() for substring in {'FLAIR'}):
						info[t1w_flair].append({'item': s.series_id, 'acq': 'Electrode' + orientation})
				else:
					if any(substring in s.series_description.upper() for substring in {'T2','2D'}):
						info[t2w].append({'item': s.series_id, 'acq': orientation})
					elif any(substring in s.series_description.upper() for substring in {'PD'}):
						info[t1w_pd].append({'item': s.series_id, 'acq': orientation})
					elif any(substring in s.series_description.upper() for substring in {'FLAIR'}):
						info[t1w_flair].append({'item': s.series_id, 'acq': orientation})
					elif any(substring in s.series_description.upper() for substring in {'SSFSE'}):
						info[t1w_acq].append({'item': s.series_id, 'acq': 'SSFSE' + orientation})
						
			elif any(substring in s.series_description.upper() for substring in {'DWI', 'DTI', 'DIFFUSION'}):
				if postop:
					info[dwi_acq].append({'item': s.series_id, 'acq': 'Electrode'})
				else:
					info[dwi].append({'item': s.series_id})

			elif any(substring in s.series_description.upper() for substring in {'FRACTIONAL', 'ANSIO', 'ANSIO.'}):
				if postop:
					info[fa_acq].append({'item': s.series_id, 'acq': 'Electrode'})
				else:
					info[fa].append({'item': s.series_id})
					   
		#   CT SCANS 
		elif any(substring in s.study_description.upper() for substring in {'CT'}):
			electrode_list = {'OVER', 'UNDER', 'ELECTRODE', 'ROUTINE', 'F_U_HEAD', 'F/U_HEAD', 'ER_HEAD', 'POST', 'POST OP'}
			frame_list = {'STEROTACTIC', 'STEREOTACTIC', 'STEALTH', 'CTA_COW'}
			
			if ('SCOUT' not in s.series_description.upper()):
				if any(substring in s.protocol_name.upper() for substring in electrode_list):
					info[ct_acq].append({'item': s.series_id, 'acq': 'Electrode'})
				elif any(substring in s.protocol_name.upper() for substring in frame_list):
					info[ct_acq].append({'item': s.series_id, 'acq': 'Frame'})
				else:
					info[ct].append({'item': s.series_id})
				
	return info
