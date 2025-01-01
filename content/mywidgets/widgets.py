
import ipywidgets as widgets
from . basic import *







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
        self.p             = None
        self.interp        = None
        w0                 = Header('Results')
        w1                 = ResultsTextBox('p-value')
        w2                 = ResultsTextBox('Interp.')
        super().__init__( [w0, w1, w2] )
        self.pvalue_widget = w1
        self.interp_widget = w2
        self.mgr.set_results_widget( self )

    def set_interpretation(self, s):
        self.interp_widget.value = s
    
    def set_pvalue(self, x):
        self.p = x
        self.pvalue_widget.value = str(x)