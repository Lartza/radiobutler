from django.db import models


class ImageSlide(models.Model):
    trigger_time = models.DateTimeField(null=True)
    image = models.ImageField(upload_to='slides/')
    sent = models.BooleanField()
