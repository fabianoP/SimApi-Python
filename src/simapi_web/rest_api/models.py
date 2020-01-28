from django.db import models

# Create your models here.


class Timestep(models.Model):
    """Represents the Timestep values for the fmu"""
    user_id = models.IntegerField()
    time_step = models.BigIntegerField()


class Output(models.Model):
    """Represents output received from an fmu timestep"""

    time_step = models.BigIntegerField()
    yshade = models.DecimalField(max_digits=20, decimal_places=4)
    dry_bulb = models.DecimalField(max_digits=20, decimal_places=4)
    troo = models.DecimalField(max_digits=20, decimal_places=4)
    isolext = models.DecimalField(max_digits=20, decimal_places=4)
    sout = models.DecimalField(max_digits=20, decimal_places=4)
    zonesens = models.DecimalField(max_digits=20, decimal_places=4)
    cool_rate = models.DecimalField(max_digits=20, decimal_places=4)


class Input(models.Model):
    """Represents fmu inputs from web api"""

    time_step = models.BigIntegerField()
    yshade = models.DecimalField(max_digits=20, decimal_places=4)


