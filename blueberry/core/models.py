from django.db import models
from django.contrib.auth.models import User
import utils


class Theme(models.Model):
    #The filesystem name, used for the template search path.
    class_path = models.CharField(max_length = 50, unique = True, default = "")    
    pretty_name = models.CharField(max_length = 50)
    #Controls template search path order. 
    priority = models.IntegerField(unique = True)
    
    def __unicode__(self):
        return "{0} ({1})".format(self.pretty_name, self.class_path)
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.class_path = utils.moduleify(self.pretty_name)
        
        super(Theme, self).save(*args, **kwargs)
    
class ResourceTemplate(models.Model):
    #The filesystem name.    
    class_path = models.CharField(max_length = 100)    
    pretty_name = models.CharField(max_length = 50)
    
    def __unicode__(self):
        return self.pretty_name

class Revision(models.Model):
    created_on = models.DateTimeField(auto_now = True)
    created_by = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.created_on.isoformat()
                
class Resource(models.Model):        
    revision = models.ForeignKey(Revision)    
    template = models.ForeignKey(ResourceTemplate)
    path_suffix = models.CharField(max_length = 100)
    title = models.CharField(max_length = 50)
    description = models.TextField()
    
    def __unicode__(self):
        return "{0}: {1}".format(self.path_suffix, self.title)
    
class ResourceMap(models.Model):
    revision = models.ForeignKey(Revision)
    parent = models.ForeignKey('ResourceMap', null = True, blank = True)
    url = models.CharField(primary_key = True, max_length = 500)    
    resource = models.ForeignKey(Resource) 
    
    def __unicode__(self):
        return self.url
    
class Panel(models.Model):
    class_path = models.CharField(max_length = 100)
    resource = models.ForeignKey(Resource)    
    alias = models.CharField(max_length = 100)
    
    class Meta:
        unique_together = (('resource', 'alias'),)
    
class Block(models.Model):    
    class_path = models.CharField(max_length = 100)
    panel = models.ForeignKey(Panel)
    alias = models.CharField(max_length = 100)
    
    class Meta:
        unique_together = (('panel', 'alias'),)
     