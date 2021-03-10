from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'services', views.ServiceViewSet)
router.register(r'bearers', views.BearerViewSet)
router.register(r'imageslides', views.ImageSlideViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/helloworld/', views.HelloWorld.as_view()),
    path('radiodns/spi/3.1/SI.xml', views.service_information, name='service_information'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
