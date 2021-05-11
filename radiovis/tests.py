# Copyright 2021 Radio Moreeni
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import datetime, timezone, timedelta
from unittest.mock import patch
import tempfile
from io import BytesIO

from django.urls import reverse
from django.test import override_settings
from django.contrib.auth.models import User
from django.db.models import ProtectedError
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from PIL import Image as PILImage

from radioepg.models import Service, Bearer
from .models import TextSlide, ImageSlide, Image


def image():
    img = BytesIO()
    PILImage.new('RGB', (100, 100)).save(img, 'PNG')
    img.seek(0)
    data = SimpleUploadedFile('testimage.png', img.getvalue())
    return data


class TextSlideTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='asdf@asdf.com')
        self.client.force_login(self.user)

    def test_textslide_protected_21days(self):
        instance = TextSlide.objects.create(message='Test', sent=datetime.now(timezone.utc) - timedelta(days=1))
        response = self.client.delete(reverse('textslide-detail', args=[instance.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        with self.assertRaises(ProtectedError):
            instance.delete()

    def test_textslide_removal(self):
        instance = TextSlide.objects.create(message='Test', sent=datetime.now(timezone.utc) - timedelta(days=22))
        response = self.client.delete(reverse('textslide-detail', args=[instance.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TextSlide.objects.count(), 0)
        instance = TextSlide.objects.create(message='Test', sent=datetime.now(timezone.utc) - timedelta(days=22))
        instance.delete()
        self.assertEqual(TextSlide.objects.count(), 0)

    @patch('radiovis.views.stomp')
    def test_post_textslide_fm(self, mock_stomp):
        service = Service.objects.create(shortName='Testi')
        Bearer.objects.create(platform='fm', ecc='00', pi='TEST', frequency=7.7, service=service, cost=50)
        response = self.client.post(reverse('textslide-list'), {'message': 'Testmessage'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_stomp.Connection().send.assert_called_with(body='TEXT Testmessage',
                                                        destination='/topic/fm/T00/TEST/00770/text')

    @patch('radiovis.views.stomp')
    def test_post_textslide_ip(self, mock_stomp):
        service = Service.objects.create(shortName='Testi', serviceIdentifier='testidentifier')
        Bearer.objects.create(platform='ip', url='https://example.com/teststream.mp3', mimeValue='audio/mp3',
                              bitrate=128, service=service, cost=30)
        response = self.client.post(reverse('textslide-list'), {'message': 'Testmessage'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_stomp.Connection().send.assert_called_with(body='TEXT Testmessage',
                                                        destination='/topic/testidentifier/text')


class ImageTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='asdf@asdf.com')
        self.client.force_login(self.user)

    @override_settings(MEDIA_ROOT=tempfile.TemporaryDirectory(prefix='mediatest').name)
    def test_image_protected_21days(self):
        instance = Image.objects.create(image=image())
        ImageSlide.objects.create(image=instance, sent=datetime.now(timezone.utc) - timedelta(days=1))
        response = self.client.delete(reverse('image-detail', args=[instance.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # with self.assertRaises(ProtectedError):
        #     instance.delete()

    @override_settings(MEDIA_ROOT=tempfile.TemporaryDirectory(prefix='mediatest').name)
    def test_post_image(self):
        response = self.client.post(reverse('image-list'), {'image': image()})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @override_settings(MEDIA_ROOT=tempfile.TemporaryDirectory(prefix='mediatest').name)
    def test_delete_image(self):
        i_instance = Image.objects.create(image=image())
        # Workaround to make sure the test works, Windows only?
        i_instance.image.close()
        response = self.client.delete(reverse('image-detail', args=[i_instance.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @override_settings(MEDIA_ROOT=tempfile.TemporaryDirectory(prefix='mediatest').name)
    def test_str_image(self):
        self.client.post(reverse('image-list'), {'image': image()})
        instance = Image.objects.get(pk=1)
        self.assertIn('testimage.png', str(instance))


class ImageSlideTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='asdf@asdf.com')
        self.client.force_login(self.user)

    @override_settings(MEDIA_ROOT=tempfile.TemporaryDirectory(prefix='mediatest').name)
    def test_imageslide_protected_21days(self):
        instance = ImageSlide.objects.create(image=Image.objects.create(image=image()),
                                             sent=datetime.now(timezone.utc) - timedelta(days=1))
        response = self.client.delete(reverse('imageslide-detail', args=[instance.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        with self.assertRaises(ProtectedError):
            instance.delete()

    @override_settings(MEDIA_ROOT=tempfile.TemporaryDirectory(prefix='mediatest').name)
    def test_imageslide_removal(self):
        instance = ImageSlide.objects.create(image=Image.objects.create(image=image()),
                                             sent=datetime.now(timezone.utc) - timedelta(days=22))
        response = self.client.delete(reverse('imageslide-detail', args=[instance.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ImageSlide.objects.count(), 0)
        instance = ImageSlide.objects.create(image=Image.objects.create(image=image()),
                                             sent=datetime.now(timezone.utc) - timedelta(days=22))
        instance.delete()
        self.assertEqual(ImageSlide.objects.count(), 0)

    @patch('radiovis.views.stomp')
    @override_settings(MEDIA_ROOT=tempfile.TemporaryDirectory(prefix='mediatest').name)
    def test_post_imageslide_fm(self, mock_stomp):
        service = Service.objects.create(shortName='Testi')
        Bearer.objects.create(platform='fm', ecc='00', pi='TEST', frequency=7.7, service=service, cost=50)
        instance = Image.objects.create(image=image())
        response = self.client.post(reverse('imageslide-list'), {'image': reverse('image-detail', args=[instance.id]),
                                                                 'link': 'http://testlink'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_stomp.Connection().send.assert_called_with(body='SHOW http://testserver/media/images/testimage.png',
                                                        headers={'trigger-time': 'NOW', 'link': 'http://testlink'},
                                                        destination='/topic/fm/T00/TEST/00770/image')
        response = self.client.post(reverse('imageslide-list'), {'image': reverse('image-detail', args=[instance.id]),
                                                                 'trigger_time': '2021-05-10 12:00:00+00:00'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_stomp.Connection().send.assert_called_with(body='SHOW http://testserver/media/images/testimage.png',
                                                        headers={'trigger-time': '2021-05-10T12:00:00Z'},
                                                        destination='/topic/fm/T00/TEST/00770/image')

    @patch('radiovis.views.stomp')
    @override_settings(MEDIA_ROOT=tempfile.TemporaryDirectory(prefix='mediatest').name)
    def test_post_imageslide_ip(self, mock_stomp):
        service = Service.objects.create(shortName='Testi', serviceIdentifier='testidentifier')
        Bearer.objects.create(platform='ip', url='https://example.com/teststream.mp3', mimeValue='audio/mp3',
                              bitrate=128, service=service, cost=30)
        instance = Image.objects.create(image=image())
        response = self.client.post(reverse('imageslide-list'),
                                    {'image': reverse('image-detail', args=[instance.id]),
                                     'link': 'http://testlink'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_stomp.Connection().send.assert_called_with(body='SHOW http://testserver/media/images/testimage.png',
                                                        headers={'trigger-time': 'NOW', 'link': 'http://testlink'},
                                                        destination='/topic/testidentifier/image')
        response = self.client.post(reverse('imageslide-list'),
                                    {'image': reverse('image-detail', args=[instance.id]),
                                     'trigger_time': '2021-05-10 12:00:00+00:00'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_stomp.Connection().send.assert_called_with(body='SHOW http://testserver/media/images/testimage.png',
                                                        headers={'trigger-time': '2021-05-10T12:00:00Z'},
                                                        destination='/topic/testidentifier/image')
