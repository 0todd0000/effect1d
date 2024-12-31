
import ipywidgets as widgets
from IPython.display import display, clear_output
# from traitlets import validate
# import matplotlib.pyplot as plt




class AppHeader( widgets.HBox ):
    def __init__(self):
        s = '''
        <h1 style="text-align:center;">Effect Size Interpretation Calculator</h1>
        <h3 style="text-align:center;">One-dimensional functional data, two-sample case</h3>
        '''
        w        = widgets.HTML(value=s, placeholder='', description='')
        layout   = widgets.Layout(display='flex', flex_flow='column', align_items='center')
        super().__init__(children=[w], layout=layout)


class Header( widgets.HBox ):
    def __init__(self, label):
        w        = widgets.HTML(value=f'<h3>{label}</h3>', placeholder='', description='')
        layout   = widgets.Layout(display='flex', flex_flow='column', align_items='center')
        super().__init__(children=[w], layout=layout)



# class SpinGroupSize( widgets.BoundedIntText ):
#     def __init__(self, mgr):
#         super().__init__(value=8, min=3, max=40, step=1, description='Group size', disabled=False, layout=widgets.Layout(width='200px'),)
#         self.observe(self.on_value_changed, names='value')
#         self.mgr = mgr
#
#     def on_value_changed(self, change):
#         n = change['new']
#         with out:
#             clear_output()
#             print( "n = ", n)
#
#         fpath = f'img/contours_n={n}.png'
#         with open(fpath, 'rb') as f:
#             img = f.read()
#         w.value = img
#         # self.mgr.on_groupsize_changed( change['new'] )
#



#
# class MPLWidget( widgets.Image ):
#     def __init__(self):
#
#         self.basic = True
#         self.fig   = None
#         self.ax    = None
#
#
#         import base64
#         from io import BytesIO
#         import numpy as np
#
#         self.fig = plt.figure()
#         self.ax = self.fig.add_axes([0,0,1,1])
#         self.ax.plot( np.random.randn(10) )
#
#         b = BytesIO()
#         plt.savefig(b, format='png')
#         b.seek(0)
#         img = b.getvalue()
#         # b.close()
#         self.fig.set_visible(False)
#
#         super().__init__(value=img, format='png', border=None)
#
#         # self.fig.set_visible(False)
#
#
#
#         # # graphic = base64.b64encode(image_png)
#         # # graphic = graphic.decode('utf-8')
#         # # return graphic
#         #
#         #
#         # fpath = '/Users/todd/Dropbox/2019Sync/Documents/Professional/Jiku/Marketing/Logo/Blender/jiku-core-clean.png'
#         # with open(fpath, 'rb') as f:
#         #     img = f.read()
#         # super().__init__(value=img, format='png')
#
#
#
#         # fpath = open("images/WidgetArch.png", "rb")
#         # img = file.read()
#         # widgets.Image(
#         #     value=image,
#         #     format='png',
#         #     width=300,
#         #     height=400,
#         # )
#
#
#         # self.fig = plt.figure()
#         #
#         # self.box = widgets.Box( [self.fig] )
#         #
#         # plt.show( self.fig )
#
#         # with self.out:
#         #     self.fig = plt.figure()
#         #     self.ax = self.fig.add_axes([0,0,1,1])
#         #
#         #     if self.basic:
#         #         import numpy as np
#         #         self.ax.plot( np.random.randn(10) )
#         #     else:
#         #         from . plt import Effect1DPlotParameters, Effect1DPlotter
#         #         params       = Effect1DPlotParameters(n=5, d=1.0, w=20, dlim=(0.2,5), wlim=(3,50))
#         #         self.plotter = Effect1DPlotter( self.ax )
#         #         self.plotter.update( params )
#         #
#         #     plt.show( self.fig )
#         # super().__init__(  [self.out], selected_index=0  )
#
#
#     def update(self, params, mgr):
#         mgr._print('MPLWidget.update', params, mgr)
#
#
#
#
#
#
#         # self.ax.cla()
#         # self.ax.plot( np.random.randn(5), "r" )
#
#
#         with self:
#             self.fig.set_visible(True)
#             b = BytesIO()
#             plt.savefig(b, format='png')
#             b.seek(0)
#             img = b.getvalue()
#             b.close()
#
#
#             self.value = img
#
#             # display(self)
#
#
#
#         # if self.basic:
#         #     import numpy as np
#         #
#         # else:
#         #     self.plotter = Effect1DPlotter( self.ax )
#         #     self.plotter.update( params )
#         # self.fig.canvas.draw()
#         # display(self.fig)



class Output( widgets.Output ):
    def __init__(self, mgr):
        super().__init__()
        self.observe(self.on_value_changed, names='value')
        self.mgr = mgr
        self.mgr.set_output_widget( self )

    def on_value_changed(self, change):
        pass



class _EnforceSliderGap(object):
    pass
    # @validate('value')
    # def enforce_gap(self, proposal):
    #     gap    = self.step
    #     x0, x1 = proposal.value
    #     oldx0, oldx1 = self.value
    #     if (x1-x0) < gap:
    #         if oldx0 == x0:
    #             x1 = x0 + gap
    #         else:
    #             x0 = x1 - gap
    #     return (x0, x1)

# class SliderDLimits( widgets.FloatRangeSlider, _EnforceSliderGap ):
#     def __init__(self, mgr):
#         self.step = 0.1
#         super().__init__(value=[0.1, 4], min=0, max=10, step=self.step, description='d limits:', disabled=False, continuous_update=False, orientation='horizontal', readout=True, readout_format='.1f', layout=widgets.Layout(width='500px') )
#         self.observe(self.on_value_changed, names='value')
#         self.mgr = mgr
#
#     def on_value_changed(self, change):
#         self.mgr.on_dlimits_changed( change['new'] )
#
#
#
# class SliderWLimits( widgets.IntRangeSlider, _EnforceSliderGap ):
#     def __init__(self, mgr):
#         self.step = 1
#         super().__init__(value=[5, 50], min=3, max=80, step=self.step, description='FWHM limits:', disabled=False, continuous_update=False, orientation='vertical', readout=True, readout_format='d', layout=widgets.Layout(width='100px', height='400px'))
#         self.observe(self.on_value_changed, names='value')
#         self.mgr = mgr
#
#     def on_value_changed(self, change):
#         self.mgr.on_wlimits_changed( change['new'] )



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


