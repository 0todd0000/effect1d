
import ipywidgets as widgets
from IPython.display import display, clear_output
import matplotlib.pyplot as plt


class DropdownDesign( widgets.Dropdown ):
    def __init__(self):
        super().__init__(
            options=['One-sample', 'Paired', 'Two-sample'],
            value='Two-sample',
            description='Design:',
            disabled=False,
            )
            


class MPLWidget( widgets.Stack ):
    def __init__(self):
        import numpy as np
        self.out = widgets.Output()
        with self.out:
            self.fig = plt.figure()
            self.ax = self.fig.add_axes([0,0,1,1])
            self.ax.plot( np.random.randn(10) )
            plt.show( self.fig )
        super().__init__(  [self.out], selected_index=0  )
        
    
    def update(self):
        import numpy as np
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