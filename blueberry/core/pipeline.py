from django.template import RequestContext


class BlueberryContext(RequestContext):
           
    def __init__(self, request, resource_map, *args, **kwargs):
        super(BlueberryContext, self).__init__(request, *args, **kwargs)
        self.resource_map = resource_map
        self.request = request        
        
    
            
        
        