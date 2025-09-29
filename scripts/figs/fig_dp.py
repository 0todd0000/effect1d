
'''
Calculate effect size and its simple and functional interpretations
'''

import os
import numpy as np
import matplotlib.pyplot as plt
import effect1d as e1d
d2p = e1d.stats.d2p_onesample_0d



# calculate effect-size p-values for one-sample case:
interps  = [['Very small',0.01], ['Small',0.2], ['Medium',0.5], ['Large',0.8], ['Very large',1.2], ['Huge',2.0]]
labels,d = zip(*interps)
n        = np.arange(2,80)
p        = np.array([[d2p(dd, nn) for dd in d]  for nn in n]) 





# plot:
plt.close('all')
plt.figure(figsize=(6,4))
ax = plt.axes()

colors = plt.cm.gray( np.linspace(0,1,9)  )[:6]
# loc    = [(25,-0.5,0), (25,-1.7,-3), (25,-4.7,-8), (25,-8.5,-19), (25,-14.5,-32)]
loc    = [(25,-0.4,0), (25,-1.8,-5), (25,-5.3,-22), (25,-9.1,-40), (23,-14.5,-58), (14.5,-14.5,-67)]
for pp,cc,ss,lc in zip(p.T,colors,labels,loc): 
    ax.plot( n, np.log(pp), color=cc, lw=2, zorder=1 )
    x,y,a = lc
    ax.text(x, y, ss, rotation=a, color=cc)
vlines = [3, 4, 7, 13, 70]
dx     = [-0.5, 0, 0, 0, 0]
dy     = [0, 0, 0, 2, 0]
for vl,ddx,ddy in zip(vlines, dx, dy):
    ha = 'right' if vl==3 else 'left'
    ax.plot([vl,vl], [-15,np.log(0.05)], color='r', ls=':', zorder=0)
    ax.text(vl+ddx, -11+ddy, fr'$n$ = {vl}', rotation=-90, ha=ha, va='top', color='r')


ax.axhline( np.log(0.05), color='r', ls='--', label=r'$\alpha$=0.05', zorder=0)
ax.legend( bbox_to_anchor=(0.5,0.78) )
ax.set_ylim(-15,0.5)
ax.set_xlabel(f'Sample size ($n$)', size=12)
ax.set_ylabel('log( p-value )', size=12)
plt.tight_layout()
fpath = os.path.join( os.path.dirname(__file__), 'pdf', 'fig_oa.pdf' )
plt.savefig(fpath)
plt.show()







