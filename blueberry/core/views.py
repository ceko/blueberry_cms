from flow import BlueberryContext
from django.shortcuts import render_to_response, HttpResponseRedirect
import utils
import models


def request_processor(request, path):    
    canonical_path = utils.get_canonical_path(path)    
    if canonical_path.lstrip('/') != path and canonical_path <> "/":
        return HttpResponseRedirect(canonical_path)
    
    resource_map = utils.get_resource_map(canonical_path)
    context = BlueberryContext(request, resource_map)
    template_controller_klass = utils.get_template_controller_instance(resource_map)
    template_controller = template_controller_klass(context)
    template_vars = {
        'controller' : template_controller,
    }
              
    return render_to_response(template_controller.template, template_vars, context_instance=context)