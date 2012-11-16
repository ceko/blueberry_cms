from blueberry.core.templates import HTMLTemplateController 


class homepage(HTMLTemplateController):    
    template = 'homepage.html'
        
    def __init__(self, *args, **kwargs):
        super(homepage, self).__init__(*args, **kwargs)
        #self.load_panel('main_content')
    