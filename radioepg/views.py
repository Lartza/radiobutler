#import pika

from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework import permissions

from .models import Service, Bearer, ImageSlide
from .serializers import ServiceSerializer, BearerSerializer, ImageSlideSerializer


class HelloWorld(APIView):
    def get(self, request):
        return Response("Hello World!")


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]


class BearerViewSet(viewsets.ModelViewSet):
    queryset = Bearer.objects.all()
    serializer_class = BearerSerializer
    permission_classes = [permissions.IsAuthenticated]


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


def service_information(request):
    services = Service.objects.all()
    for service in services:
        if service.logo:
            service.logo32url = service.logo.url.replace('.png', '_32.png')
            service.logo112url = service.logo.url.replace('.png', '_112.png')
            service.logo128url = service.logo.url.replace('.png', '_128.png')
            service.logo320url = service.logo.url.replace('.png', '_320.png')
    context = {'services': services}

    return render(request, 'radioepg/SI.xml', context, content_type='text/xml')
