

import os
from collections.abc import Iterable
from math import atan2,degrees,floor
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
import matplotlib as mpl
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
        

    
    def calc_contour(self, X, Y, Z, a):
        # calculate contours in pixel units:
        from skimage import measure
        cs    = measure.find_contours(Z, a)
        if len(cs) == 0:
            return None,None
        else:
            y0,x0 = cs[0].T
            # transform to X and Y units
            xlim  = X.min(), X.max()
            ylim  = Y.min(), Y.max()
            dx    = xlim[1] - xlim[0]
            dy    = ylim[1] - ylim[0]
            nx    = X.shape[1] - 1
            ny    = X.shape[0] - 1
            x     = ((x0 / nx) * dx) + xlim[0]
            y     = ((y0 / ny) * dy) + ylim[0]
            r0    = np.vstack( [x0,y0] ).T
            r     = np.vstack( [x,y] ).T
            return r0, r

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
        # plot contour lines:
        for pp in p0r[1:-1]:
            _,r  = self.calc_contour(D, W, P, pp)
            if r is not None:
                self.ax.plot( *r.T, '0.7' )
        # plot contour labels:
        p0rtx  = np.array([ sum(p0r[i:i+2])/2  for i in range(p0r.size-1) ])
        labels = ['Negligible'] + list(self.labels)
        label_colors = ['0.8'] + ['0.6'] + ['k']*5
        for pp,ll,cc in zip(p0rtx[::-1], labels, label_colors):
            r0,r = self.calc_contour(D, W, P, pp)
            if r is not None:
                # self.ax.plot( *r.T, 'k:' )
                i    = int(floor( r.shape[0] / 2 ))
                # self.ax.plot( *r[i], 'ro' )
                x0,y0 = r0[i]
                x1,y1 = r0[i-1]
                phi =  atan2(y1-y0, x1-x0)
                self.ax.text(*r[i], ll, color=cc, ha='center', va='center', rotation=degrees(phi))
        cb = plt.colorbar( sm, ax=self.ax )
        cb.set_label( 'Probability' )
        self.ax.set_xlabel("Cohen's d")
        self.ax.set_ylabel('FWHM')
        # plt.tight_layout()



# params = Effect1DPlotParameters(n=5, d=1.0, w=20, dlim=(0.2,5), wlim=(3,50))
#
# plt.figure()
# ax = plt.axes()
# plotter = Effect1DPlotter( ax )
# plotter.update( params )
# # ax.imshow(P)
# plt.show()
