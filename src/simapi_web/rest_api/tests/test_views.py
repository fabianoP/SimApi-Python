from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.views import status
from rest_api.temp.models import User, InitModel


class UserInitModelCreateAPIView(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('api-timestep-list')
        self.test_user = User(name='test_user2',
                              email='testuser2@test.com',
                              password='test user2 88')

    def test_create_time_step(self):
        self.assertEquals(
            Timestep.objects.count(),
            0
        )

        data = {
            'user': self.test_user,
            'time_step': 600
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(
            Timestep.objects.count(),
            1
        )

        timestep = Timestep.objects.first()
        self.assertEquals(timestep.user,
                          data['user'])
        self.assertEquals(timestep.time_step,
                          data['time_step'])

    def test_get_time_step_list(self):
        timestep = Timestep(user=self.test_user,
                            time_step=600)
        timestep.save()

        response = self.client.get(self.url)
        response_json = response.json()

        self.assertEquals(response.status_code,
                          status.HTTP_200_OK)

        self.assertEquals(len(response_json),
                          1)

        data = response_json[0]
        self.assertEquals(data['user'],
                          timestep.user)
        self.assertEquals(data['time_step'],
                          timestep.time_step)

