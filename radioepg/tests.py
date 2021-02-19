from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User

from .models import Service


class ServiceTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='asdf@asdf.com', password='testpassword')

    def test_create_service(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/api/services/',
                                    {'short_name': 'Testi', 'medium_name': 'Testikanava', 'fqdn': 'radiodns.test',
                                     'service_identifier': 'testservice'})
        self.assertEqual(response.status_code, 201)
        self.client.logout()

        service = Service.objects.get(id=1)
        self.assertEqual(service.short_name, 'Testi')
        self.assertEqual(service.medium_name, 'Testikanava')
