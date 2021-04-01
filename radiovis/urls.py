from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r'imageslides', views.ImageSlideViewSet)
router.register(r'textslides', views.TextSlideViewSet)
router.register(r'images', views.ImageViewSet)
