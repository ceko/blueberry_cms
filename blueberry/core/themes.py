import models
raise Exception("This is not needed now.")

def prioritized_themes():    
    return  models.Theme.objects.all().order_by('-id')