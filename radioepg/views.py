from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions

from .models import Service, Bearer
from .serializers import ServiceSerializer, BearerSerializer


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
