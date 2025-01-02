
from collections.abc import Iterable
from math import floor
import rft1d


def d2t(d, n):
    return d / (1/n + 1/n)**0.5


def d2p0d(d, n):
    '''
    Calculate probabilty associated with Cohen's d value for the
    two-sample case with group sizes of n 
    '''
    if isinstance(d, Iterable):
        return [d2p0d(dd, n)  for dd in d]
    t = d2t(d, n)
    v = 2*n - 2
    p = rft1d.t.sf0d(t, v)
    return p


def p1d(d, n, w, Q=101):
    v  = 2*n - 2
    u  = d2t(d, n)
    p  = rft1d.t.sf(u, v, Q, w)
    return p



class _Params(object):
    def __init__(self):
        self.n  = 8
        self.d  = 1.0
        self.w  = 25


class Effect1DInterpretationCalculator(object):
    def __init__(self):
        self.labels  = ('Negligible', 'Very small', 'Small', 'Medium', 'Large', 'Very large', 'Huge')
        self.dc0     = (-100, 0.01, 0.2, 0.5, 0.8, 1.2, 2.0)  # critical d-values for 0D case
        self.nlabels = len(self.labels)
        self.dc1     = None  # critical d-values for 0D case
        self.p0      = None  # p-values associated with dc0
        self.n       = None  # group size

    def set_n(self, n):
        self.n   = n
        self.p0  = [d2p0d(d, n)  for d in self.dc0]

    def update(self, n, d, fwhm):
        self.set_n( n )
        p     = p1d(d, n, fwhm)        
        for i,(p0,label) in enumerate(zip(self.p0, self.labels)):
            if (p > p0):
                if i>1:
                    label = self.labels[i-1]
                break
        return dict(p=p, label=label)

    def update_params(self, params):
        return self.update( params.n, params.d, params.w )


if __name__ == "__main__":
    calc = Effect1DInterpretationCalculator()
    # n,d,w  = 8, 2.9, 25
    # res = calc.update(n, d, w)
    
    params = _Params()
    res = calc.update_params(params)
    
    print( calc.labels )
    print()
    print( calc.p0 )
    print()
    print( res )