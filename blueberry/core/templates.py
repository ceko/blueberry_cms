from utils import smart_class_loader
from django.conf import settings
from django.template.loader import render_to_string
from django.template import RequestContext
import models


class PanelLoadedError(Exception):
    pass

class PanelLoaderError(Exception):
    pass

class BlockLoadedError(Exception):
    pass

class BlockLoaderError(Exception):
    pass

class BLOCK_PERSISTENCE_LEVELS:
    _none = 1
    _global = 2
    _page = 3     

class PANEL_PERSISTENCE_LEVELS:
    _global = 1
    _page = 2

class BlockLoader(object):
    
    def __init__(self, controller, request, resource_map):
        self.controller = controller
        self.request = request
        self.resource_map = resource_map

    def load(self, block_id, block_type, persistence_level):
        module_name = "scaffolding.blocks.{0}".format(block_type)  
        block_class = smart_class_loader(module_name)
        if not block_class:
            raise BlockLoaderError("Could not find block for " + block_type)
            
        if persistence_level == BLOCK_PERSISTENCE_LEVELS._none:
            return block_class(block_id, self.request, self.resource_map, self.controller)
        else:
            raise Exception("Not supported yet.")

class PanelLoader(object):
    
    def __init__(self, controller, request, resource_map):
        self.controller = controller
        self.request = request
        self.resource_map = resource_map
        
    def load(self, panel_id, panel_type, persistence_level):        
        module_name = "scaffolding.panels.{0}".format(panel_type)  
        panel_class = smart_class_loader(module_name)
        if not panel_class:
            raise PanelLoaderError("Could not find panel for " + panel_type)
            
        if persistence_level == PANEL_PERSISTENCE_LEVELS._page:
            return panel_class(panel_id, self.request, self.resource_map, self.controller)
        else:
            raise Exception("Not supported yet.")

class ControllerBase(object):
    
    def __init__(self, request, resource_map, parent = None):
        self.request = request
        self.resource_map = resource_map
        self.block_loader = BlockLoader(self, request, resource_map)
        self.panel_loader = PanelLoader(self, request, resource_map)
        self.parent = parent
        
        self.panels = {}
        #Global blocks that don't belong to panels. 
        self.blocks = {}
        self._load_persistent_panels()
    
    def _load_persistent_panels(self):
        
        blocks = models.Block.objects.select_related().filter(panel__resource__exact = self.resource_map.resource_id)        
        for block in blocks:
            block_container = self.panels.get(block.panel.alias, None)
            if not block_container:
                block_container = self.panel_loader.load(block.panel.alias, block.panel.class_path, PANEL_PERSISTENCE_LEVELS._page)
                self.panels[block.panel.alias] = block_container                
            
            loaded_block = block_container.block_loader.load(block.alias, block.class_path, BLOCK_PERSISTENCE_LEVELS._none)
            block_container.blocks[loaded_block.id] = loaded_block      
                
    def load_block(self, block_id, block_type, persistence_level = BLOCK_PERSISTENCE_LEVELS._none):
        if self.blocks.has_key(block_id):
            raise BlockLoadedError("Block with id {0} has already been loaded.".format(block_id))
            
        block = self.block_loader.load(block_id, block_type, persistence_level)
        self.blocks[block_id] = block
    
    #This probably shouldn't exist, or should be changed.    
    def load_panel(self, panel_id, panel_type = 'default_panel', persistence_level = PANEL_PERSISTENCE_LEVELS._page):
        if self.panels.has_key(panel_id):
            raise PanelLoadedError("Panel with id {0} has already been loaded.".format(panel_id))
        
        panel = self.panel_loader.load(panel_id, panel_type, persistence_level)   
        self.panels[panel_id] = panel
        
class HTMLTemplateController(ControllerBase):
    
    def __init__(self, *args, **kwargs):
        super(HTMLTemplateController, self).__init__(*args, **kwargs)
        self.load_block('breadcrumbs', 'navigation.breadcrumbs')
        
class BlockControllerBase(ControllerBase):
    
    def __init__(self, id, request, resource_map, parent = None):
        self.id = id
        self.request = request
        self.resource_map = resource_map
        self.block_loader = BlockLoader(self, request, resource_map)
        self.panel_loader = PanelLoader(self, request, resource_map)
        self.parent = parent
    
    def __unicode__(self):
        template_vars = {
            'block' : self,
            'controller' : self.parent,
        }
        return render_to_string(self.template, template_vars, context_instance = RequestContext(self.request))

class PanelBase(object):
    
    def __init__(self, id, request, resource_map, parent):
        self.id = id
        self.request = request
        self.resource_map = resource_map
        self.block_loader = BlockLoader(self, request, resource_map)
        self.parent = parent
        self.blocks = {}       
        
    def __unicode__(self):
        output = u''        
        for key, value in self.blocks.items():            
            template_vars = {
                'block' : value,
                'panel' : self,
            }
            
            output += render_to_string(value.template, template_vars, context_instance = RequestContext(self.request))
        
        return output
    