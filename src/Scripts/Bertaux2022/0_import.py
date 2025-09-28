

import os,pathlib
import numpy as np
import matplotlib.pyplot as plt
import h5py



def parse_filename(fpath):
    sessions = ['M0', 'M6']
    limbs    = ['L', 'R']
    x        = os.path.split( fpath )[1].split('_')
    sess     = sessions.index( x[1] )
    limb     = limbs.index( x[2][0] )
    return sess,limb

def parse_subj(x):
    groups = ['HEA', 'HOA']
    group  = np.asarray([groups.index(s[:3]) for s in x], dtype=int)
    subj   = np.asarray([s[3:] for s in x], dtype=int)
    return group,subj
    # for s in x:

def parse_affected_limb(x):
    limbs    = ['L', 'R', 'N']
    afflimb  = np.asarray([limbs.index(xx) for xx in x], dtype=int)
    return afflimb

def parse_trial(x):
    trial    = np.asarray([xx[-2:] for xx in x], dtype=int)
    return trial

def parse_cycle(x):
    cycle    = np.asarray([xx.split('_')[-1] for xx in x], dtype=int)
    return cycle
    

def read_arff(fpath):
    with open(fpath, 'r') as f:
        lines = f.readlines()
    for i,line in enumerate(lines):
        if line.startswith('@DATA'):
            i += 1
            break
    sess,limb     = parse_filename( fpath )
    a             = np.array([line.strip().split(',')  for line in lines[i:]])
    if sess==1:  # M6 --- remove last row which containts "?"
         a        = a[:-1]
    y             = np.asarray(a[:,:-4], dtype=float)  # dependent variable
    b             = np.isnan(y).any(axis=1)
    y,a           = y[~b], a[~b]
    group,subj    = parse_subj( a[:,101] )
    affected_limb = parse_affected_limb( a[:,102] ) 
    trial         = parse_trial( a[:,103] )
    cycle         = parse_cycle( a[:,104] )
    sess          = sess * np.asarray([1]*y.shape[0])
    limb          = limb * np.asarray([1]*y.shape[0])
    d             = dict(y=y, group=group, subj=subj, sess=sess, limb=limb, affected_limb=affected_limb, trial=trial, cycle=cycle)
    return d

    
def stack_dictionaries( *args ):
    d = dict()
    for key in args[0].keys():
        x      = [d[key]  for d in args]
        x      = np.vstack(x) if key=='y' else np.hstack(x)
        d[key] = x
    return d
        


# read data files:
dirREPO = pathlib.Path( __file__ ).parent.parent.parent.parent
dir0    = os.path.join(dirREPO, 'data', 'Bertaux2022')
fname0  = 'HEA_M0_LHipAngles_X.arff'
fname1  = 'HEA_M0_RHipAngles_X.arff'
fname2  = 'HOA_M0_LHipAngles_X.arff'
fname3  = 'HOA_M0_RHipAngles_X.arff'
fname4  = 'HOA_M6_LHipAngles_X.arff'
fname5  = 'HOA_M6_RHipAngles_X.arff'
fnames  = [fname0, fname1, fname2, fname3, fname4, fname5]
dicts   = [read_arff( os.path.join(dir0, s) )   for s in fnames]
d       = stack_dictionaries( *dicts )



# save imported data:
fpathH5 = os.path.join(dir0, 'imported.h5')
with h5py.File(fpathH5, 'w') as f:
    for key in d.keys():
        f.create_dataset( key, data=d[key], compression='gzip', compression_opts=9 )


# check that data have been saved correctly:
with h5py.File(fpathH5, 'r') as f:
    y1 = np.array(f['y'])
print( np.all( d['y']==y1 ) )






