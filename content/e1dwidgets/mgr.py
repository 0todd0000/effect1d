
from IPython.display import clear_output


class CallbackManager( object ):
    def __init__(self, print_messages=True):
        self.print_messages = print_messages
        self.output_widget  = None
        self.results_widget = None
        self.figure_widget  = None

    def _print(self, *args):
        if self.print_messages:
            with self.output_widget:
                # clear_output(wait=True)
                self.output_widget.clear_output(wait=True)
                print( *args )
    
    def on_d_changed(self, x):
        self._print('d changed', x)
        self.results_widget.set_pvalue( '0.234' )
        self.results_widget.set_interpretation( 'Very big da yo' )

    def on_design_changed(self, x):
        self._print('design changed', x)

    def on_dlimits_changed(self, lim):
        x0,x1 = lim
        self._print('d limits changed', x0, x1)
   
    def on_fwhm_changed(self, x):
        self._print('FWHM changed', x)

    def on_groupsize_changed(self, n):
        self._print('Group size changed', n)
        # params  = Effect1DPlotParameters(n=int(n), d=1.0, w=20, dlim=(0.2,5), wlim=(3,50))
        # self.figure_widget.update(params)
        self.figure_widget.update(None)
        
    
    def on_wlimits_changed(self, lim):
        x0,x1 = lim
        self._print('FWHM limits changed', x0, x1)

    def set_figure_widget(self, w):
        self.figure_widget  = w

    def set_output_widget(self, w):
        self.output_widget  = w
        
    def set_results_widget(self, w):
        self.results_widget = w
        
    