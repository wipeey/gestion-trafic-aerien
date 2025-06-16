from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('aeroport/liste', views.aeroport_list, name="aeroport_list"),
    path('avion/liste', views.avion_list, name="avion_list"),
    path('compagnie/liste', views.compagnie_list, name="compagnie_list"),
    path('piste/liste', views.piste_list, name="piste_list"),
    path('typeavion/liste', views.type_avion_list, name="type_avion_list"),
    path('vol/liste', views.vol_list, name="vol_list")
]
