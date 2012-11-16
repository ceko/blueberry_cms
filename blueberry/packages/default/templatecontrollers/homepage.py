from base import BaseHTMLTemplateController 


class homepage(BaseHTMLTemplateController):    
    template = 'homepage.html'
        
    def __init__(self, *args, **kwargs):
        super(homepage, self).__init__(*args, **kwargs)
        
    