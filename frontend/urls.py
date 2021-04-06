from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('service/', views.service, name='service'),
    path('slideshow/', views.slideshow, name='slideshow'),
    path('gallery/', views.gallery, name='gallery'),
]
