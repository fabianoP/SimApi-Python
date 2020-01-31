from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from django.test import TestCase

from rest_api.models import Input
from rest_api.models import Output
from rest_api.models import Timestep
from user_profile.models import User


class TimestepTestCase(TestCase):
    """
    Test case for Timestep model
    """
    def test_timestep(self):
        self.user = User.objects.create(name='test_user',
                                        email='testuser@test.com',
                                        password='test user 88')

        self.assertEquals(
            Timestep.objects.count(),
            0
        )
        Timestep.objects.create(user=self.user,
                                time_step=600)
        Timestep.objects.create(user=self.user,
                                time_step=1200)

        self.assertEquals(
            Timestep.objects.count(),
            2
        )


class InputTestCase(TestCase):
    """
    Test case for Input model
    """
    def test_input(self):
        self.user = User.objects.create(name='test_user',
                                        email='testuser@test.com',
                                        password='test user 88')

        self.t_step = Timestep.objects.create(user=self.user,
                                              time_step=600)
        self.t_step2 = Timestep.objects.create(user=self.user,
                                               time_step=1200)

        self.assertEquals(
            Input.objects.count(),
            0
        )
        Input.objects.create(
            time_step=self.t_step, yshade=1.0
        )
        Input.objects.create(
            time_step=self.t_step2, yshade=2.0
        )
        self.assertEquals(
            Input.objects.count(),
            2
        )


class OutputTestCase(TestCase):
    """
    Test case for Output model
    """
    def test_output(self):
        self.user = User.objects.create(name='test_user',
                                        email='testuser@test.com',
                                        password='test user 88')

        self.t_step = Timestep.objects.create(user=self.user,
                                              time_step=600)
        self.t_step2 = Timestep.objects.create(user=self.user,
                                               time_step=1200)

        self.assertEquals(
            Output.objects.count(),
            0
        )
        Output.objects.create(time_step=self.t_step,
                              yshade=1.0,
                              dry_bulb=1.2,
                              troo=1.5,
                              isolext=1.6,
                              sout=1.7,
                              zonesens=1.8,
                              cool_rate=1.9)
        Output.objects.create(time_step=self.t_step2,
                              yshade=1.2,
                              dry_bulb=1.4,
                              troo=1.8,
                              isolext=1.9,
                              sout=1.2,
                              zonesens=1.3,
                              cool_rate=1.6)
        self.assertEquals(
            Output.objects.count(),
            2
        )
