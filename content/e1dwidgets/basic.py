
import ipywidgets as widgets
from IPython.display import display, clear_output
from traitlets import validate
import matplotlib.pyplot as plt





class DropdownDesign( widgets.Dropdown ):
    def __init__(self, mgr):
        self.labels = ['One-sample', 'Paired', 'Two-sample']
        super().__init__(options=self.labels, value='Two-sample', description='Design', disabled=False)
        self.observe(self.on_value_changed, names='value')
        self.mgr = mgr
    
    def on_value_changed(self, change):
        ind = self.labels.index( change['new'] )
        self.mgr.on_design_changed( ind )
    

class Header( widgets.HBox ):
    def __init__(self, label):
        w        = widgets.HTML(value=f'<h3>{label}</h3>', placeholder='', description='')
        layout   = widgets.Layout(display='flex', flex_flow='column', align_items='center')
        super().__init__(children=[w], layout=layout)


class MPLWidget( widgets.Stack ):
    def __init__(self):
        
        self.basic = False
        
        
        
        self.out = widgets.Output()
        with self.out:
            self.fig = plt.figure()
            self.ax = self.fig.add_axes([0,0,1,1])
            
            if self.basic:
                import numpy as np
                self.ax.plot( np.random.randn(10) )
            else:
                from . plt import Effect1DPlotParameters, Effect1DPlotter
                params       = Effect1DPlotParameters(n=5, d=1.0, w=20, dlim=(0.2,5), wlim=(3,50))
                self.plotter = Effect1DPlotter( self.ax )
                self.plotter.update( params )
            
            plt.show( self.fig )
        super().__init__(  [self.out], selected_index=0  )
        
    
    def update(self, params, mgr):
        
        with self.out:
            clear_output(wait=True)
            self.ax.cla()
            if self.basic:
                import numpy as np
                self.ax.plot( np.random.randn(5), "r" )
            else:
                self.plotter = Effect1DPlotter( self.ax )
                self.plotter.update( params )
            display(self.fig)


class Output( widgets.Output ):
    def __init__(self, mgr):
        super().__init__()
        self.mgr = mgr
        self.mgr.set_output_widget( self )



class _EnforceSliderGap(object):
    @validate('value')
    def enforce_gap(self, proposal):
        gap    = self.step
        x0, x1 = proposal.value
        oldx0, oldx1 = self.value
        if (x1-x0) < gap:
            if oldx0 == x0:
                x1 = x0 + gap
            else:
                x0 = x1 - gap
        return (x0, x1)

class SliderDLimits( widgets.FloatRangeSlider, _EnforceSliderGap ):
    def __init__(self, mgr):
        self.step = 0.1
        super().__init__(value=[0.1, 4], min=0, max=10, step=self.step, description='d limits:', disabled=False, continuous_update=False, orientation='horizontal', readout=True, readout_format='.1f', layout=widgets.Layout(width='500px') )
        self.observe(self.on_value_changed, names='value')
        self.mgr = mgr
    
    def on_value_changed(self, change):
        self.mgr.on_dlimits_changed( change['new'] )
        


class SliderWLimits( widgets.IntRangeSlider, _EnforceSliderGap ):
    def __init__(self, mgr):
        self.step = 1
        super().__init__(value=[5, 50], min=3, max=80, step=self.step, description='FWHM limits:', disabled=False, continuous_update=False, orientation='vertical', readout=True, readout_format='d', layout=widgets.Layout(width='100px', height='400px'))
        self.observe(self.on_value_changed, names='value')
        self.mgr = mgr
    
    def on_value_changed(self, change):
        self.mgr.on_wlimits_changed( change['new'] )



class SpinGroupSize( widgets.BoundedIntText ):
    def __init__(self, mgr):
        super().__init__(value=10, min=3, max=1000, step=1, description='Group size', disabled=False, layout=widgets.Layout(width='200px'),)
        self.observe(self.on_value_changed, names='value')
        self.mgr = mgr
        
    def on_value_changed(self, change):
        self.mgr.on_groupsize_changed( change['new'] )



class SpinFWHM( widgets.BoundedFloatText ):
    def __init__(self, mgr):
        super().__init__(value=10, min=3, max=80, step=0.1, description='FWHM', disabled=False, layout=widgets.Layout(width='200px'),)
        self.observe(self.on_value_changed, names='value')
        self.mgr = mgr
        
    def on_value_changed(self, change):
        self.mgr.on_fwhm_changed( change['new'] )
        


class SpinCohensD( widgets.BoundedFloatText ):
    def __init__(self, mgr):
        super().__init__(value=0.5, min=0.1, max=5, step=0.1, description="Cohen's d", disabled=False, layout=widgets.Layout(width='200px'),)
        self.observe(self.on_value_changed, names='value')
        self.mgr = mgr
        
    def on_value_changed(self, change):
        self.mgr.on_d_changed( change['new'] )


class ResultsTextBox( widgets.Text ):
    def __init__(self, label):
        super().__init__(value='(None)', placeholder='', description=label, disabled=True, layout = widgets.Layout(width='200px'))
        

