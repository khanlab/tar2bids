import os
import numpy
from cfmm import infotodict as cfmminfodict
from cfmm import create_key

def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """

    # call cfmm for general labelling and get dictionary
    info = cfmminfodict(seqinfo)

    # delete all functional keys from cfmm
    rest = create_key('sub-{subject}/func/sub-{subject}_task-rest_run-{item:02d}_bold')
    rest_sbref = create_key('sub-{subject}/func/sub-{subject}_task-rest_run-{item:02d}_sbref')

    rest_psf = create_key('sub-{subject}/func/sub-{subject}_acq-psf_task-rest_run-{item:02d}_bold')
    rest_psf_dico = create_key('sub-{subject}/func/sub-{subject}_acq-psf_task-rest_run-{item:02d}_rec-dico_bold')

    movie = create_key('sub-{subject}/func/sub-{subject}_task-movie_run-{item:02d}_bold')
    movie_sbref = create_key('sub-{subject}/func/sub-{subject}_task-movie_run-{item:02d}_sbref')

    info.pop(rest)
    info.pop(rest_sbref)
    info.pop(rest_psf)
    info.pop(rest_psf_dico)
    info.pop(movie)
    info.pop(movie_sbref)

    # create functional keys
    task_ge = create_key('sub-{subject}/func/sub-{subject}_task-{task}_acq-ge_part-mag_run-{run}_bold')
    task_ge_phase = create_key('sub-{subject}/func/sub-{subject}_task-{task}_acq-ge_part-phase_run-{run}_bold')
    task_se = create_key('sub-{subject}/func/sub-{subject}_task-{task}_acq-se_run-{run}_bold')

    # add functional keys to the dictionary
    info[task_ge]=[]
    info[task_ge_phase]=[]
    info[task_se]=[]

    # Now we loop through seqinfo again to grab just the functional files
    # the tasks are told apart by the length of the runs (will also ignore partial runs)
    # also save acquisition time in mag and phase list
    magacq=[]
    semagacq=[]
    phaseacq=[]
    for idx, s in enumerate(seqinfo):
        if ('bold' in s.protocol_name):
            if ('se' in (s.sequence_name).strip()):
                if (s.dim4==102):
                    if ('M' in (s.image_type[2].strip())):
                        info[task_se].append({'item': s.series_id, 'acqtime': s.acquisition_time, 'task': 'checkerboard'})
                        semagacq.append(float(s.acquisition_time))
                elif (s.dim4==64):
                    if ('M' in (s.image_type[2].strip())):
                        info[task_se].append({'item': s.series_id, 'acqtime': s.acquisition_time, 'task': 'visuotopy'})
                        semagacq.append(float(s.acquisition_time))
            elif ('fid' in (s.sequence_name).strip()):
                if (s.dim4==102):
                    if (('M' == (s.image_type[2].strip())) or (('FMRI' in (s.image_type[2].strip())) and ('mbep2d'!=s.series_description[0:6]))): #If realtime was on phase will start with mb and mag with act
                        info[task_ge].append({'item': s.series_id, 'acqtime': s.acquisition_time, 'task': 'checkerboard'})
                        magacq.append(float(s.acquisition_time))
                    elif (('P' == (s.image_type[2].strip())) or (('FMRI' in (s.image_type[2].strip())) and ('mbep2d'==s.series_description[0:6]))): #If realtime was on phase will start with mb and mag with act
                        info[task_ge_phase].append({'item': s.series_id, 'acqtime': s.acquisition_time,  'task': 'checkerboard'})
                        phaseacq.append(float(s.acquisition_time))
                elif (s.dim4==64):
                    if (('M' == (s.image_type[2].strip())) or (('FMRI' in (s.image_type[2].strip())) and ('mbep2d'!=s.series_description[0:6]))):
                        info[task_ge].append({'item': s.series_id, 'acqtime': s.acquisition_time, 'task': 'visuotopy'})
                        magacq.append(float(s.acquisition_time))
                    elif (('P' == (s.image_type[2].strip())) or (('FMRI' in (s.image_type[2].strip())) and ('mbep2d'==s.series_description[0:6]))):
                        info[task_ge_phase].append({'item': s.series_id, 'acqtime': s.acquisition_time, 'task': 'visuotopy'})
                        phaseacq.append(float(s.acquisition_time))

    # Now we have all the sequences in the right bins we need to link up the magnitudes and phases from the GE to ensure the runs match
    # find the unique magnitude runs and sort by start times
    magtimes = list(sorted(set(magacq)))
    semagtimes = list(sorted(set(magacq)))

    # find the pairs of indicies corresponding to the same run
    magind =[None]*len(magtimes)
    phaseind =[None]*len(magtimes)
    for i in xrange(len(magtimes)):
        #find last phase file with that acq time (vunerable: assumes last phase recon is correct recon)
        magind[i]=magacq.index(magtimes[i])
        try:
            phaseind[i]=len(phaseacq)-1-(phaseacq[::-1]).index(magtimes[i])
        except:
            phaseind[i]=-1 # no phase run found do not append it
    # put the results sorted back into info
    maginfo = info[task_ge]
    phaseinfo = info[task_ge_phase]
    seinfo = info[task_se]
    info[task_se]=[]
    info[task_ge]=[]
    info[task_ge_phase]=[]

    for i in xrange(len(semagtimes)):
        info[task_se].append(seinfo[i])
        info[task_se][i]['run']=str(i+1).zfill(2)

    for i in xrange(len(magind)):
        info[task_ge].append(maginfo[magind[i]])
        info[task_ge][i]['run']=str(i+1).zfill(2)
        if phaseind[i]>-1: # if no run found phase is not appended
            phaseinfo[phaseind[i]]['run']=str(i+1).zfill(2)
            info[task_ge_phase].append(phaseinfo[phaseind[i]])

    return info
