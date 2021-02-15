from django.db import models


class Service(models.Model):
    short_name = models.CharField(max_length=8)
    medium_name = models.CharField(max_length=16)

    def __str__(self):
        return self.short_name


class Bearer(models.Model):
    bearer_id = models.TextField()
    service = models.ForeignKey(Service, related_name='bearers', on_delete=models.CASCADE)
    cost = models.IntegerField()
    mimeValue = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.bearer_id
