
import ipywidgets as widgets
from . basic import *






class FigureWidget( widgets.HBox ):
    def __init__(self, mgr):
        self.mgr        = mgr
        self.mpl_widget = MPLWidget()
        self.slider_d   = SliderDLimits( mgr )
        self.slider_w   = SliderWLimits( mgr )
        layout_slider_d = widgets.Layout(display='flex', flex_flow='column', align_items='center', width='100%')
        layout_slider_w = widgets.Layout(display='flex', flex_flow='column', align_items='center', width='100%')
        layout_v        = widgets.Layout(display='flex', flex_flow='column', align_items='center', width='100%')
        hbox_slider_d   = widgets.HBox(children=[self.slider_d], layout=layout_slider_d)
        vbox            = widgets.VBox(children=[self.mpl_widget, hbox_slider_d], layout=layout_v)
        layout          = widgets.Layout(display='flex', flex_flow='row', align_items='center', width='100%')
        super().__init__(children=[self.slider_w, vbox],layout=layout)
        self.mgr.set_figure_widget(self)
        
    def update(self, params):
        self.mgr._print('update')
        self.mpl_widget.update( params, self.mgr )
        





class DesignWidget( widgets.HBox ):
    def __init__(self, mgr):
        layout = widgets.Layout(display='flex', flex_flow='column', align_items='center', width='100%')
        w      = DropdownDesign( mgr )
        super().__init__(children=[w], layout=layout)





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



    
    # def update(self):
    #     out = widgets.Output()
    #     self.widget_pvalue.value = '0.555'
        




