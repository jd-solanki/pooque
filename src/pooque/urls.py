from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("welcome/", views.welcome),
    path("done/", views.done),
]
