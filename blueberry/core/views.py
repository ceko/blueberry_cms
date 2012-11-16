from pipeline import BlueberryContext
from django.shortcuts import render_to_response, HttpResponseRedirect
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
    
    resource_map = models.ResourceMap.objects.select_related('parent', 'resource', 'resource__template').get(pk=path)
    context = BlueberryContext(request, resource_map)
    template_controller_klass = utils.get_template_controller_instance(resource_map)
    template_controller = template_controller_klass(context)  
    
    template_vars = {
        'controller' : template_controller,
    }
              
    return render_to_response(template_controller.template, template_vars, context_instance=context)