from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Aeroport, Avion, Compagnie, Piste, TypeAvion, Vol
from .forms import (
    AeroportForm, AvionForm, CompagnieForm, PisteForm, 
    TypeAvionForm, VolForm, VolSearchForm
)


def index(request):
    return render(request, 'trafic_aerien/index.html')


# ===== AEROPORT VIEWS =====
def aeroport_list(request):
    aeroports = Aeroport.objects.all().order_by('nom')
    return render(request, 'trafic_aerien/aeroport/list.html', {'aeroports': aeroports})


def aeroport_create(request):
    if request.method == 'POST':
        form = AeroportForm(request.POST)
        if form.is_valid():
            aeroport = form.save()
            return redirect('aeroport_list')
    else:
        form = AeroportForm()
    
    return render(request, 'trafic_aerien/aeroport/form.html', {
        'form': form,
        'title': 'Créer un aéroport'
    })


def aeroport_edit(request, pk):
    aeroport = get_object_or_404(Aeroport, pk=pk)
    
    if request.method == 'POST':
        form = AeroportForm(request.POST, instance=aeroport)
        if form.is_valid():
            aeroport = form.save()
            return redirect('aeroport_list')
    else:
        form = AeroportForm(instance=aeroport)
    
    return render(request, 'trafic_aerien/aeroport/form.html', {
        'form': form,
        'aeroport': aeroport,
        'title': f'Modifier {aeroport.nom}'
    })


def aeroport_delete(request, pk):
    aeroport = get_object_or_404(Aeroport, pk=pk)    
    aeroport.delete()
    return redirect('aeroport_list')


# ===== PISTE VIEWS =====
def piste_list(request):
    pistes = Piste.objects.select_related('aeroport').all().order_by('aeroport__nom', 'numero')
    return render(request, 'trafic_aerien/piste/list.html', {'pistes': pistes})


def piste_create(request):
    if request.method == 'POST':
        form = PisteForm(request.POST)
        if form.is_valid():
            piste = form.save()
            return redirect('piste_list')
    else:
        form = PisteForm()
    
    return render(request, 'trafic_aerien/piste/form.html', {
        'form': form,
        'title': 'Créer une piste'
    })


def piste_edit(request, pk):
    piste = get_object_or_404(Piste, pk=pk)
    
    if request.method == 'POST':
        form = PisteForm(request.POST, instance=piste)
        if form.is_valid():
            piste = form.save()
            return redirect('piste_list')
    else:
        form = PisteForm(instance=piste)
    
    return render(request, 'trafic_aerien/piste/form.html', {
        'form': form,
        'piste': piste,
        'title': f'Modifier Piste {piste.numero}'
    })


def piste_delete(request, pk):
    piste = get_object_or_404(Piste, pk=pk)
    piste.delete()
    return redirect('piste_list')
    

# ===== COMPAGNIE VIEWS =====
def compagnie_list(request):
    compagnies = Compagnie.objects.all().order_by('nom')
    return render(request, 'trafic_aerien/compagnie/list.html', {'compagnies': compagnies})


def compagnie_create(request):
    if request.method == 'POST':
        form = CompagnieForm(request.POST)
        if form.is_valid():
            compagnie = form.save()
            return redirect('compagnie_list')
    else:
        form = CompagnieForm()
    
    return render(request, 'trafic_aerien/compagnie/form.html', {
        'form': form,
        'title': 'Créer une compagnie'
    })


def compagnie_edit(request, pk):
    compagnie = get_object_or_404(Compagnie, pk=pk)
    
    if request.method == 'POST':
        form = CompagnieForm(request.POST, instance=compagnie)
        if form.is_valid():
            compagnie = form.save()
            return redirect('compagnie_list')
    else:
        form = CompagnieForm(instance=compagnie)
    
    return render(request, 'trafic_aerien/compagnie/form.html', {
        'form': form,
        'compagnie': compagnie,
        'title': f'Modifier {compagnie.nom}'
    })


def compagnie_delete(request, pk):
    compagnie = get_object_or_404(Compagnie, pk=pk)
    compagnie.delete()
    return redirect('compagnie_list')


# ===== TYPE AVION VIEWS =====
def type_avion_list(request):
    types_avion = TypeAvion.objects.all().order_by('marque', 'modele')
    return render(request, 'trafic_aerien/typeavion/list.html', {'types_avion': types_avion})


