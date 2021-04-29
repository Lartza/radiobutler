from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Service, Bearer


class ServiceTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='asdf@asdf.com')

    def test_post_service(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('service-list'),
                                    {'shortName': 'Testi', 'mediumName': 'Testikanava', 'fqdn': 'radiodns.test',
                                     'serviceIdentifier': 'testservice'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Service.objects.count(), 1)
        service = Service.objects.get()
        self.assertEqual(service.shortName, 'Testi')
        self.assertEqual(service.mediumName, 'Testikanava')

    def test_put_service(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('service-list'),
                                    {'shortName': 'Testi', 'mediumName': 'Testikanava', 'fqdn': 'radiodns.test',
                                     'serviceIdentifier': 'testservice'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.put(response.json()['apiurl'],
                                   {'shortName': 'Testi2', 'mediumName': 'Testikanava2', 'fqdn': 'radiodns.test',
                                    'serviceIdentifier': 'testservice'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Service.objects.count(), 1)
        service = Service.objects.get()
        self.assertEqual(service.shortName, 'Testi2')

    def test_patch_service(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('service-list'),
                                    {'shortName': 'Testi', 'mediumName': 'Testikanava', 'fqdn': 'radiodns.test',
                                     'serviceIdentifier': 'testservice'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.patch(response.json()['apiurl'], {'shortDescription': 'Lorem ipsum'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Service.objects.count(), 1)
        service = Service.objects.get()
        self.assertEqual(service.shortDescription, 'Lorem ipsum')

    def test_post_nested_bearer(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('service-list'),
                                    {'shortName': 'Testi', 'mediumName': 'Testikanava', 'fqdn': 'radiodns.test',
                                     'serviceIdentifier': 'testservice', 'bearers[0][platform]': "fm",
                                     "bearers[0][ecc]": "00", "bearers[0][pi]": "test", "bearers[0][frequency]": 7.7})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Bearer.objects.count(), 1)

    def test_put_nested_bearer(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('service-list'),
                                    {'shortName': 'Testi', 'mediumName': 'Testikanava', 'fqdn': 'radiodns.test',
                                     'serviceIdentifier': 'testservice', 'bearers[0][platform]': "fm",
                                     "bearers[0][ecc]": "00", "bearers[0][pi]": "test", "bearers[0][frequency]": 7.7})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        service_apiurl = response.json()['apiurl']
        response = self.client.put(service_apiurl,
                                   {'shortName': 'Testi', 'mediumName': 'Testikanava', 'fqdn': 'radiodns.test',
                                    'serviceIdentifier': 'testservice', 'bearers[0][platform]': "fm",
                                    "bearers[0][ecc]": "g1", "bearers[0][pi]": "test", "bearers[0][frequency]": 7.7})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Bearer.objects.count(), 1)
        response = self.client.put(service_apiurl,
                                   {'shortName': 'Testi', 'mediumName': 'Testikanava', 'fqdn': 'radiodns.test',
                                    'serviceIdentifier': 'testservice', 'bearers[0][platform]': "fm",
                                    "bearers[0][ecc]": "g1", "bearers[0][pi]": "test", "bearers[0][frequency]": 7.7,
                                    "bearers[0][apiurl]": reverse('bearer-detail', args=[1])})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Bearer.objects.count(), 1)

    def test_service_str(self):
        Service.objects.create(shortName='Testi')
        service = Service.objects.get()
        self.assertEqual(str(service), service.shortName)


class BearerTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='asdf@asdf.com')
        self.service = Service.objects.create(shortName='Testi')

    def test_post_bearer(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('bearer-list'), {'platform': 'fm', 'ecc': '00', 'pi': 'TEST',
                                                             'frequency': 7.7,
                                                             'service': reverse('service-detail',
                                                                                args=[self.service.id]),
                                                             'cost': 50})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        bearer_id = response.json()['id']

        response = self.client.post(reverse('bearer-list'), {'platform': 'ip', 'url': 'https://test',
                                                             'mimeValue': 'audio/mp3',
                                                             'service': reverse('service-detail',
                                                                                args=[self.service.id]),
                                                             'cost': 30})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Bearer.objects.count(), 2)
        bearer = Bearer.objects.get(pk=bearer_id)
        self.assertEqual(bearer.pi, 'test')

    def test_put_bearer(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('bearer-list'), {'platform': 'fm', 'ecc': '00', 'pi': 'test',
                                                             'frequency': 7.7,
                                                             'service': reverse('service-detail',
                                                                                args=[self.service.id]),
                                                             'cost': 50})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(reverse('bearer-list'), {'platform': 'ip', 'url': 'https://test',
                                                             'mimeValue': 'audio/mp3',
                                                             'service': reverse('service-detail',
                                                                                args=[self.service.id]),
                                                             'cost': 30})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.put(reverse('bearer-detail', args=[1]),
                                   {'platform': 'fm', 'ecc': '00', 'pi': 'TEST',
                                    'frequency': 8.7,
                                    'service': reverse('service-detail', args=[self.service.id]),
                                    'cost': 50})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put(reverse('bearer-detail', args=[2]),
                                   {'platform': 'ip', 'url': 'https://test2',
                                    'mimeValue': 'audio/mp3',
                                    'service': reverse('service-detail', args=[self.service.id]),
                                    'cost': 30})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Bearer.objects.count(), 2)
        bearer = Bearer.objects.get(pk=1)
        self.assertEqual(bearer.frequency, 8.7)
        self.assertEqual(bearer.pi, 'test')

    def test_patch_bearer(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('bearer-list'), {'platform': 'fm', 'ecc': '00', 'pi': 'test',
                                                             'frequency': 7.7,
                                                             'service': reverse('service-detail',
                                                                                args=[self.service.id]),
                                                             'cost': 50})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.patch(reverse('bearer-detail', args=[response.json()['id']]), {'ecc': 'G1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Bearer.objects.count(), 1)
        bearer = Bearer.objects.get()
        self.assertEqual(bearer.ecc, 'g1')
        self.assertEqual(bearer.pi, 'test')

    def test_validate(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('bearer-list'), {'platform': 'fm', 'pi': 'test',
                                                             'frequency': 7.7,
                                                             'service': reverse('service-detail',
                                                                                args=[self.service.id])})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(reverse('bearer-list'), {'platform': 'fm', 'ecc': '00',
                                                             'frequency': 7.7,
                                                             'service': reverse('service-detail',
                                                                                args=[self.service.id])})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(reverse('bearer-list'), {'platform': 'fm', 'ecc': '00', 'pi': 'test',
                                                             'service': reverse('service-detail',
                                                                                args=[self.service.id])})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(reverse('bearer-list'), {'platform': 'ip',
                                                             'mimeValue': 'audio/mp3',
                                                             'service': reverse('service-detail',
                                                                                args=[self.service.id])})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(reverse('bearer-list'), {'platform': 'ip', 'url': 'https://test',
                                                             'service': reverse('service-detail',
                                                                                args=[self.service.id])})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bearer_str(self):
        Bearer.objects.create(platform='fm', ecc='00', pi='test', frequency=7.7, service_id=self.service.id, cost=50)
        Bearer.objects.create(platform='ip', url='https://example.com/teststream.mp3', mimeValue='audio/mp3',
                              bitrate=128, service_id=self.service.id, cost=30)
        bearer = Bearer.objects.get(pk=1)
        self.assertEqual(str(bearer), f'{bearer.platform} {bearer.ecc} {bearer.pi} {bearer.frequency} {bearer.cost}')
        bearer = Bearer.objects.get(pk=2)
        self.assertEqual(str(bearer),
                         f'{bearer.platform} {bearer.url} {bearer.mimeValue} {bearer.bitrate} {bearer.cost}')


class ServiceInformationTest(APITestCase):
    def test_service_information(self):
        service = Service.objects.create(shortName='Testi', mediumName='Testikanava', fqdn='test.test.tld',
                                         serviceIdentifier='testidentifier')
        Bearer.objects.create(platform='fm', ecc='00', pi='test', frequency=7.7, service_id=1, cost=50)
        Bearer.objects.create(platform='ip', url='https://test.test.tld/teststream.mp3', mimeValue='audio/mp3',
                              bitrate=128, service_id=service.id, cost=20)
        response = self.client.get(reverse('service_information'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
