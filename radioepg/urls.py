from django.urls import path
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r'services', views.ServiceViewSet)
router.register(r'bearers', views.BearerViewSet)

urlpatterns = [
    path('radiodns/spi/3.1/SI.xml', views.service_information, name='service_information'),
]
