from django.db import models


class Image(models.Model):
    image = models.ImageField(upload_to='slides/')


class ImageSlide(models.Model):
    trigger_time = models.DateTimeField(null=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    link = models.CharField(max_length=512, blank=True)
    sent = models.DateTimeField(null=True, editable=False)

    def __str__(self):
        return f'"{self.image}", {self.sent}'


class TextSlide(models.Model):
    message = models.CharField(max_length=128)
    sent = models.DateTimeField(null=True, editable=False)

    def __str__(self):
        return f'"{self.message}", {self.sent}'
