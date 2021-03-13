from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r'services', views.ServiceViewSet)
router.register(r'bearers', views.BearerViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/helloworld/', views.HelloWorld.as_view()),
    path('radiodns/spi/3.1/SI.xml', views.service_information, name='service_information'),
]
