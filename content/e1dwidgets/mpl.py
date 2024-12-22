
import ipywidgets as widgets
from mpl_interactions import ipyplot as iplt
import matplotlib.pyplot as plt
import numpy as np


from matplotlib.widgets import Slider, RangeSlider




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


class MPLWidget( widgets.Box ):

    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_axes([0,0.25,1,0.75])

        x = np.linspace(0, 2 * np.pi, 200)

        def f(x, freq):
            return np.sin(x * freq[1])

        ax0 = plt.axes([0.25, 0.1, 0.65, 0.03])
        # slider = Slider(axfreq, label="freq", valmin=0.05, valmax=10)
        slider = RangeSlider(ax0, label="xlim", valmin=0.05, valmax=10)
        self.controls = iplt.plot(x, f, freq=slider, ax=self.ax)


        super().__init__(  [self.controls.vbox] )


#
#
# class MPLWidget( widgets.Box ):
#
#     def __init__(self):
#         self.fig = plt.figure()
#         self.ax = self.fig.add_axes([0,0.25,1,0.75])
#
#         x = np.linspace(0, 2 * np.pi, 200)
#
#         def f(x, xlim):
#             return np.sin(x * xlim[1])
#
#         ax0     = plt.axes([0.25, 0.1, 0.65, 0.03])
#         # ax1     = plt.axes([0, 0.25, 0.03, 0.66])
#         # slider = Slider(axfreq, label="freq", valmin=0.05, valmax=10)
#         slider0 = RangeSlider(ax0, label="xlim", valmin=0.05, valmax=10, orientation='horizontal')
#         # slider1 = RangeSlider(ax1, label="ylim", valmin=0.05, valmax=10, orientation='vertical')
#         self.controls = iplt.plot(x, f, xlim=slider0, ax=self.ax)
#
#
#         super().__init__(  [self.controls.vbox] )