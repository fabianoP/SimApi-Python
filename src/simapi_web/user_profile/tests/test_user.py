from django.test import TestCase
from user_profile.models import User

# Create your tests here.


class UserTestCase(TestCase):

    def test_user(self):
        User.objects.create(name='test_user',
                            email='testuser@test.com',
                            password='test user 88')

        self.assertEquals(User.objects.count(),
                          1)
