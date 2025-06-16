from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('aeroport-list', views.aeroport_list, name="aeroport_list")
]
