from blueberry.core.templates import BlockControllerBase


class breadcrumbs(BlockControllerBase):
    
    template = 'blocks/navigation/breadcrumbs.html'
    
    def resource_hierarchy(self):
        resource_maps = [self.blueberry_context.resource_map]
        curr_obj = resource_maps[0]
        while curr_obj.parent_id:
            curr_obj = curr_obj.parent
            resource_maps.insert(0, curr_obj)
        
        return resource_maps