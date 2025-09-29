
'''
Calculate within-subject means for between-subject analysis
'''

import os
import numpy as np
import h5py



def unique_sorted(x):
    return np.sort( np.unique(x) )




# load imported data:
dir0    = os.path.join( os.path.dirname(__file__), 'data' )
fpathH5 = os.path.join(dir0, 'imported.h5')
d       = dict()
with h5py.File(fpathH5, 'r') as f:
    for k in f.keys():
        d[k] = np.array(f[k])



# calculate means:
usubj   = unique_sorted( d['subj'] )
m       = []
subj    = []
group   = []
aff     = []
sess    = []
limb    = []
for sb in usubj:
    for ss in [0,1]:
        for ll in [0,1]:
            b  = (d['subj']==sb) & (d['sess']==ss) & (d['limb']==ll)
            y  = d['y'][b]
            if y.shape[0] > 1:
                m.append( y.mean(axis=0) )
                subj.append( sb )
                sess.append( ss )
                limb.append( ll )
                group.append( d['group'][b][0] )
                aff.append( d['affected_limb'][b][0] )
m      = np.vstack(m)
subj,sess,limb,group,aff = [np.asarray(x)  for x in (subj,sess,limb,group,aff)]



# save means:
d      = dict(y=m, subj=subj, sess=sess, limb=limb, group=group, affected_limb=aff)
fpath1 = os.path.join(dir0, 'means.h5')
with h5py.File(fpath1, 'w') as f:
    for key in d.keys():
        f.create_dataset( key, data=d[key], compression='gzip', compression_opts=9 )



