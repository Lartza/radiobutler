from rest_framework import serializers

from .models import Service, Bearer


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
        # Create bearers from nested data and associate with the created service
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
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        # If this wasn't a PATCH request, we plan to remove hanging bearers at the end
        if self.context['request'].method != 'PATCH':
            removable = Bearer.objects.filter(service=instance)

        # Update or create bearers from nested data
        for bearer_data in bearers_data:
            # Match bearer for update based on primary key or bearer_id
            try:
                bearer = Bearer.objects.get(pk=bearer_data['id'])
            except KeyError:
                try:
                    bearer = Bearer.objects.get(bearer_id=bearer_data['bearer_id'])
                except Bearer.DoesNotExist:
                    bearer = None

            # If matched, update fields for that bearer, otherwise create a new one
            if bearer:
                for key, value in bearer_data.items():
                    setattr(bearer, key, value)
                bearer.save()
            else:
                bearer = Bearer.objects.create(**bearer_data)

            # Exclude matched or created bearer from removal
            if self.context['request'].method != 'PATCH':
                removable = removable.exclude(pk=bearer.pk)

        # Assume PUT requests to contain full bearer list and remove any old ones that didn't match
        if self.context['request'].method != 'PATCH':
            removable.delete()
        return instance

    class Meta:
        model = Service
        fields = '__all__'
