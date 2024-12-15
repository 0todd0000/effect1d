
import ipywidgets as widgets
from IPython.display import display, clear_output
import numpy as np
import matplotlib.pyplot as plt





class DropdownDesign( widgets.Dropdown ):
    def __init__(self):
        super().__init__(
            options=['One-sample', 'Paired', 'Two-sample'],
            value='Two-sample',
            description='Design:',
            disabled=False,
            )

class FigureWithSlidersWidget( widgets.HBox ):
    def __init__(self):
        self.fig_widget = FigureWidget()
        self.slider_d   = SliderDLimits()
        self.slider_w   = SliderWLimits()
        layout_slider_d = widgets.Layout(display='flex', flex_flow='column', align_items='center', width='100%')
        layout_slider_w = widgets.Layout(display='flex', flex_flow='column', align_items='center', width='100%')
        layout_v        = widgets.Layout(display='flex', flex_flow='column', align_items='center', width='100%')
        hbox_slider_d   = widgets.HBox(children=[self.slider_d], layout=layout_slider_d)
        vbox            = widgets.VBox(children=[self.fig_widget, hbox_slider_d], layout=layout_v)
        
        
        layout = widgets.Layout(display='flex', flex_flow='row', align_items='center', width='100%')
        super().__init__(children=[self.slider_w, vbox],layout=layout)
        
        


class FigureWidget( widgets.Stack ):
    def __init__(self):
        self.out = widgets.Output()
        with self.out:
            self.fig = plt.figure()
            self.ax = self.fig.add_axes([0,0,1,1])
            self.ax.plot( np.random.randn(10) )
            plt.show( self.fig )
        super().__init__(  [self.out], selected_index=0  )
        
    
    def update(self):
        with self.out:
            clear_output(wait=True)
            self.ax.cla()
            self.ax.plot( np.random.randn(5), "r" )
            display(self.fig)


class SliderDLimits( widgets.FloatRangeSlider ):
    def __init__(self):
        super().__init__(
            value=[0.1, 4],
            min=0,
            max=10.0,
            step=0.1,
            description='d limits:',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='.1f',
            layout = widgets.Layout(width='500px'),
            )


class SliderWLimits( widgets.FloatRangeSlider ):
    def __init__(self):
        super().__init__(
            value=[5, 50],
            min=3,
            max=80.0,
            step=1,
            description='FWHM limits:',
            disabled=False,
            continuous_update=False,
            orientation='vertical',
            readout=True,
            readout_format='.1f',
            layout = widgets.Layout(width='100px'),
            )



class HBoxDesign( widgets.HBox ):
    def __init__(self):
        layout = widgets.Layout(display='flex', flex_flow='column', align_items='center', width='100%')
        w = DropdownDesign()
        super().__init__(children=[w],layout=layout)



class HBoxDLimits( widgets.HBox ):
    def __init__(self):
        layout = widgets.Layout(display='flex', flex_flow='column', align_items='center', width='100%')
        w = SliderDLimits()
        super().__init__(children=[w],layout=layout)




class VBoxControls( widgets.VBox ):
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




class VBoxResults( widgets.VBox ):
    def __init__(self):
        w      = widgets.HTML(value="<h3>Results</h3>", placeholder='', description='')
        layout = widgets.Layout(display='flex', flex_flow='column', align_items='center')
        w0     = widgets.HBox(children=[w],layout=layout)
        
        
        

        w1 = widgets.FloatText(
            value=0.0,
            description='p-value:',
            disabled=True,
            layout = widgets.Layout(width='200px'),
        )

        w2 = widgets.Text(
            value='Large',
            placeholder='',
            description='Size',
            disabled=True,
            layout = widgets.Layout(width='200px'),
        )

        super().__init__( [w0, w1, w2] )
        self.widget_pvalue = w1


    def update(self):
        out = widgets.Output()
        self.widget_pvalue.value = 0.555
        
        # display(out)
        # with out:
        #     print('okok')





# tab = widgets.Tab(children = [out])
# tab.set_title(0, 'First')
# # tab.set_title(1, 'Second')
# display(tab)

# display( out )

# display(widgets.HBox([out, vbox1]))


