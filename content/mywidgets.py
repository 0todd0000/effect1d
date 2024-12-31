
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
        
        

class SpinGroupSize( widgets.BoundedIntText ):
    def __init__(self, mgr=None, image_widget=None):
        super().__init__(value=8, min=3, max=40, step=1, description='Group size', disabled=False, layout=widgets.Layout(width='200px'),)
        self.observe(self.on_value_changed, names='value')
        self.mgr = mgr
        self.image_widget = image_widget

    def on_value_changed(self, change):
        n = change['new']
        # with out:
        #     clear_output()
        #     print( "n = ", n)

        fpath = f'img/contours_n={n}.png'
        with open(fpath, 'rb') as f:
            img = f.read()
        self.image_widget.value = img
        # self.mgr.on_groupsize_changed( change['new'] )

