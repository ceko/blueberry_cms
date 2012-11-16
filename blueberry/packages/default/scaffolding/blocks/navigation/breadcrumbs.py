from blueberry.core.templates import BlockControllerBase


class breadcrumbs(BlockControllerBase):
    
    template = 'blocks/navigation/breadcrumbs.html'
    
    def resource_hierarchy(self):
        resource_maps = [self.resource_map]
        curr_obj = self.resource_map
        while curr_obj.parent_id:
            curr_obj = curr_obj.parent
            resource_maps.insert(0, curr_obj)
        
        return resource_maps