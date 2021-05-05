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

from io import BytesIO
from django.db import models
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image as PILImage
from radiovis.models import Image


def resize(img, res_x, res_y, service_identifier):
    with BytesIO() as f:
        img = img.resize((res_x, res_y))
        img.save(f, format='PNG')
        f.name = f'{service_identifier}_{res_x}x{res_y}.png'
        f.seek(0)
        return SimpleUploadedFile(f'{service_identifier}_{res_x}x{res_y}.png', f.getvalue())


class Service(models.Model):
    shortName = models.CharField(max_length=8)
    mediumName = models.CharField(max_length=16)
    shortDescription = models.CharField(max_length=180, blank=True)
    link = models.CharField(max_length=2000, blank=True)
    fqdn = models.CharField(max_length=255)
    serviceIdentifier = models.CharField(max_length=16, unique=True)
    logo = models.ForeignKey(Image, on_delete=models.RESTRICT, null=True)
    logo600 = models.ImageField(upload_to='resized_logos/', null=True, editable=False)
    logo320 = models.ImageField(upload_to='resized_logos/', null=True, editable=False)
    logo128 = models.ImageField(upload_to='resized_logos/', null=True, editable=False)
    logo112 = models.ImageField(upload_to='resized_logos/', null=True, editable=False)
    logo32 = models.ImageField(upload_to='resized_logos/', null=True, editable=False)

    def __str__(self):
        """Returns shortName as a string representation for Service."""
        return self.shortName

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.logo:
            img = PILImage.open(self.logo.image)
            self.logo600 = resize(img, 600, 600, self.serviceIdentifier)
            self.logo320 = resize(img, 320, 240, self.serviceIdentifier)
            self.logo128 = resize(img, 128, 128, self.serviceIdentifier)
            self.logo112 = resize(img, 112, 32, self.serviceIdentifier)
            self.logo32 = resize(img, 32, 32, self.serviceIdentifier)
        super().save(force_insert, force_update, using, update_fields)


class Bearer(models.Model):
    platform = models.CharField(max_length=2)
    ecc = models.CharField(max_length=2, blank=True)
    pi = models.CharField(max_length=4, blank=True)
    frequency = models.FloatField(null=True, blank=True)
    url = models.CharField(max_length=2000, blank=True)
    mimeValue = models.CharField(max_length=255, blank=True)
    bitrate = models.IntegerField(null=True, blank=True)
    cost = models.IntegerField(default=30)
    service = models.ForeignKey(Service, related_name='bearers', on_delete=models.CASCADE)

    def __str__(self):
        """Returns a string representation of Bearer based on platform."""
        if self.platform == 'fm':
            return f'{self.platform} {self.ecc} {self.pi} {self.frequency} {self.cost}'
        return f'{self.platform} {self.url} {self.mimeValue} {self.bitrate} {self.cost}'
