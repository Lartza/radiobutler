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
