from django.conf import settings
from blueberry.core import flow
from django.shortcuts import render_to_response, HttpResponse, HttpResponseRedirect
import blueberry.core.models
import blueberry.core.utils


def select_new_block_template(request, path, panel_id):     
    resource_map = blueberry.core.utils.get_resource_map(blueberry.core.utils.get_canonical_path(path))
    context = flow.BlueberryContext(request, resource_map)
    panel_alias = None
    try:
        float(panel_id)
        panel_alias = blueberry.core.models.Panel.objects.get(pk=panel_id).alias
    except ValueError, TypeError:
        panel_alias = panel_id    
    
    blocks = blueberry.core.models.BlockTemplate.objects.all()        
    template_vars = {
        'panel_alias' : panel_alias,
        'panel_id' : panel_id,
        'persistent_blocks' : blocks,
        'base_resource_url' : resource_map.url,
    }
    return render_to_response('admin/blocks/select_new_block_template.html', template_vars, context_instance=context)

def add_block_by_template(request, path, template_id, panel_id):
    resource_map = blueberry.core.utils.get_resource_map(blueberry.core.utils.get_canonical_path(path))
    context = flow.BlueberryContext(request, resource_map)
    block_template = blueberry.core.models.BlockTemplate.objects.get(pk=template_id)
    
    block_klass = blueberry.core.utils.get_block_controller_instance(block_template.class_path)     
    block_controller = block_klass(None, context)
    add_form_klass = block_controller.add_form_klass
    add_form = None
    
    if request.method == 'POST':
        add_form = add_form_klass(request.POST, request.FILES)
        if add_form.is_valid():            
            #assume we're adding to a panel that already exists, this will break for "new" panels.
            block = blueberry.core.models.Block()
            block.panel = blueberry.core.models.Panel.objects.get(pk=panel_id)
            block.template = blueberry.core.models.BlockTemplate.objects.get(pk=template_id)
            block.save()            
            add_form.save(block.id)
            return HttpResponseRedirect(resource_map.url + 'add-block-success/')
    else:
        add_form = add_form_klass()
    
    template_vars = {
        'add_form' : add_form,     
        'form_width' : add_form_klass.form_width,
        'form_height' : add_form_klass.form_height,   
    }
    
    return render_to_response('admin/blocks/add_block_by_template.html', template_vars, context_instance=context)

def add_block_success(request, path):
    resource_map = blueberry.core.utils.get_resource_map(blueberry.core.utils.get_canonical_path(path))
    context = flow.BlueberryContext(request, resource_map)
    return render_to_response('admin/blocks/add_block_success.html', {'base_resource_url' : resource_map.url}, context_instance=context)

def edit_block(request, path, block_id):    
    resource_map = blueberry.core.utils.get_resource_map(blueberry.core.utils.get_canonical_path(path))
    context = flow.BlueberryContext(request, resource_map)
    block = blueberry.core.models.Block.objects.select_related().get(pk=block_id)
        
    block_klass = blueberry.core.utils.get_block_controller_instance(block.template.class_path)     
    block_controller = block_klass(block, context)
    edit_form_klass = block_controller.edit_form_klass    
    edit_form = None
    
    if request.method == 'POST':
        edit_form = edit_form_klass(request.POST, request.FILES, instance=block_controller.get_extended_data())
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(resource_map.url + 'edit-block-success/')
    else:
        edit_form = edit_form_klass(instance=block_controller.get_extended_data())
        
    template_vars = {
        'edit_form' : edit_form,     
        'form_width' : edit_form_klass.form_width,
        'form_height' : edit_form_klass.form_height,   
    }
    
    return render_to_response('admin/blocks/edit_block_by_template.html', template_vars, context_instance=context)

def edit_block_success(request, path):
    resource_map = blueberry.core.utils.get_resource_map(blueberry.core.utils.get_canonical_path(path))
    context = flow.BlueberryContext(request, resource_map)
    return render_to_response('admin/blocks/edit_block_success.html', {'base_resource_url' : resource_map.url}, context_instance=context)

def delete_block(request, path, block_id):
    resource_map = blueberry.core.utils.get_resource_map(blueberry.core.utils.get_canonical_path(path))    
    block = blueberry.core.models.Block.objects.select_related().get(pk=block_id)
    block.delete()
    return HttpResponseRedirect(resource_map.url)     