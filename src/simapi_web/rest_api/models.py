from django.db import models
from django.conf import settings

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

from django.contrib.postgres.fields import JSONField

# TODO make fat models
from django.db.models import FileField


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
    """represents Users in the system"""
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

# TODO possibly just store JSON in all models except user.


class FileModel(models.Model):
    file = FileField(upload_to='./Media/', default='')


class FmuModelParameters(models.Model):
    """represents .fmu initialization parameters"""
    model_name = models.CharField(max_length=255, unique=True, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    idf_file = FileField(upload_to='./Media/', default='')
    epw_file = FileField(upload_to='./Media/', default='')

    # set as single json object
    step_size = models.IntegerField(default=0, unique=False)
    final_time = models.DecimalField(max_digits=20, decimal_places=1)
    created_on = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):

        return self.model_name


class Input(models.Model):
    """represents inputs from web api going to an fmu model"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fmu_model = models.ForeignKey(FmuModelParameters, on_delete=models.CASCADE)

    # set as single json object
    input = JSONField()

    objects = models.Manager()


class Output(models.Model):
    """represents output received from an fmu time step"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fmu_model = models.ForeignKey(FmuModelParameters, on_delete=models.CASCADE)

    # set as single json object
    output = JSONField()

    objects = models.Manager()




