from blueberry.core.templates import HTMLTemplateController, PANEL_PERSISTENCE_LEVELS
 
class BaseHTMLTemplateController(HTMLTemplateController):
            
    def __init__(self, *args, **kwargs):
        super(BaseHTMLTemplateController, self).__init__(*args, **kwargs)
        header_content = self.register_panel('header_content', persistence_level = PANEL_PERSISTENCE_LEVELS._none)        
        header_content.register_block('breadcrumbs', 'navigation.breadcrumbs')               
        