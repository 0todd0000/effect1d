
import ipywidgets as widgets
from . basic import *
from . prob import Effect1DInterpretationCalculator



class _Params(object):
    def __init__(self):
        self.n  = 8
        self.d  = 0.5
        self.w  = 25

class ControlsWidget( widgets.VBox ):
    def __init__(self, mgr):
        self.mgr = mgr
        w0       = Header('Parameters')
        w1       = SpinGroupSize( mgr )
        w2       = SpinFWHM( mgr )
        w3       = SpinCohensD( mgr )
        super().__init__( [w0, w1, w2, w3] )

class ResultsWidget( widgets.VBox ):
    def __init__(self, mgr):
        self.mgr           = mgr
        self.calc          = Effect1DInterpretationCalculator()
        self.params        = _Params()
        w0                 = Header('Results')
        w1                 = ResultsTextBox('p-value')
        w2                 = ResultsTextBox('Interp.')
        super().__init__( [w0, w1, w2] )
        self.pvalue_widget = w1
        self.interp_widget = w2
        self.mgr.set_results_widget( self )
        self._update()
        

    def set_interpretation(self, s):
        self.interp_widget.value = s
    
    def set_pvalue(self, x):
        self.pvalue_widget.value = f'{x:.05f}'
        
    def _update(self):
        res = self.calc.update_params( self.params )
        self.set_pvalue( res['p'] )
        self.set_interpretation( res['label'] )
    
    def update_d(self, x):
        self.params.d = x
        self._update()
        
    def update_fwhm(self, x):
        self.params.w = x
        self._update()

    def update_n(self, x):
        self.params.n = x
        self._update()
        