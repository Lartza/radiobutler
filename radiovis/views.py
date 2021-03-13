# import pika

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ImageSlide
from .serializers import ImageSlideSerializer


class ImageSlideViewSet(viewsets.ModelViewSet):
    queryset = ImageSlide.objects.all()
    serializer_class = ImageSlideSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True)
    def send(self, request, pk=None):
        slide = self.get_object()
        if slide.trigger_time:
            trigger_time = slide.trigger_time.isoformat()
        else:
            trigger_time = 'NOW'
#        connection = pika.BlockingConnection(
#            pika.ConnectionParameters(host='localhost'))
#        channel = connection.channel()
#        channel.basic_publish(exchange='amq.topic', routing_key='text',
#                              body=f'SHOW {request.scheme}://{request.META.get('HTTP_HOST')}{slide.image.url}'.encode())
        slide.sent = True
        slide.save()
        return Response(f'UNFINISHED Sent: SHOW {request.scheme}://{request.META.get("HTTP_HOST")}{slide.image.url}'
                        f' trigger-time: {trigger_time}')
