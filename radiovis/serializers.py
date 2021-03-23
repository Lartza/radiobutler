from io import BytesIO

from rest_framework import serializers
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile

from .models import ImageSlide


def resave_png(image_data):
    # Resave PNG files to simplify and (hopefully) increase compatibility
    image = Image.open(image_data)
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    return InMemoryUploadedFile(buffer, image_data.field_name, image_data.name, image_data.content_type, image.size,
                                image_data.charset)


class ImageSlideSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ImageSlide
        fields = '__all__'

    def create(self, validated_data):
        if validated_data['image'].content_type == 'image/png':
            validated_data['image'] = resave_png(validated_data['image'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data['image'].content_type == 'image/png':
            validated_data['image'] = resave_png(validated_data['image'])
        return super().update(instance, validated_data)
