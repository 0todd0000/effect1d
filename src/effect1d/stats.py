

import numpy as np



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