def type_avion_create(request):
    if request.method == 'POST':
        form = TypeAvionForm(request.POST)
        if form.is_valid():
            type_avion = form.save()
            return redirect('type_avion_list')
    else:
        form = TypeAvionForm()
    
    return render(request, 'trafic_aerien/typeavion/form.html', {
        'form': form,
        'title': 'Créer un type d\'avion'
    })


def type_avion_edit(request, pk):
    type_avion = get_object_or_404(TypeAvion, pk=pk)
    
    if request.method == 'POST':
        form = TypeAvionForm(request.POST, instance=type_avion)
        if form.is_valid():
            type_avion = form.save()
            return redirect('type_avion_list')
    else:
        form = TypeAvionForm(instance=type_avion)
    
    return render(request, 'trafic_aerien/typeavion/form.html', {
        'form': form,
        'type_avion': type_avion,
        'title': f'Modifier {type_avion}'
    })


def type_avion_delete(request, pk):
    type_avion = get_object_or_404(TypeAvion, pk=pk)
    type_avion.delete()
    return redirect('type_avion_list')


# ===== AVION VIEWS =====
def avion_list(request):
    avions = Avion.objects.select_related('compagnie', 'type_avion').all().order_by('nom')
    return render(request, 'trafic_aerien/avion/list.html', {'avions': avions})


def avion_create(request):
    if request.method == 'POST':
        form = AvionForm(request.POST)
        if form.is_valid():
            avion = form.save()
            return redirect('avion_list')
    else:
        form = AvionForm()
    
    return render(request, 'trafic_aerien/avion/form.html', {
        'form': form,
        'title': 'Créer un avion'
    })


def avion_edit(request, pk):
    avion = get_object_or_404(Avion, pk=pk)
    
    if request.method == 'POST':
        form = AvionForm(request.POST, instance=avion)
        if form.is_valid():
            avion = form.save()
            return redirect('avion_list')
    else:
        form = AvionForm(instance=avion)
    
    return render(request, 'trafic_aerien/avion/form.html', {
        'form': form,
        'avion': avion,
        'title': f'Modifier {avion.nom}'
    })


def avion_delete(request, pk):
    avion = get_object_or_404(Avion, pk=pk)
    avion.delete()
    return redirect('avion_list')


# ===== VOL VIEWS =====
def vol_list(request):
    vols = (
        Vol.objects
        .select_related('avion', 'avion__compagnie', 'aeroport_depart', 'aeroport_arrivee')
        .all()
        .order_by('-date_heure_depart')
    )
    
    # Gestion de la recherche
    search_form = VolSearchForm(request.GET)
    if search_form.is_valid():
        if search_form.cleaned_data['aeroport_depart']:
            vols = vols.filter(aeroport_depart=search_form.cleaned_data['aeroport_depart'])
        if search_form.cleaned_data['aeroport_arrivee']:
            vols = vols.filter(aeroport_arrivee=search_form.cleaned_data['aeroport_arrivee'])
        if search_form.cleaned_data['compagnie']:
            vols = vols.filter(avion__compagnie=search_form.cleaned_data['compagnie'])
        if search_form.cleaned_data['date_debut']:
            vols = vols.filter(date_heure_depart__date__gte=search_form.cleaned_data['date_debut'])
        if search_form.cleaned_data['date_fin']:
            vols = vols.filter(date_heure_depart__date__lte=search_form.cleaned_data['date_fin'])
    
    # Pagination
    paginator = Paginator(vols, 20)  # 20 vols par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'trafic_aerien/vol/list.html', {
        'vols': page_obj,
        'search_form': search_form,
        'page_obj': page_obj,
    })


def vol_create(request):
    if request.method == 'POST':
        form = VolForm(request.POST)
        if form.is_valid():
            vol = form.save()
            return redirect('vol_list')
    else:
        form = VolForm()
    
    return render(request, 'trafic_aerien/vol/form.html', {
        'form': form,
        'title': 'Créer un vol'
    })


def vol_edit(request, pk):
    vol = get_object_or_404(Vol, pk=pk)
    
    if request.method == 'POST':
        form = VolForm(request.POST, instance=vol)
        if form.is_valid():
            vol = form.save()
            return redirect('vol_list')
    else:
        form = VolForm(instance=vol)
    
    return render(request, 'trafic_aerien/vol/form.html', {
        'form': form,
        'vol': vol,
        'title': f'Modifier Vol {vol.id}'
    })


def vol_delete(request, pk):
    vol = get_object_or_404(Vol, pk=pk)
    vol.delete()
    return redirect('vol_list')