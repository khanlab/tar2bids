import sys
import pprint
import json
import pydicom
import jcamp
#from pybruker import jcamp
import numpy as np


#take in <path_to_dicom> as input
#write out <path_to_dicom>.{bvec,bval,bmat} as output

# Strip off '.dcm'
fname = sys.argv[1]
fname_noExt = fname[0:-4]

# read dicom header
H = pydicom.read_file(fname, stop_before_pixels=True)

#read bruker headers
method=jcamp.jcamp_parse(
          H[0x0177,0x1100].value.decode('utf-8').splitlines()
          )
visu_pars=jcamp.jcamp_parse(
          H[0x0177,0x1101].value.decode('utf-8').splitlines()
          )

#with open(fname_noExt+'_method.json', 'w') as fp:
#    json.dump(method,  fp, indent=4)

#with open(fname_noExt+'_visu_pars.json', 'w') as fp:
#    json.dump(visu_pars,  fp, indent=4)

# Bvalue information for Budde sequence
#if visu_pars["$VisuAcqSequenceName"]["value"].find('rFOV_DWEpiWave') > -1:

bval = method["$PVM_DwEffBval"]["value"]
bvec = method["$PVM_DwDir"]["value"]
bvec = np.reshape(bvec, (int(len(bvec)/3), 3)).T
bmat = method["$PVM_DwBMat"]["value"]
bmat = np.reshape(bmat, (int(len(bmat)/9), 9)).T

with open(fname_noExt+'.bval', 'w') as fp:
    for item in bval:
        fp.write("%f " % item)
    fp.write("\n")

with open(fname_noExt+'.bvec', 'w') as fp:
    for row in bvec:
        for item in row:
            fp.write("%f " % item)
        fp.write("\n")

with open(fname_noExt+'.bmat', 'w') as fp:
    for row in bmat:
        for item in row:
            fp.write("%s " % item)
        fp.write("\n")


