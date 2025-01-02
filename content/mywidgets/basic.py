
import ipywidgets as widgets



class AppHeader( widgets.HBox ):
    def __init__(self):
        s = '''
        <h1 style="text-align:center;">Effect Size Interpretation Calculator</h1>
        <h3 style="text-align:center;">One-dimensional functional data, two-sample case</h3>
        '''
        w        = widgets.HTML(value=s, placeholder='', description='')
        layout   = widgets.Layout(display='flex', flex_flow='column', align_items='center')
        super().__init__(children=[w], layout=layout)
        


class FigureWidget( widgets.Image ):
    def __init__(self, mgr):
        img = self._load_image( 8 )
        super().__init__(value=img, format='png', border=None, width=600)
        self.mgr = mgr
        self.mgr.set_figure_widget( self )

    def _load_image(self, n):
        fpath = f'img/contours_n={n}.png'
        with open(fpath, 'rb') as f:
            img = f.read()
        return img
    
    def update(self, n):
        self.value = self._load_image( n )
        # self.mgr.on_groupsize_changed( change['new'] )




class Header( widgets.HBox ):
    def __init__(self, label):
        w        = widgets.HTML(value=f'<h3>{label}</h3>', placeholder='', description='')
        layout   = widgets.Layout(display='flex', flex_flow='column', align_items='center')
        super().__init__(children=[w], layout=layout)




class Output( widgets.Output ):
    def __init__(self, mgr):
        super().__init__()
        self.mgr  = mgr
        self.mgr.set_output_widget( self )
        
    


class ResultsTextBox( widgets.Text ):
    def __init__(self, label):
        super().__init__(value='(None)', placeholder='', description=label, disabled=True, layout = widgets.Layout(width='200px'))



class SpinGroupSize( widgets.BoundedIntText ):
    def __init__(self, mgr):
        super().__init__(value=8, min=3, max=40, step=1, description='Group size', disabled=False, layout=widgets.Layout(width='200px'),)
        self.observe(self.on_value_changed, names='value')
        self.mgr = mgr

    def on_value_changed(self, change):
        self.mgr.on_groupsize_changed( change['new'] )


class SpinFWHM( widgets.BoundedFloatText ):
    def __init__(self, mgr):
        super().__init__(value=25, min=3, max=80, step=0.1, description='FWHM', disabled=False, layout=widgets.Layout(width='200px'),)
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


