from blueberry.core.templates import BlockControllerBase
from django import forms
from blueberry.seed import models
from blueberry.core.forms import BaseEditorModelForm


class generic_content_form(BaseEditorModelForm):
        
    content = forms.CharField()
    
    class Meta(BaseEditorModelForm.Meta):
        model = models.GenericContentBlock

class generic_content(BlockControllerBase):
    
    template = 'blocks/editors/generic_content.html'
    add_form_klass = generic_content_form
    edit_form_klass = generic_content_form
    
    def get_template_data(self):        
        return {'content' : self.get_extended_data().content,}
    
    #TODO: Cache this of course    
    def get_extended_data(self):
        return models.GenericContentBlock.objects.get(block = self.model)
