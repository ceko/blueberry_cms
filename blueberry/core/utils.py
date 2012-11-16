from django.conf import settings
from south.models import MigrationHistory
from os import path 
import themes
import unicodedata
import re


class ControllerNotFoundError(Exception):
    pass

def database_is_initialized():
    return MigrationHistory.objects.filter(app_name = 'core').count() > 0

def smart_class_loader(module_name):
    """
    Loads a class by looking through loaded templates.  Will return the first class it finds in prioritized themes.  
    The class must be named the same as the end path of the module.
    Ex: blueberry.core.packages.default.templatecontrollers.homepage with class homepage.
    """    
    for theme in settings.INSTALLED_THEMES:
        this_module_name = "{0}.{1}.{2}".format(
            settings.PACKAGES_MODULE_ROOT,
            theme.class_path,
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

def moduleify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces and hyphens to underscores.
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\.\s-]', '', value).strip().lower())
    return re.sub('[-\s\.]+', '_', value)