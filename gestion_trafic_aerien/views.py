from django.shortcuts import render
from .models import Compagnie

# Create your views here.
def index(request):
    compagnies = Compagnie.objects.all()
    return render(request, 'trafic_aerien/index.html',  {'compagnies': compagnies})
