from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('aeroport/liste', views.aeroport_list, name="aeroport_list"),
    path('avion/liste', views.avion_list, name="avion_list")
]
