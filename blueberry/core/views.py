from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, HttpResponseRedirect
from django.conf import settings
import utils
import models


def request_processor(request, path):
    redirect = False      
    if not path.endswith("/"):
        path = path + "/"
        redirect = path <> "/"
    if not path.startswith("/"):
        path = "/" + path        
        
    if redirect:
        return HttpResponseRedirect(path)
    print request.META['REMOTE_ADDR']
    resource_map = models.ResourceMap.objects.select_related('parent', 'resource', 'resource__template').get(pk=path)
    template_controller_klass = utils.get_template_controller_instance(resource_map)
    template_controller = template_controller_klass(request, resource_map)  
    
    template_vars = {
        'controller' : template_controller,
    }
              
    return render_to_response(template_controller.template, template_vars, context_instance=RequestContext(request))