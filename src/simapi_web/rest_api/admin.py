from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Timestep)
admin.site.register(models.Input)
admin.site.register(models.Output)
