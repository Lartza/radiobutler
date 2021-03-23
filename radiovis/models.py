from django.db import models


class ImageSlide(models.Model):
    trigger_time = models.DateTimeField(null=True)
    image = models.ImageField(upload_to='slides/')
    link = models.CharField(max_length=2000, blank=True)
    sent = models.BooleanField()
