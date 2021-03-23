from django.db import models

from .storage import LogoStorage


class Service(models.Model):
    shortName = models.CharField(max_length=8)
    mediumName = models.CharField(max_length=16)
    shortDescription = models.CharField(max_length=180, blank=True)
    link = models.CharField(max_length=2000, blank=True)
    fqdn = models.CharField(max_length=255)
    serviceIdentifier = models.CharField(max_length=16)
    logo = models.ImageField(upload_to='logos/', storage=LogoStorage(), null=True)

    def __str__(self):
        return self.shortName


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
        if self.platform == 'fm':
            return f'{self.platform} {self.ecc} {self.pi} {self.frequency} {self.cost}'
        return f'{self.platform} {self.url} {self.mimeValue} {self.bitrate} {self.cost}'
