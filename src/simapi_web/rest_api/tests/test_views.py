from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.views import status

from rest_api.models import Timestep, Input, Output
from user_profile.models import User


class TimeStepCreateAPIView(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('api-time-step', kwargs={'version': 'v1'})

    def test_create_timestep(self):
        self.assertEquals(
            Timestep.objects.count(),
            0
        )

        data = {

        }
