
'''
Calculate effect size and its simple and functional interpretations
'''

import os,pathlib
import numpy as np
import matplotlib.pyplot as plt
import h5py
import spm1d



def unique_sorted(x):
    return np.sort( np.unique(x) )


def d2t_onesample(d, n):
    return d / (1/n)**0.5

def d2p_onesample_0d(d, n):
    '''
    Calculate probabilty associated with Cohen's d value for the
    one-sample (or paired) case with a sample sizes of n
    '''
    from collections.abc import Iterable
    from scipy import stats
    if isinstance(d, Iterable):
        return np.array( [d2p_onesample_0d(dd, n)  for dd in d] )
    t = d2t_onesample(d, n)
    v = n - 1
    p = stats.t.sf(t, v)
    return p
    

def d2p_onesample_1d(d, n, Q, fwhm):
    import rft1d
    v  = n - 1
    u  = d2t_onesample(d, n)
    p  = rft1d.t.sf(u, v, Q, fwhm)
    return p

def p2d_onesample_1d(p, n, Q, fwhm):
    import rft1d
    v  = n - 1
    t  = rft1d.t.isf(p, v, Q, fwhm)
    d  = t2d_onesample(t, n)
    return d

def t2d_onesample(t, n):
    return t * (1/n)**0.5



# load imported data:
dirREPO = pathlib.Path( __file__ ).parent.parent.parent.parent
dir0    = os.path.join(dirREPO, 'data', 'Bertaux2022')
fpathH5 = os.path.join(dir0, 'means.h5')
d       = dict()
with h5py.File(fpathH5, 'r') as f:
    for k in f.keys():
        d[k] = np.array(f[k])



# separate data into groups (right limb only;  results are similar for left-limb only)
# group 0:  healthy (group=0)
# group 1:  OA, month 0 (group=1, sess=0)
# group 2:  OA, month 6 (group=1, sess=1)
limb   = 1
y0     = d['y'][  (d['group']==0) & (d['limb']==limb) ]
oasubj = unique_sorted( d['subj'][(d['affected_limb']==limb) & d['sess']==1] )
y1     = np.vstack([d['y'][  (d['subj']==u) & (d['limb']==limb) & (d['sess']==0) ]  for u in oasubj])
y2     = np.vstack([d['y'][  (d['subj']==u) & (d['limb']==limb) & (d['sess']==1) ]  for u in oasubj])


# conduct functional hypothesis test using SPM
spm    = spm1d.stats.ttest_paired( y2, y1 ).inference(0.05)
fwhm   = spm.fwhm


# calculate effect size and their probabilities:
y     = y2 - y1     # pairwise differences
n,Q   = y.shape     # sample size, domain size
d     = y.mean(axis=0) / y.std(ddof=1, axis=0)  # functional Cohen's d value
t     = d2t_onesample(d, n)  # functional t-value (also calculated above using spm1d.stats.ttest_paired;  this is just a check)
p0    = d2p_onesample_0d(-d, n)
p1    = d2p_onesample_1d(-d, n, Q, fwhm)


# calculate interpretations:
labels = ('Very small', 'Small', 'Medium', 'Large', 'Very large', 'Huge')
dth0   = (0.01, 0.2, 0.5, 0.8, 1.2, 2.0)  # d-value thresholds for 0D case
nn,ww  = 10, 25   # approximations from recommended guidelines;  see paper for a discussion
pth    = d2p_onesample_0d( dth0, nn )
dth1   = p2d_onesample_1d( pth, nn, Q, ww )

print( fwhm )
print( d.min() )
print( dth0 )
print( np.around(dth1,3) )



# plot:
plt.close('all')
fig,axs = plt.subplots( 2, 2, figsize=(8,6), tight_layout=True )
ax0,ax1,ax2,ax3 = axs.ravel()

ax0.plot( y1.T, color='r', lw=0.2 )
ax0.plot( y2.T, color='c', lw=0.2 )
ax0.plot( y0.mean(axis=0), color='k', lw=5, label='Healthy' )
ax0.plot( y1.mean(axis=0), color='r', lw=5, label='OA, Month 0' )
ax0.plot( y2.mean(axis=0), color='c', lw=5, label='OA, Month 6' )
ax0.legend()
ax0.set_xlabel('Time (%)')
ax0.set_ylabel('Hip flexion (deg)')



spm.plot( ax=ax1 )
ax1.plot( t, 'r')
ax1.set_xlabel('Time (%)', size=10)
ax1.set_ylabel('t-value', size=10)


ax2.plot( d )
for dd0,dd1,ss in zip(dth0,dth1,labels[:3]):
    ax2.axhline(-dd0, color='k', linestyle=':')
    ax2.axhline(-dd1, color='r', linestyle=':')
ax2.set_xlabel('Time (%)', size=10)
ax2.set_ylabel('Effect size (d-value)', size=10)



# ax3.plot( p0, label='Uncorrected' )
# ax3.plot( p1, label='RFT-corrected' )
ax3.plot( np.log(p0), label='Uncorrected' )
ax3.plot( np.log(p1), label='RFT-corrected' )
ax3.legend()
# ax3.set_ylim(0, 0.2)
ax3.set_xlabel('Time (%)', size=10)
ax3.set_ylabel('log-probability', size=10)


plt.show()







