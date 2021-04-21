from datetime import datetime, timezone, timedelta
import tempfile

from django.urls import reverse
from django.test import override_settings
from django.contrib.auth.models import User
from django.db.models import ProtectedError
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from PIL import Image as PILImage

from .models import TextSlide, ImageSlide, Image


def image():
    img = PILImage.new('RGB', (600, 600), '#ff0000')
    tmp = tempfile.NamedTemporaryFile(prefix='testimage', suffix='.png')
    img.save(tmp, format='PNG')
    tmp.seek(0)
    return tmp


class TextSlideTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='asdf@asdf.com')
        self.client.force_login(self.user)

    def test_textslide_protected_21days(self):
        instance = TextSlide.objects.create(message='Test', sent=datetime.now(timezone.utc) - timedelta(days=1))
        response = self.client.delete(reverse('textslide-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        with self.assertRaises(ProtectedError):
            instance.delete()

    def test_textslide_removal(self):
        TextSlide.objects.create(message='Test', sent=datetime.now(timezone.utc) - timedelta(days=22))
        response = self.client.delete(reverse('textslide-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TextSlide.objects.count(), 0)
        instance = TextSlide.objects.create(message='Test', sent=datetime.now(timezone.utc) - timedelta(days=22))
        instance.delete()
        self.assertEqual(TextSlide.objects.count(), 0)


class ImageTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='asdf@asdf.com')
        self.client.force_login(self.user)

    @override_settings(MEDIA_ROOT=tempfile.TemporaryDirectory(prefix='mediatest').name)
    def test_image_protected_21days(self):
        tmp = image()
        response = self.client.post(reverse('image-list'), {'image': tmp})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        instance = Image.objects.get(pk=1)
        ImageSlide.objects.create(image=instance, sent=datetime.now(timezone.utc) - timedelta(days=1))
        response = self.client.delete(reverse('image-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @override_settings(MEDIA_ROOT=tempfile.TemporaryDirectory(prefix='mediatest').name)
    def test_post_image(self):
        tmp = image()
        response = self.client.post(reverse('image-list'), {'image': tmp})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # @override_settings(MEDIA_ROOT=tempfile.TemporaryDirectory(prefix='mediatest').name)
    # def test_delete_image(self):
    #     tmp = image()
    #     response = self.client.post(reverse('image-list'), {'image': tmp})
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     response = self.client.delete(reverse('image-detail', args=[1]))
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @override_settings(MEDIA_ROOT=tempfile.TemporaryDirectory(prefix='mediatest').name)
    def test_str_image(self):
        tmp = image()
        self.client.post(reverse('image-list'), {'image': tmp})
        instance = Image.objects.get(pk=1)
        self.assertRegex(str(instance), r'^images\/testimage\S+\.png')


class ImageSlideTest(APITestCase):
    @override_settings(MEDIA_ROOT=tempfile.TemporaryDirectory(prefix='mediatest').name)
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='asdf@asdf.com')
        self.client.force_login(self.user)
        tmp = image()
        self.client.post(reverse('image-list'), {'image': tmp})
        self.image = Image.objects.get(pk=1)

    def test_imageslide_protected_21days(self):
        instance = ImageSlide.objects.create(image=self.image, sent=datetime.now(timezone.utc) - timedelta(days=1))
        response = self.client.delete(reverse('imageslide-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        with self.assertRaises(ProtectedError):
            instance.delete()

    def text_imageslide_removal(self):
        ImageSlide.objects.create(image=self.image, sent=datetime.now(timezone.utc) - timedelta(days=22))
        response = self.client.delete(reverse('imageslide-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ImageSlide.objects.count(), 0)
        instance = ImageSlide.objects.create(image=self.image, sent=datetime.now(timezone.utc) - timedelta(days=22))
        instance.delete()
        self.assertEqual(ImageSlide.objects.count(), 0)
