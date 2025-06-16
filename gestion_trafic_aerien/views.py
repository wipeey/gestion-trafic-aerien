from django.shortcuts import render
from .models import Aeroport, Avion

def index(request):
    return render(request, 'trafic_aerien/index.html')

def aeroport_list(request):
    aeroports = Aeroport.objects.all()
    return render(request, 'trafic_aerien/aeroport/list.html', {'aeroports': aeroports})


def avion_list(request):
    avions = Avion.objects.all()
    return render(request, 'trafic_aerien/avion/list.html', {'avions': avions})