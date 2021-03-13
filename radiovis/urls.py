from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r'imageslides', views.ImageSlideViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
