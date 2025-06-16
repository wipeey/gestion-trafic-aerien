from django.shortcuts import render
from .models import Aeroport, Avion, Compagnie, Piste, TypeAvion, Vol

def index(request):
    return render(request, 'trafic_aerien/index.html')

def aeroport_list(request):
    aeroports = Aeroport.objects.all()
    return render(request, 'trafic_aerien/aeroport/list.html', {'aeroports': aeroports})

def avion_list(request):
    avions = Avion.objects.all()
    return render(request, 'trafic_aerien/avion/list.html', {'avions': avions})

def compagnie_list(request):
    compagnies = Compagnie.objects.all()
    return render(request, 'trafic_aerien/compagnie/list.html', {'compagnies': compagnies})

def piste_list(request):
    pistes = Piste.objects.all()
    return render(request, 'trafic_aerien/piste/list.html', {'pistes': pistes})

def type_avion_list(request):
    types_avion = TypeAvion.objects.all()
    return render(request, 'trafic_aerien/typeavion/list.html', {'types_avion': types_avion})

def vol_list(request):
    vols = (
        Vol.objects
           .select_related('avion', 'aeroport_depart', 'aeroport_arrivee')
           .all()
    )
    return render(request, 'trafic_aerien/vol/list.html', {
        'vols': vols,
    })
