
'''
Calculate effect size and its simple and functional interpretations
'''

import numpy as np
import matplotlib.pyplot as plt
import spm1d
import effect1d as e1d
d2p = e1d.stats.d2p_onesample_0d




interps  = [['Very small',0.01], ['Small',0.2], ['Medium',0.5], ['Large',0.8], ['Very large',1.2], ['Huge',2.0]]
labels,d = zip(*interps)
n        = np.arange(2,30)
p        = np.array([[d2p(dd, nn) for dd in d]  for nn in n]) 





# plot:
plt.close('all')
plt.figure(figsize=(6,4))
ax = plt.axes()

colors = plt.cm.copper( np.linspace(0,1,len(labels))  )

for pp,cc,ss in zip(p.T,colors,labels): 
    ax.plot( n, np.log(pp), color=cc, label=ss )
ax.axhline( np.log(0.05), color='r', ls='--', label='alpha=0.05')
ax.legend()



# colors = '0', 'r', 'b'
# ax.plot( y1.T, color=colors[1], lw=0.2 )
# ax.plot( y2.T, color=colors[2], lw=0.2 )
# ax.plot( y0.mean(axis=0), color=colors[0], lw=5, label='Healthy' )
# ax.plot( y1.mean(axis=0), color=colors[1], lw=5, label='OA, Month 0' )
# ax.plot( y2.mean(axis=0), color=colors[2], lw=5, label='OA, Month 6' )
# ax.legend()
ax.set_xlabel('Sample size', size=12)
ax.set_ylabel('log(p-value)', size=12)
plt.tight_layout()
# fpath = os.path.join( os.path.dirname(__file__), 'pdf', 'fig_oa.pdf' )
# plt.savefig(fpath)
plt.show()







