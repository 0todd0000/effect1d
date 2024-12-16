

import os
from collections.abc import Iterable
from math import atan2,degrees
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
import matplotlib as mpl
from shapely.geometry import Polygon
import rft1d



eps = np.finfo(np.float64).eps


plt.style.use('bmh')
plt.rcParams['lines.linewidth'] = 2
plt.rcParams['xtick.labelsize'] = 'small'
plt.rcParams['ytick.labelsize'] = 'small'
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family']     = 'Arial'





class Effect1DPlotParameters(object):
    def __init__(self, n=5, d=1.0, w=20, dlim=(0.2,5), wlim=(3,50)):
        self._ngrid = 21
        self.n      = n
        self.d      = d
        self.dlim   = dlim
        self.w      = w
        self.wlim   = wlim





class Effect1DPlotter(object):
    def __init__(self, ax):
        self.ax     = ax
        self.labels = ('Very small', 'Small', 'Medium', 'Large', 'Very large', 'Huge')
        self.d0     = (0.01, 0.2, 0.5, 0.8, 1.2, 2.0)  # d-values for 0D case
        

 
    def d2t(self, d, n):
        return d / (1/n + 1/n)**0.5

   
    def d2p0d(self, d, n):
        '''
        Calculate probabilty associated with Cohen's d value for the
        two-sample case with group sizes of n 
        '''
        if isinstance(d, Iterable):
            return np.array( [self.d2p0d(dd, n)  for dd in d] )
        t = self.d2t(d, n)
        v = 2*n - 2
        p = stats.t.sf(t, v)
        return p
    

    def p1d(self, d, n, w, Q=101):
        v  = 2*n - 2
        u  = self.d2t(d, n)
        p  = rft1d.t.sf(u, v, Q, w)
        return p
    

    
    
    def polygon_centroid_and_phi(self, verts, ds, ws):
        poly = Polygon( verts )
        # centoid:
        r    = poly.centroid
        x,y  = r.x, r.y
        # principal axis:
        cov = np.cov(verts.T )
        a,r = np.linalg.eig( cov )
        i   = a.argmax()
        r   = r[:,i]
        dr  = r / [ds.max()-ds.min(), ws.max()-ws.min()]
        phi =  atan2(dr[1], dr[0])
        return (x,y), phi
    
        
        
    def update(self, params):
        p0    = self.d2p0d(self.d0, params.n)    # 0D probabilities for d interpretation thresholds
        ds    = np.linspace(*params.dlim, params._ngrid)
        ws    = np.linspace(*params.wlim, params._ngrid)
        D,W   = np.meshgrid(ds, ws)
        P     = np.reshape([self.p1d(d, params.n, w)  for d,w in zip(D.ravel(), W.ravel())], D.shape)
        # using log transform:
        logP   = np.log(P)
        norm   = mpl.colors.LogNorm(vmin=0.0001, vmax=1)
        cmap   = plt.cm.BuPu
        colors = cmap( norm( logP ) )
        sm     = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        p0r    = np.array([eps] + list(p0[::-1]) + [1])
        cs     = self.ax.contourf(D, W, P, p0r, cmap=cmap, norm=norm)
        self.ax.contour(cs, p0r, colors='0.1', linewidths=0.5)
        # plot labels:
        labels = ['Negligible'] + list(self.labels)
        label_colors = ['0.7'] + ['k']*6
        for path,label,col in zip(cs.get_paths(), labels[::-1], label_colors[::-1]):
            (x,y),phi = self.polygon_centroid_and_phi( path.vertices, ds, ws )
            self.ax.text(x, y, label, color=col, ha='center', va='center', rotation=degrees(phi))
        cb = plt.colorbar( sm, ax=self.ax )
        cb.set_label( 'Probability' )
        self.ax.set_xlabel("Cohen's d")
        self.ax.set_ylabel('FWHM')
        # plt.tight_layout()
        # plt.show()
        
    



# params = Effect1DPlotParameters(n=5, d=1.0, w=20, dlim=(0.2,5), wlim=(3,50))
#
# plt.figure()
# ax = plt.axes()
# plotter = Effect1DPlotter( ax )
# plotter.update( params )
# # ax.imshow(P)
# plt.show()
