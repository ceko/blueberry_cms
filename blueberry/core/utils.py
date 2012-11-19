from django.conf import settings
import packages.settings
from south.models import MigrationHistory
import unicodedata
import re
import models


class ControllerNotFoundError(Exception):
    pass

#This may not be needed anymore
def database_is_initialized():
    return MigrationHistory.objects.filter(app_name = 'core').count() > 0

def smart_class_loader(module_name):
    """
    Loads a class by looking through loaded templates.  Will return the first class it finds in prioritized themes.  
    The class must be named the same as the end path of the module.
    Ex: blueberry.core.packages.default.templatecontrollers.homepage with class homepage.
    """    
    for package in settings.PACKAGES:
        this_module_name = "{0}.{1}".format(
            package,
            module_name
        )
        
        try:
            class_name = this_module_name.split('.')[-1]
            module = __import__(this_module_name, fromlist = [class_name,])                    
            return getattr(module, class_name)
        except ImportError:
            pass
    
    return None

def get_template_controller_instance(resource_map):
    module_name = "templatecontrollers.{0}".format(             
        resource_map.resource.template.class_path
    )  
    klass = smart_class_loader(module_name)
    if not klass:
        raise ControllerNotFoundError('A controller for "{0}" was not found in any packages.'.format(resource_map.resource.template.class_path))
    else:
        return klass

def get_block_controller_instance(klass_path):
    module_name = "scaffolding.blocks.{0}".format(             
        klass_path
    )  
    klass = smart_class_loader(module_name)
    if not klass:
        raise ControllerNotFoundError('A block controller for "{0}" was not found in any packages.'.format(klass_path))
    else:
        return klass

def moduleify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces and hyphens to underscores.
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\.\s-]', '', value).strip().lower())
    return re.sub('[-\s\.]+', '_', value)

def get_canonical_path(path):
    if not path.endswith("/"):
        path += "/"
    if not path.startswith("/"):
        path = "/" + path
        
    return path

def get_resource_map(path):
    #This should get a resource map by checked out revision.  It would probably be
    #something transient that would throw an exception on save.  The function would always pull the current resource
    #map if the user was anonymous, but if they were logged in it would query permissions and pull either the current or the 
    #currently checked out one for review or editing.
    path = get_canonical_path(path)
        
    return models.ResourceMap.objects.select_related('parent', 'resource', 'resource__template').get(pk=path)
    