from django.db import models
import blueberry.core.models

class AbstractBlock(models.Model):

    block = models.ForeignKey(blueberry.core.models.Block)

    class Meta:
        abstract = True

class GenericContentBlock(AbstractBlock):
        
    content = models.TextField()