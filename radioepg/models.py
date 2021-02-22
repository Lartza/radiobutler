from django.db import models

from .storage import LogoStorage


class Service(models.Model):
    short_name = models.CharField(max_length=8)
    medium_name = models.CharField(max_length=16)
    short_description = models.CharField(max_length=180, blank=True)
    link = models.CharField(max_length=2000, blank=True)
    fqdn = models.CharField(max_length=255)
    service_identifier = models.CharField(max_length=16)
    logo = models.ImageField(upload_to='logos/', storage=LogoStorage(), null=True)

    def __str__(self):
        return self.short_name


class Bearer(models.Model):
    bearer_id = models.TextField()
    service = models.ForeignKey(Service, related_name='bearers', on_delete=models.CASCADE)
    cost = models.IntegerField()
    mime_value = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.bearer_id
