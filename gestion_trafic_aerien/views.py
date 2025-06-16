from django.shortcuts import render
from .models import Aeroport

def index(request):
    return render(request, 'trafic_aerien/index.html')

def aeroport_list(request):
    aeroports = Aeroport.objects.all()
    return render(request, 'trafic_aerien/aeroport/list.html', {'aeroports': aeroports})