
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
        
        
