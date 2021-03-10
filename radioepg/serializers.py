from rest_framework import serializers

from .models import Service, Bearer, ImageSlide


class BearerSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Bearer
        fields = '__all__'
        extra_kwargs: dict = {
            'bearer_id': {
                'validators': [],
            }
        }


class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    bearers = BearerSerializer(many=True, required=False, allow_null=True)

    def create(self, validated_data):
        bearers_data = []
        try:
            bearers_data = validated_data.pop('bearers')
        except KeyError:
            pass
        service = Service.objects.create(**validated_data)
        for bearer in bearers_data:
            Bearer.objects.create(service=service, **bearer)
        return service

    def update(self, instance, validated_data):
        bearers_data = []
        try:
            bearers_data = validated_data.pop('bearers')
        except KeyError:
            pass
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()

        if self.context['request'].method != 'PATCH':
            removable = Bearer.objects.filter(service=instance)

        for bearer_data in bearers_data:
            try:
                bearer = Bearer.objects.get(pk=bearer_data['id'])
            except KeyError:
                try:
                    bearer = Bearer.objects.get(bearer_id=bearer_data['bearer_id'])
                except Bearer.DoesNotExist:
                    bearer = None

            if bearer:
                for k, v in bearer_data.items():
                    setattr(bearer, k, v)
                bearer.save()
            else:
                bearer = Bearer.objects.create(**bearer_data)

            if self.context['request'].method != 'PATCH':
                removable = removable.exclude(pk=bearer.pk)

        if self.context['request'].method != 'PATCH':
            removable.delete()
        return instance

    class Meta:
        model = Service
        fields = '__all__'


class ImageSlideSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ImageSlide
        fields = '__all__'
