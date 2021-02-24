import os
import tempfile
from django.test import override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from PIL import Image

from .models import Service, Bearer


def image():
    img = Image.new('RGB', (600, 600), '#ff0000')
    tmp = tempfile.TemporaryFile(prefix='logo', suffix='.png')
    img.save(tmp, format='PNG')
    tmp.seek(0)
    return tmp


class ServiceTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='asdf@asdf.com')

    @override_settings(MEDIA_ROOT=tempfile.TemporaryDirectory(prefix='mediatest').name)
    def test_post_service(self):
        tmp = image()

        self.client.force_login(self.user)
        response = self.client.post(reverse('service-list'),
                                    {'short_name': 'Testi', 'medium_name': 'Testikanava', 'fqdn': 'radiodns.test',
                                     'service_identifier': 'testservice', 'logo': tmp})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Service.objects.count(), 1)
        service = Service.objects.get()
        self.assertTrue(os.path.exists(service.logo.path.replace('.png', '_32.png')))
        self.assertEqual(service.short_name, 'Testi')
        self.assertEqual(service.medium_name, 'Testikanava')

    @override_settings(MEDIA_ROOT=tempfile.TemporaryDirectory(prefix='mediatest').name)
    def test_put_service(self):
        tmp = image()

        self.client.force_login(self.user)
        response = self.client.post(reverse('service-list'),
                                    {'short_name': 'Testi', 'medium_name': 'Testikanava', 'fqdn': 'radiodns.test',
                                     'service_identifier': 'testservice', 'logo': tmp})
        logo = Service.objects.get().logo
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        tmp.seek(0)
        response = self.client.put(reverse('service-detail', args=[1]),
                                   {'short_name': 'Testi2', 'medium_name': 'Testikanava2', 'fqdn': 'radiodns.test',
                                    'service_identifier': 'testservice', 'logo': tmp})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Service.objects.count(), 1)
        service = Service.objects.get()
        self.assertEqual(service.short_name, 'Testi2')
        self.assertEqual(service.logo, logo)

    def test_patch_service(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('service-list'),
                                    {'short_name': 'Testi', 'medium_name': 'Testikanava', 'fqdn': 'radiodns.test',
                                     'service_identifier': 'testservice'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.patch(reverse('service-detail', args=[1]), {'short_description': 'Lorem ipsum'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Service.objects.count(), 1)
        service = Service.objects.get()
        self.assertEqual(service.short_description, 'Lorem ipsum')

    def test_service_str(self):
        Service.objects.create(short_name='Testi')
        service = Service.objects.get()
        self.assertEqual(str(service), service.short_name)


class BearerTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='asdf@asdf.com')
        Service.objects.create(short_name='Testi')

    def test_create_bearer(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('bearer-list'), {'bearer_id': 'fm:test',
                                                             'service': reverse('service-detail', args=[1]),
                                                             'cost': 50})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Bearer.objects.count(), 1)

    def test_bearer_str(self):
        Bearer.objects.create(bearer_id='fm:test', service_id=1, cost=50)
        bearer = Bearer.objects.get()
        self.assertEqual(str(bearer), bearer.bearer_id)


class ServiceInformationTest(APITestCase):
    def test_service_information(self):
        response = self.client.get(reverse('service_information'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
