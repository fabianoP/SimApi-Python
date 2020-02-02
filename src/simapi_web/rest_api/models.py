from django.db import models
from django.conf import settings

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self, email, name, password=None):

        if not email:
            raise ValueError('User must have an email address.')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, name, password):

        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Represents Users in the system"""
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):

        return self.name

    def get_short_name(self):

        return self.name

    def __str__(self):

        return self.email


class Timestep(models.Model):
    """Represents the Timestep values for the fmu"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    time_step = models.BigIntegerField(unique=True, default=0, primary_key=True)

    objects = models.Manager()


class Output(models.Model):
    """Represents output received from an fmu timestep"""

    time_step = models.OneToOneField(Timestep, primary_key=True, on_delete=models.CASCADE, unique=True)
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

    time_step = models.OneToOneField(Timestep, primary_key=True, on_delete=models.CASCADE, unique=True)
    yshade = models.DecimalField(max_digits=20, decimal_places=4)

    objects = models.Manager()
