from faker import Faker
from rest_framework.test import APITestCase, APIClient

from applications.user.models import User

fake = Faker()


class BaseAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username=fake.user_name(), password='<PASSWORD>')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
