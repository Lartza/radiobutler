from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Service, Bearer


class ServiceTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='asdf@asdf.com',  # nosec
                                             password='testpassword')

    def test_create_service(self):
        self.client.login(username='testuser', password='testpassword')  # nosec
        response = self.client.post(reverse('service-list'),
                                    {'short_name': 'Testi', 'medium_name': 'Testikanava', 'fqdn': 'radiodns.test',
                                     'service_identifier': 'testservice'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.logout()

        self.assertEqual(Service.objects.count(), 1)
        service = Service.objects.get()
        self.assertEqual(service.short_name, 'Testi')
        self.assertEqual(service.medium_name, 'Testikanava')

    def test_service_str(self):
        Service.objects.create(short_name='Testi')
        service = Service.objects.get()
        self.assertEqual(str(service), service.short_name)


class BearerTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='asdf@asdf.com',  # nosec
                                             password='testpassword')
        Service.objects.create(short_name='Testi')

    def test_create_bearer(self):
        self.client.login(username='testuser', password='testpassword')  # nosec
        response = self.client.post(reverse('bearer-list'), {'bearer_id': 'fm:test',
                                                             'service': reverse('service-detail', args=[1]),
                                                             'cost': 50})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.logout()

        self.assertEqual(Bearer.objects.count(), 1)

    def test_bearer_str(self):
        Bearer.objects.create(bearer_id='fm:test', service_id=1, cost=50)
        bearer = Bearer.objects.get()
        self.assertEqual(str(bearer), bearer.bearer_id)


class ServiceInformationTest(APITestCase):
    def test_service_information(self):
        response = self.client.get(reverse('service_information'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
