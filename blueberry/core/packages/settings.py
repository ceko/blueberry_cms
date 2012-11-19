import sys
from threading import Lock
import django.conf


_p = []
#TODO: If a path is sent that is different, refresh the cache.
def get_package_settings(package_paths):
    lock = Lock()
    lock.acquire()
    try:
        if any(_p):
            return _p
              
        for package in package_paths:
            _p.append(PackageSettings(package))
    finally:
        lock.release()
    
    return _p
                
class PackageSettings(object):
    
    def __init__(self, klass_path):
        self._klass_path = klass_path
        settings_path = '{0}.settings'.format(klass_path)
        __import__(settings_path)
        self._settings = sys.modules[settings_path]
    
    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, '_settings').__getattribute__(name)
        except AttributeError:
            return object.__getattribute__(self, name)
     
    def urlpatterns(self):        
        urls_path = '{0}.urls'.format(self._klass_path)
        __import__(urls_path)
        return sys.modules[urls_path].urlpatterns