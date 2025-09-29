
from math import sqrt
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt



interpretations = [['Very small',0.01], ['Small',0.2], ['Medium',0.5], ['Large',0.8], ['Very large',1.2], ['Huge',2.0]]



def p_effect(d, n):
	v      = n -2
	t      = d * sqrt(n)
	return stats.t.sf(t, v)
	



#(0) Calculate probabilities for effect sizes:
labels,d = zip(*interpretations)
n        = [10, 30, 100]
p0       = np.array([[p_effect(dd, nn) for dd in d]  for nn in n])

print( np.around(p0,3).T )