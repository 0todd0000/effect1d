

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
                self.output_widget.clear_output(wait=True)
                print( *args )
    
    def on_d_changed(self, x):
        self._print('d changed', x)
        self.results_widget.update_d( x )

    def on_fwhm_changed(self, x):
        self._print('FWHM changed', x)
        self.results_widget.update_fwhm( x )

    def on_groupsize_changed(self, n):
        self._print('Group size changed', n)
        self.figure_widget.update( n )
        self.results_widget.update_n( n )

    def set_figure_widget(self, w):
        self.figure_widget  = w

    def set_output_widget(self, w):
        self.output_widget  = w

    def set_results_widget(self, w):
        self.results_widget = w
        
        