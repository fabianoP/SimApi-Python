from django.db import models
from user_profile.models import User

# Create your models here.


class Timestep(models.Model):
    """Represents the Timestep values for the fmu"""

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    time_step = models.BigIntegerField(unique=True, default=0, primary_key=True)

    objects = models.Manager()


class Output(models.Model):
    """Represents output received from an fmu timestep"""

    timestep = models.OneToOneField(Timestep, primary_key=True, on_delete=models.CASCADE, unique=True)
    yshade = models.DecimalField(max_digits=20, decimal_places=4)
    dry_bulb = models.DecimalField(max_digits=20, decimal_places=4)
    troo = models.DecimalField(max_digits=20, decimal_places=4)
    isolext = models.DecimalField(max_digits=20, decimal_places=4)
    sout = models.DecimalField(max_digits=20, decimal_places=4)
    zonesens = models.DecimalField(max_digits=20, decimal_places=4)
    cool_rate = models.DecimalField(max_digits=20, decimal_places=4)

    objects = models.Manager()


class Input(models.Model):
    """Represents fmu inputs from web api"""

    timestep = models.OneToOneField(Timestep, primary_key=True, on_delete=models.CASCADE, unique=True)
    yshade = models.DecimalField(max_digits=20, decimal_places=4)

    objects = models.Manager()
