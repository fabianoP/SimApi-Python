from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.FmuModel)
admin.site.register(models.Input)
admin.site.register(models.Output)
admin.site.register(models.ContainerHostNames)
