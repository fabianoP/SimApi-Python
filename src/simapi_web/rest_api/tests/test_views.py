from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.views import status
from rest_api.models import Timestep, Input, Output, User


class UserCreateAPIView(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('api-user-list')

    def test_create_user(self):
        self.assertEquals(
            User.objects.count(),
            0
        )

        data = {
            'name': 'test_user',
            'email': 'testuser@test.com',
            'password': 'test user 88'
        }

        response = self.client.post(self.url, data=data, format='json')

        self.assertEquals(response.status_code,
                          status.HTTP_201_CREATED)
        self.assertEquals(User.objects.count(),
                          1)

        user = User.objects.first()

        self.assertEquals(user.name,
                          data['name'])
        self.assertEquals(user.email,
                          data['email'])

    def test_get_user_list(self):
        user = User(name='test_user',
                    email='testuser@test.com',
                    password='test user 88')
        user.save()

        response = self.client.get(self.url)
        response_json = response.json()

        self.assertEquals(response.status_code,
                          status.HTTP_200_OK)

        self.assertEquals(len(response_json),
                          1)

        data = response_json[0]

        self.assertEquals(data['name'],
                          user.name)
        self.assertEquals(data['email'],
                          user.email)


class TimeStepCreateAPIView(APITestCase):
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


class InputCreateAPIView(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('api-input-list')
        self.test_user = User(name='test_user3',
                              email='testuser3@test.com',
                              password='test user3 88')
        self.test_test_step = Timestep(user=self.test_user,
                                       time_step=600)

    def test_create_input(self):
        self.assertEquals(
            Input.objects.count(),
            0
        )

        data = {
            'time_step': self.test_test_step,
            'yshade': 1.0
        }
        response = self.client.post(self.url,
                                    data=data,
                                    format='json')
        self.assertEquals(response.status_code,
                          status.HTTP_201_CREATED)
        self.assertEquals(Input.objects.count(),
                          1)

        test_input = Input.objects.first()
        self.assertEquals(test_input.time_step,
                          data['time_step'])
        self.assertEquals(test_input.yshade,
                          data['yshade'])

    def test_get_input_list(self):
        test_input = Input(time_step=self.test_test_step,
                           yshade=1.0)
        test_input.save()

        response = self.client.get(self.url)
        response_json = response.json()

        self.assertEquals(response.status_code,
                          status.HTTP_200_OK)

        self.assertEquals(len(response_json),
                          1)

        data = response_json[0]
        self.assertEquals(data['time_step'],
                          test_input.time_step)
        self.assertEquals(data['yshade'],
                          test_input.yshade)


class OutputCreateAPIView(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('api-output-list')
        self.test_user = User(name='test_user4',
                              email='testuser4@test.com',
                              password='test user4 88')
        self.test_test_step = Timestep(user=self.test_user,
                                       time_step=600)

    def test_create_output(self):
        self.assertEquals(
            Output.objects.count(),
            0
        )

        data = {
            'time_step': self.test_test_step,
            'yshade': 1.0,
            'dry_bulb': 1.2,
            'troo': 1.5,
            'isolext': 1.6,
            'sout': 1.7,
            'zonesens': 1.8,
            'cool_rate': 1.9
        }
        response = self.client.post(self.url,
                                    data=data,
                                    format='json')
        self.assertEquals(response.status_code,
                          status.HTTP_201_CREATED)
        self.assertEquals(Input.objects.count(),
                          1)

        test_input = Output.objects.first()
        self.assertEquals(test_input.time_step,
                          data['time_step'])
        self.assertEquals(test_input.yshade,
                          data['yshade'])
        self.assertEquals(test_input.yshade,
                          data['dry_bulb'])
        self.assertEquals(test_input.yshade,
                          data['troo'])
        self.assertEquals(test_input.yshade,
                          data['isolext'])
        self.assertEquals(test_input.yshade,
                          data['sout'])
        self.assertEquals(test_input.yshade,
                          data['zonesens'])
        self.assertEquals(test_input.yshade,
                          data['cool_rate'])

    def test_get_output_list(self):
        test_output = Output(time_step=self.test_test_step,
                             yshade=1.0,
                             dry_bulb=1.2,
                             troo=1.5,
                             isolext=1.6,
                             sout=1.7,
                             zonesens=1.8,
                             cool_rate=1.9)
        test_output.save()

        response = self.client.get(self.url)
        response_json = response.json()

        self.assertEquals(response.status_code,
                          status.HTTP_200_OK)

        self.assertEquals(len(response_json),
                          1)

        data = response_json[0]
        self.assertEquals(data['time_step'],
                          test_output.time_step)
        self.assertEquals(data['yshade'],
                          test_output.yshade)
        self.assertEquals(data['dry_bulb'],
                          test_output.dry_bulb)
        self.assertEquals(data['troo'],
                          test_output.troo)
        self.assertEquals(data['isolext'],
                          test_output.isolext)
        self.assertEquals(data['sout'],
                          test_output.sout)
        self.assertEquals(data['zonsens'],
                          test_output.zonesens)
        self.assertEquals(data['cool_rate'],
                          test_output.cool_rate)


