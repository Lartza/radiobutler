from django.urls import path
from . import views

urlpatterns = [
    path('api/helloworld/', views.HelloWorld.as_view()),
]
