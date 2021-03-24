from rest_framework import serializers

from .models import Service, Bearer


class BearerSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Bearer
        fields = '__all__'

    def create(self, validated_data):
        validated_data['ecc'] = validated_data['ecc'].lower()
        validated_data['pi'] = validated_data['pi'].lower()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['ecc'] = validated_data['ecc'].lower()
        validated_data['pi'] = validated_data['pi'].lower()
        return super().update(instance, validated_data)

    def validate(self, attrs):
        if attrs['platform'] == 'fm':
            if attrs['ecc'] == '':
                raise serializers.ValidationError({'ecc': 'ECC is required for FM bearers'})
            if attrs['pi'] == '':
                raise serializers.ValidationError({'pi': 'PI is required for FM bearers'})
            if attrs['frequency'] == '':
                raise serializers.ValidationError({'frequency': 'Frequency is required for FM bearers'})
        if attrs['platform'] == 'ip':
            if attrs['url'] == '':
                raise serializers.ValidationError({'url': 'URL is required for IP bearers'})
            if attrs['mimeValue'] == '':
                raise serializers.ValidationError({'url': 'mimeValue is required for IP bearers'})
        return attrs


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
            # Match bearer for update based on primary key or details
            try:
                bearer = Bearer.objects.get(pk=bearer_data['id'])
            except (Bearer.DoesNotExist, KeyError):
                try:
                    bearer = Bearer.objects.get(platform=bearer_data['platform'], ecc=bearer_data['ecc'],
                                                pi=bearer_data['pi'])
                except (Bearer.DoesNotExist, KeyError):
                    try:
                        bearer = Bearer.objects.get(platform=bearer_data['platform'], ecc=bearer_data['url'])
                    except (Bearer.DoesNotExist, KeyError):
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
