from profiles.localsettings import *
from themes import prioritized_themes
import utils


if utils.database_is_initialized():
    INSTALLED_THEMES = [x for x in prioritized_themes()]

    TEMPLATE_DIRS = (
        ["{0}{1}/templates".format(PACKAGES_ROOT, x.class_path) for x in INSTALLED_THEMES]
    )
    
    STATICFILES_DIRS = (    
        ["{0}{1}/static".format(PACKAGES_ROOT, x.class_path) for x in INSTALLED_THEMES]
    )
               

    