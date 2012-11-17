from django.template import RequestContext
from pipeline.compressors import CompressorBase
import cssmin


class BlueberryContext(RequestContext):
           
    def __init__(self, request, resource_map, *args, **kwargs):
        super(BlueberryContext, self).__init__(request, *args, **kwargs)
        self.resource_map = resource_map
        self.request = request        
        
class DefaultCompressor(CompressorBase):    
    
    def compress_js(self, js):
        raise Exception("Compressing javascript through the default compressor is not available.")
    
    def compress_css(self, css):
        return cssmin.cssmin(css)