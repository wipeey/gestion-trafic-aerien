from django.urls import path
from . import views

urlpatterns = [
    # Index
    path('', views.index, name="index"),
    
    # ===== AEROPORT URLS =====
    path('aeroport/liste', views.aeroport_list, name="aeroport_list"),
    path('aeroport/creer/', views.aeroport_create, name="aeroport_create"),
    path('aeroport/<int:pk>/modifier/', views.aeroport_edit, name="aeroport_edit"),
    path('aeroport/<int:pk>/supprimer/', views.aeroport_delete, name="aeroport_delete"),
    
    # ===== PISTE URLS =====
    path('piste/liste', views.piste_list, name="piste_list"),
    path('piste/creer/', views.piste_create, name="piste_create"),
    path('piste/<int:pk>/modifier/', views.piste_edit, name="piste_edit"),
    path('piste/<int:pk>/supprimer/', views.piste_delete, name="piste_delete"),
    
    # ===== COMPAGNIE URLS =====
    path('compagnie/liste', views.compagnie_list, name="compagnie_list"),
    path('compagnie/creer/', views.compagnie_create, name="compagnie_create"),
    path('compagnie/<int:pk>/modifier/', views.compagnie_edit, name="compagnie_edit"),
    path('compagnie/<int:pk>/supprimer/', views.compagnie_delete, name="compagnie_delete"),
    
    # ===== TYPE AVION URLS =====
    path('typeavion/liste', views.type_avion_list, name="type_avion_list"),
    path('typeavion/creer/', views.type_avion_create, name="type_avion_create"),
    path('typeavion/<int:pk>/modifier/', views.type_avion_edit, name="type_avion_edit"),
    path('typeavion/<int:pk>/supprimer/', views.type_avion_delete, name="type_avion_delete"),
    
    # ===== AVION URLS =====
    path('avion/liste', views.avion_list, name="avion_list"),
    path('avion/creer/', views.avion_create, name="avion_create"),
    path('avion/<int:pk>/modifier/', views.avion_edit, name="avion_edit"),
    path('avion/<int:pk>/supprimer/', views.avion_delete, name="avion_delete"),
    
    # ===== VOL URLS =====
    path('vol/liste', views.vol_list, name="vol_list"),
    path('vol/creer/', views.vol_create, name="vol_create"),
    path('vol/importer/', views.vol_import, name="vol_import"),
    path('vol/<int:pk>/modifier/', views.vol_edit, name="vol_edit"),
    path('vol/<int:pk>/supprimer/', views.vol_delete, name="vol_delete"),
]