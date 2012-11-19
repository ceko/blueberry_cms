from django import forms


class BaseEditorModelForm(forms.ModelForm):
    
    form_height = 400
    form_width = 500
    
    def save(self, block_id = None, *args, **kwargs):
        if block_id:
            kwargs.update({'commit' : False})
            extended_block = super(BaseEditorModelForm, self).save(*args, **kwargs)
            extended_block.block_id = block_id
            extended_block.save()
            return extended_block            
        else:                
            return super(BaseEditorModelForm, self).save(*args, **kwargs)
    
    class Meta:
        exclude = ('block',)

