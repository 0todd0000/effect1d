
import ipywidgets as widgets
from . basic import DropdownDesign, MPLWidget, SliderDLimits, SliderWLimits






class FigureWidget( widgets.HBox ):
    def __init__(self):
        self.fig_widget = MPLWidget()
        self.slider_d   = SliderDLimits()
        self.slider_w   = SliderWLimits()
        layout_slider_d = widgets.Layout(display='flex', flex_flow='column', align_items='center', width='100%')
        layout_slider_w = widgets.Layout(display='flex', flex_flow='column', align_items='center', width='100%')
        layout_v        = widgets.Layout(display='flex', flex_flow='column', align_items='center', width='100%')
        hbox_slider_d   = widgets.HBox(children=[self.slider_d], layout=layout_slider_d)
        vbox            = widgets.VBox(children=[self.fig_widget, hbox_slider_d], layout=layout_v)
        
        
        layout = widgets.Layout(display='flex', flex_flow='row', align_items='center', width='100%')
        super().__init__(children=[self.slider_w, vbox],layout=layout)





class DesignWidget( widgets.HBox ):
    def __init__(self):
        layout = widgets.Layout(display='flex', flex_flow='column', align_items='center', width='100%')
        w = DropdownDesign()
        super().__init__(children=[w],layout=layout)





class ControlsWidget( widgets.VBox ):
    def __init__(self, fig, results):
        
        w      = widgets.HTML(value="<h3>Parameters</h3>", placeholder='', description='')
        layout = widgets.Layout(display='flex', flex_flow='column', align_items='center')
        w0     = widgets.HBox(children=[w],layout=layout)
        
        
        w1 = widgets.BoundedIntText(
            value=10,
            min=3,
            max=50,
            step=1,
            description='Group size:',
            disabled=False,
            layout = widgets.Layout(width='200px'),
        )
        
        # def on_value_change(change):
        #     print(change['new'])
        # w0.observe(on_value_change, names='value')
        
        out = widgets.Output()
        def on_value_change(change):
            with out:
                self.fig.update()
                self.results.update()
                # print( self.fig )
        w1.observe(on_value_change, names='value')
        
        
        w2 = widgets.BoundedFloatText(
            value=7.5,
            min=3,
            max=50.0,
            step=0.1,
            description='FWHM:',
            disabled=False,
            layout = widgets.Layout(width='200px'),
        )

        w3 = widgets.BoundedFloatText(
            value=7.5,
            min=0.01,
            max=10.0,
            step=0.1,
            description="Cohen's d:",
            disabled=False,
            layout = widgets.Layout(width='200px'),
        )

        super().__init__( [w0, w1, w2, w3, out] )
        self.fig     = fig
        self.results = results




class ResultsWidget( widgets.VBox ):
    def __init__(self):
        w      = widgets.HTML(value="<h3>Results</h3>", placeholder='', description='')
        layout = widgets.Layout(display='flex', flex_flow='column', align_items='center')
        w0     = widgets.HBox(children=[w],layout=layout)
        w1 = widgets.Text(value='0.0', placeholder='', description='p-value', disabled=True, layout = widgets.Layout(width='200px'))
        w2 = widgets.Text(value='Large', placeholder='', description='Size', disabled=True, layout = widgets.Layout(width='200px'))

        super().__init__( [w0, w1, w2] )
        self.widget_pvalue = w1


    def update(self):
        out = widgets.Output()
        self.widget_pvalue.value = '0.555'
        




