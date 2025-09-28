
'''
Check correspondence between imported (parsed) data and
the provided metadata
'''

import os,pathlib
import numpy as np
import h5py
import pandas as pd



def unique_sorted(x):
    return np.sort( np.unique(x) )




# read metadata:
dirREPO        = pathlib.Path( __file__ ).parent.parent.parent.parent
dir0           = os.path.join(dirREPO, 'data', 'Bertaux2022')
fpathCSV       = os.path.join(dir0, 'metadata.csv') 
df             = pd.read_csv( fpathCSV )
labels_groups  = ['HEA', 'HOA']
labels_m6      = {np.nan:0, 'No':0, 'Yes':1}
labels_afflimb = ['L', 'R', 'N']
group          = np.asarray([labels_groups.index(x)  for x in df['Cohorte']])
subj           = np.asarray(df['Id Inclusion'], dtype=int)
m6             = np.asarray([labels_m6[x]  for x in df['M6 Available (Yes/No)']])
affected_limb  = np.asarray([labels_afflimb.index(x)  for x in df['OASide']])
d0             = dict(group=group, subj=subj, m6=m6, affected_limb=affected_limb)


# load imported data:
fpathH5 = os.path.join(dir0, 'imported.h5')
d1      = dict()
with h5py.File(fpathH5, 'r') as f:
    for k in f.keys():
        d1[k]  = np.array(f[k])




# check that subject labels are the same:
usubj0  = unique_sorted(  d0['subj']  )
usubj1  = unique_sorted(  d1['subj']  )
print( 'Same subject labels: ', np.all(usubj0==usubj1) )


# check that subject labels are the same within each group:
usubj0  = unique_sorted(  d0['subj'][ d0['group']==0 ] )
usubj1  = unique_sorted(  d1['subj'][ d1['group']==0 ] )
print( 'Same subjects in healthy group: ', np.all(usubj0==usubj1) )

usubj0  = unique_sorted(  d0['subj'][ d0['group']==1 ] )
usubj1  = unique_sorted(  d1['subj'][ d1['group']==1 ] )
print( 'Same subjects in OA group: ', np.all(usubj0==usubj1) )


# check that M6 (6-month follow-up) data are available in same subjects
usubj0  = unique_sorted(  d0['subj'][ d0['m6']==1 ] )
usubj1  = unique_sorted(  d1['subj'][ d1['sess']==1 ] )
print( 'Same subjects with M6: ', np.all(usubj0==usubj1) )


# check affected limb:
usubj0  = unique_sorted( d0['subj'] )
aff0    = np.array([d0['affected_limb'][d0['subj']==u][0]  for u in usubj0])
usubj1  = unique_sorted( d1['subj'] )
aff1    = np.array([d1['affected_limb'][d1['subj']==u][0]  for u in usubj1])
print( 'Same affected limb in all subjects: ', np.all(aff0==aff1) )




