import models


def prioritized_themes():    
    return  models.Theme.objects.all().order_by('-id')