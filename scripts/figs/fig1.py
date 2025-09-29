
import os
from math import sqrt
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
import rft1d

plt.style.use('bmh')
plt.rcParams['lines.linewidth'] = 2
plt.rcParams['xtick.labelsize'] = 'small'
plt.rcParams['ytick.labelsize'] = 'small'
plt.rcParams['font.sans-serif'] = 'Arial'


interpretations = [['Very small',0.01], ['Small',0.2], ['Medium',0.5], ['Large',0.8], ['Very large',1.2], ['Huge',2.0]]



def p_effect(d, n):
	v      = n -2
	t      = d * sqrt(n)
	return stats.t.sf(t, v)
	

def p_effect_mv(d, n, ndv=1):
	v      = n -2
	t      = d * sqrt(n)
	pu     = stats.t.sf(t, v)     # uncorrected p value
	p      = 1 - ( 1 - pu )**ndv  # corrected p value (Bonferroni)
	p      = max(0, min(1, p))    # constrain to the range [0,1]
	return p

#(0) Calculate probabilities for effect sizes:
labels,d = zip(*interpretations)
n        = [10, 30, 100]
p0       = np.array([[p_effect(dd, nn) for dd in d]  for nn in n])
# multivariate:
n1,ndv   = 10, [1, 3, 10]
p1       = np.array([[p_effect_mv(dd, n1, mm) for dd in d]  for mm in ndv])


#(1) Plot:
plt.close('all')
fig,(ax0,ax1) = plt.subplots(1, 2, figsize=(12,4))
# plt.get_current_fig_manager().window.move(0, 0)

ax = ax0
ax.plot(d, p0.T, 'o-')
ox,oy = -0.01, 0.03
for xx,pp,ss in zip(d,p0[0],labels):
	ax.text( xx+ox , pp+oy, ss, size=11 )
ax.legend([f'$N = {nn}$'  for nn in n], fontsize=12)
ax.set_xlabel("Cohen's d", size=14)
ax.set_ylabel('Probability', size=14)

ax = ax1
ax.plot(d, p1.T, 'o-')
ox,oy = 0.01, 0.01
for xx,pp,ss in zip(d,p1[-1],labels):
	ax.text( xx+ox , pp+oy, ss, size=11 )
ax.legend([f'$M = {mm}$'  for mm in ndv], fontsize=12)
ax.set_xlabel("Cohen's d", size=14)
# ax.set_ylabel('Probability')

panel_labels = ['(a)  Sample size ( $N$ ) dependence;   $M=1$', '(b) Dependent variable count ( $M$ ) dependence;   $N=10$']
[ax.text(0.0, 1.08, s, size=14, transform=ax.transAxes)   for ax,s in zip([ax0,ax1], panel_labels)]

plt.setp([ax0,ax1], ylim=(-0.03, 1.03))


plt.tight_layout()
plt.show()


# plt.savefig(  os.path.join(  os.path.dirname(__file__) , 'pdf', 'fig1.pdf'  )  )