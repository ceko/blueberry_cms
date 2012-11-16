from utils import smart_class_loader
from django.utils.safestring import mark_safe
from django.conf import settings
from django.template.loader import render_to_string
from django.template import RequestContext
import models
from pipeline import BlueberryContext
from html import HTML


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
    _inherit = 4

class PANEL_PERSISTENCE_LEVELS:
    _none = 1
    _global = 2
    _page = 3

class BlockLoader(object):
    
    block_loader_template = "scaffolding.blocks.{0}"
    
    def __init__(self, controller, blueberry_context):
        self.controller = controller
        self.blueberry_context = blueberry_context

    def load_type(self, class_path):
        module_name = self.block_loader_template.format(class_path)  
        block_class = smart_class_loader(module_name)
        if not block_class:
            raise PanelLoaderError("Could not find block for " + class_path)
        return block_class

    def load_persistent(self, block, persistence_level):
        block_class = self.load_type(block.template.class_path)            
        return block_class(block, self.blueberry_context, persistence_level, self.controller)

    #I think this may only be used when loading transient blocks, so this could probably be refactored.
    def load_unbound(self, panel, alias, class_path, persistence_level):
        block_class = self.load_type(class_path)
        block = models.Block.create_initial(panel.model)        
        if persistence_level == BLOCK_PERSISTENCE_LEVELS._none or \
           persistence_level == BLOCK_PERSISTENCE_LEVELS._inherit and panel.persistence_level == PANEL_PERSISTENCE_LEVELS._none:
            block.transient = True
            
        return block_class(block, self.blueberry_context, persistence_level, self.controller)

class PanelLoader(object):
    
    panel_loader_template = "scaffolding.panels.{0}"
        
    def __init__(self, controller, blueberry_context):
        self.controller = controller
        self.blueberry_context = blueberry_context
    
    def load_type(self, class_path):
        if not class_path:
            class_path = "default_panel"
            
        module_name = self.panel_loader_template.format(class_path)  
        panel_class = smart_class_loader(module_name)
        if not panel_class:
            raise PanelLoaderError("Could not find panel for " + class_path)
        return panel_class
        
    def load_persistent(self, panel, persistence_level, class_path=None):
        panel_class = self.load_type(class_path)        
        return panel_class(panel, self.blueberry_context, persistence_level, self.controller)        
    
    #I think this may only be used when loading transient panels, so this could probably be refactored.
    def load_unbound(self, alias, persistence_level, class_path=None):        
        panel_class = self.load_type(class_path)
        panel = models.Panel.create_initial(alias, self.blueberry_context)
        if persistence_level == PANEL_PERSISTENCE_LEVELS._none:
            panel.transient = True
            
        return panel_class(panel, self.blueberry_context, PANEL_PERSISTENCE_LEVELS._none, self.controller)        
    
class ControllerBase(object):
    
    def __init__(self, blueberry_context, parent = None):
        self.blueberry_context = blueberry_context        
        self.panel_loader = PanelLoader(self, blueberry_context)
        self.parent = parent
        
        self.panels = {}        
        self._load_persistent_panels()
    
    def _load_persistent_panels(self):
        """
        Loads persistent panel and block information into the panel dictionary.  The blocks may be finished loading, or they
        may need another database call to populate with persisted information.
        """        
        blocks = models.Block.objects.select_related().filter(panel__resource__exact = self.blueberry_context.resource_map.resource_id)        
        for block in blocks:
            block_container = self.panels.get(block.panel.alias, None)
            if not block_container:
                block_container = self.panel_loader.load_persistent(block.panel, PANEL_PERSISTENCE_LEVELS._page)
                self.panels[block.panel.alias] = block_container                
            
            loaded_block = block_container.block_loader.load_persistent(block, BLOCK_PERSISTENCE_LEVELS._page)
            block_container.blocks[loaded_block.model.id] = loaded_block      
     
    def register_panel(self, panel_id, class_path = 'default_panel', persistence_level = PANEL_PERSISTENCE_LEVELS._page):
        """
        Panels that haven't been persisted to the database yet are registered.  All panels that have been saved are loaded
        at page controller initialization. 
        """
        if self.panels.has_key(panel_id):
            raise PanelLoadedError("Panel with id {0} has already been loaded.".format(panel_id))
        
        panel = self.panel_loader.load_unbound(panel_id, persistence_level, class_path)   
        self.panels[panel_id] = panel
        return panel
        
class HTMLTemplateController(ControllerBase):
    
    def __init__(self, *args, **kwargs):
        super(HTMLTemplateController, self).__init__(*args, **kwargs)        
        
class BlockControllerBase(ControllerBase):
    
    def __init__(self, block, blueberry_context, persistence_level = BLOCK_PERSISTENCE_LEVELS._inherit, parent = None):
        self.model = block
        self.blueberry_context = blueberry_context
        self.persistence_level = persistence_level        
        self.parent = parent
    
    def is_transient(self):
        return \
            self.persistence_level == BLOCK_PERSISTENCE_LEVELS._none or \
            self.parent.persistence_level == PANEL_PERSISTENCE_LEVELS._none and \
            self.persistence_level == BLOCK_PERSISTENCE_LEVELS._inherit
            
    
    def __unicode__(self):
        template_vars = {
            'block' : self,
            'panel' : self.parent,
            'controller' : self.parent,
        }        
        output = render_to_string(self.template, template_vars, context_instance = self.blueberry_context)
        return mark_safe(HTMLBuilder.wrap_block(self, output))

class PanelControllerBase(object):
    
    def __init__(self, panel, blueberry_context, persistence_level = PANEL_PERSISTENCE_LEVELS._page, parent = None):
        self.model = panel
        self.blueberry_context = blueberry_context
        self.persistence_level = persistence_level
        self.block_loader = BlockLoader(self, blueberry_context)
        self.parent = parent
        self.blocks = {}       
    
    def register_block(self, block_id, block_type, persistence_level = BLOCK_PERSISTENCE_LEVELS._inherit):
        """
        Panels that haven't been persisted to the database yet are registered.  All blocks that have been saved are loaded
        at page controller initialization. 
        """
        if self.blocks.has_key(block_id):
            raise BlockLoadedError("Block with id {0} has already been loaded.".format(block_id))
            
        block = self.block_loader.load_unbound(self, block_id, block_type, persistence_level)
        self.blocks[block_id] = block
        return block
    
    def is_transient(self):
        return self.persistence_level == PANEL_PERSISTENCE_LEVELS._none
        
    def __unicode__(self):
        output = u''        
        for key, value in self.blocks.items():
            output += value.__unicode__()
        
        return mark_safe(HTMLBuilder.wrap_panel(self, output))


class HTMLBuilder(object):
    
    @staticmethod
    def wrap_panel(panel, panel_output):
        if panel.blueberry_context.request.user.is_authenticated() and not panel.is_transient():
            h = HTML()
            d = h.div(klass = "berry_edit_panel")
            d.text(panel_output, escape=False)
            d = h.div(klass = "berry_add_block", panel_id = unicode(panel.model.id))
            d.text("Add Block")
            return h.__unicode__()
        else:
            return panel_output
    
    @staticmethod
    def wrap_block(block, block_output):
        if block.blueberry_context.request.user.is_authenticated() and not block.is_transient():
            h = HTML()
            d = h.div(klass = "berry_edit_block", block_id = unicode(block.model.id))
            d.text(block_output, escape=False)
            return h.__unicode__()
        else:
            return block_output
    
    
    