from rest_framework import serializers

from .models import ImageSlide, TextSlide, Image


class ImageSlideSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ImageSlide
        fields = '__all__'


class TextSlideSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TextSlide
        fields = '__all__'


class ImageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Image
        fields = ('apiurl', 'image')
