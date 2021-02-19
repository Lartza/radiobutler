from rest_framework import serializers

from .models import Service, Bearer


class BearerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Bearer
        fields = '__all__'


class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    bearers = BearerSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = '__all__'
