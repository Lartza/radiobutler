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

from django.db import models


class Image(models.Model):
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f'{self.image}'


class ImageSlide(models.Model):
    trigger_time = models.DateTimeField(null=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    link = models.CharField(max_length=512, blank=True)
    sent = models.DateTimeField(null=True, editable=False)

    def __str__(self):
        return str(self.sent)


class TextSlide(models.Model):
    message = models.CharField(max_length=128, default='')
    sent = models.DateTimeField(null=True, editable=False)

    def __str__(self):
        return f'{self.sent}, "{self.message}"'
