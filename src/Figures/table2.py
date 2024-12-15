
import os
import numpy as np
from scipy import stats
# from spm1d import rft1d
import rft1d





def cohens_d(yA, yB):
	mA,mB  = yA.mean(axis=0), yB.mean(axis=0)
	sA,sB  = yA.std(axis=0, ddof=1), yB.std(axis=0, ddof=1)
	nA,nB  = yA.shape[0], yB.shape[0]
	s      = (   (  (nA-1)*sA*sA + (nB-1)*sB*sB  )  /  ( nA+nB-2 )   )**0.5
	d      = (mA - mB) / s
	return d

def d2t(d, n):
	return d / (1/n + 1/n)**0.5

def t2d(t, n):
	return t * (1/n + 1/n)**0.5


table = [['Very small',0.01], ['Small',0.2], ['Medium',0.5], ['Large',0.8], ['Very large',1.2], ['Huge',2.0]]
labels,d0 = zip( *table )




# calculate probabilities for given thresholds:
n     = 10
v     = 2*n-2
t0    = [d2t(dd, n)  for dd in d0]
p0    = [stats.t.sf(tt, v)  for tt in t0]


# calculate t-values and d-values for same probabilities in 1D case:
Q     = 101
fwhm  = 21.9
tc1   = [rft1d.t.isf(pp, v, Q, fwhm)  for pp in p0]
d1    = [t2d(tt, n)  for tt in tc1]




print("Label       Cohen's d    p-value   Functional d")
print("-----------------------------------------------")
for ss,dd0,pp,dd1 in zip(labels,d0,p0,d1):
    print( f'{ss:10}  {dd0:9}      {pp:.3f}      {dd1:.2f}' )

