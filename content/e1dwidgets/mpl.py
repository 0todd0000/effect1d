
import ipywidgets as widgets
# from mpl_interactions import ipyplot as iplt
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO


# from matplotlib.widgets import Slider, RangeSlider




# class MPLWidget( widgets.Box ):
#
#     def __init__(self):
#         self.fig = plt.figure()
#         self.ax = self.fig.add_axes([0,0.25,1,0.75])
#
#         x = np.linspace(0, 2 * np.pi, 200)
#
#         def f(x, freq):
#             return np.sin(x * freq[1])
#
#         axfreq = plt.axes([0.25, 0.1, 0.65, 0.03])
#         # slider = Slider(axfreq, label="freq", valmin=0.05, valmax=10)
#         slider = RangeSlider(axfreq, label="freq", valmin=0.05, valmax=10)
#         self.controls = iplt.plot(x, f, freq=slider, ax=self.ax)
#
#
#         super().__init__(  [self.controls.vbox] )


# class MPLWidget( widgets.Box ):
#
#     def __init__(self):
#         self.fig = plt.figure()
#         self.ax = self.fig.add_axes([0.25,0.25,0.75,0.75])
#
#         x = np.linspace(0, 2 * np.pi, 200)
#
#         def f(x, xx, yy):
#             return np.sin(x * xx[1])
#
#         ax0 = plt.axes([0.25, 0.1, 0.65, 0.03])
#         ax1 = plt.axes([0.03, 0.25, 0.03, 0.65])
#         slider0 = RangeSlider(ax0, label="xlim", valmin=0.05, valmax=10, orientation='horizontal')
#         slider1 = RangeSlider(ax1, label="xlim", valmin=0.05, valmax=10, orientation='vertical')
#         self.controls = iplt.plot(x, f, xx=slider0, yy=slider1, ax=self.ax)
#
#
#         super().__init__(  [self.controls.vbox] )




# class MPLWidget( widgets.Box ):
#
#     def __init__(self):
#         self.fig = plt.figure()
#         self.ax = self.fig.add_axes([0.20,0.20,0.79,0.79])
#
#         self.fig.canvas.toolbar_visible = False
#         self.fig.canvas.header_visible = False
#         self.fig.canvas.footer_visible = False
#
#         # self.fig, self.ax = plt.subplots()
#         # plt.subplots_adjust(bottom=0.20, left=0.20)
#         #
#         x = np.linspace(0, 1, 11)
#
#         def f(x, xx, yy):
#             return np.random.randn(11)
#
#         ax0 = plt.axes([0.20, 0.05, 0.65, 0.03])
#         ax1 = plt.axes([0.05, 0.20, 0.03, 0.65])
#         slider0 = RangeSlider(ax0, label="xlim", valmin=0.05, valmax=10, valfmt='%.1f', orientation='horizontal')
#         slider1 = RangeSlider(ax1, label="xlim", valmin=0.05, valmax=10, valfmt='%.1f', orientation='vertical')
#         self.controls = iplt.plot(x, f, xx=slider0, yy=slider1, ax=self.ax, xlim='fixed', ylim='fixed')
#
#         # self.ax.set_title(None)
#
#
#         # def my_callback(a):
#         #     self.ax.set_xlim(0, 20)
#         #
#         # self.controls.register_callback(my_callback, "x")
#
#
#         super().__init__(  [self.controls.vbox] )
#
#
#
#     def connect(self, fn, *args):
#         self.controls.register_callback(fn, *args)
#
#     def update(self, out):
#         # with out:
#         #     print('aaaa')
#
#         self.ax.cla()
#         self.ax.plot(  np.random.randn(11, 'ro')  )
#         # plt.draw()
#         self.fig.canvas.draw()
        
        

class MPLImageWidget( widgets.Image ):

    def __init__(self):
        self.fig = plt.figure()
        self.ax  = self.fig.add_axes([0.20,0.20,0.79,0.79])
        
        self.fig.canvas.toolbar_visible = False
        self.fig.canvas.header_visible = False
        self.fig.canvas.footer_visible = False
        
        np.random.seed(0)
        self.shape = 20,50
        a     = np.random.randn( *self.shape )
        self.ax.imshow( a )
        # img       = self.fig2img()
        
        b = BytesIO()
        plt.savefig(b, format='png')
        b.seek(0)
        img = b.getvalue()
        b.close()
        
        
        super().__init__(value=img, format='png', border=None, width=300)
        
        # self.a1   = np.random.randn( *shape )
        # ### first image:
        # self.set_image( self.a0 )


        
        

    # def fig2img(self):
    #     b = BytesIO()
    #     plt.savefig(b, format='png')
    #     b.seek(0)
    #     img = b.getvalue()
    #     b.close()
    #     return img
    #
    #
    # def set_image(self, a):
    #     self.ax.cla()
    #     self.ax.imshow( a )
    #     self.value = self.fig2img()
    #
    #
    # # def connect(self, fn, *args):
    # #     self.controls.register_callback(fn, *args)
    # #
    # def update(self):
    #     a = np.random.randn( *self.shape )
    #     # with out:
    #     #     print('aaaa')
    #
    #     self.set_image(  a  )
    #     # plt.draw()
    #     # self.fig.canvas.draw()