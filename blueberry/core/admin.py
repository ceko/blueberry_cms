from django.contrib import admin
import models 


class ThemeAdmin(admin.ModelAdmin):
    readonly_fields = ['class_path',]
    list_display = ['priority', 'pretty_name', 'class_path',] 
    list_display_links = ['pretty_name',]

admin.site.register(models.Theme, ThemeAdmin)

class ResourceTemplateAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.ResourceTemplate, ResourceTemplateAdmin)

class ResourceAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Resource, ResourceAdmin)

class ResourceMapAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.ResourceMap, ResourceMapAdmin)

class PanelAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Panel, PanelAdmin)

class BlockAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Block, BlockAdmin)

class RevisionAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Revision, RevisionAdmin)