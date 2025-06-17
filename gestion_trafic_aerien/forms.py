from django import forms
from .models import Aeroport, Piste, Compagnie, TypeAvion, Avion, Vol


class AeroportForm(forms.ModelForm):
    class Meta:
        model = Aeroport
        fields = ['nom', 'pays']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Charles de Gaulle, Orly, JFK...',
                'maxlength': 100
            }),
            'pays': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: France, États-Unis, Allemagne...',
                'maxlength': 100
            }),
        }
        labels = {
            'nom': 'Nom de l\'aéroport',
            'pays': 'Pays',
        }


class PisteForm(forms.ModelForm):
    class Meta:
        model = Piste
        fields = ['numero', 'aeroport', 'longueur']
        widgets = {
            'numero': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 1, 2, 09, 27...',
                'min': 1
            }),
            'aeroport': forms.Select(attrs={
                'class': 'form-select'
            }),
            'longueur': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Longueur en mètres (ex: 3500)',
                'min': 500,
                'step': 10
            }),
        }
        labels = {
            'numero': 'Numéro de piste',
            'aeroport': 'Aéroport',
            'longueur': 'Longueur (m)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['aeroport'].queryset = Aeroport.objects.all().order_by('nom')
        self.fields['aeroport'].empty_label = "Sélectionner un aéroport"


class CompagnieForm(forms.ModelForm):
    class Meta:
        model = Compagnie
        fields = ['nom', 'description', 'pays_rattachement']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Air France, Lufthansa, Emirates...',
                'maxlength': 100
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Description de la compagnie aérienne...',
                'rows': 4
            }),
            'pays_rattachement': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: France, Allemagne, Émirats Arabes Unis...',
                'maxlength': 100
            }),
        }
        labels = {
            'nom': 'Nom de la compagnie',
            'description': 'Description',
            'pays_rattachement': 'Pays de rattachement',
        }


class TypeAvionForm(forms.ModelForm):
    class Meta:
        model = TypeAvion
        fields = ['marque', 'modele', 'description', 'image', 'longueur_piste_necessaire']
        widgets = {
            'marque': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Boeing, Airbus, Embraer...',
                'maxlength': 100
            }),
            'modele': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 747-400, A380, E-Jets...',
                'maxlength': 100
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Caractéristiques techniques, capacité, etc...',
                'rows': 4
            }),
            'image': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de l\'image (ex: plane.jpg)'
            }),
            'longueur_piste_necessaire': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Longueur minimale en mètres (ex: 2500)',
                'min': 500,
                'step': 10
            }),
        }
        labels = {
            'marque': 'Marque',
            'modele': 'Modèle',
            'description': 'Description',
            'image': 'Image (URL)',
            'longueur_piste_necessaire': 'Longueur de piste nécessaire (m)',
        }


class AvionForm(forms.ModelForm):
    class Meta:
        model = Avion
        fields = ['nom', 'compagnie', 'type_avion']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: F-GSQA, N747BA, G-BOAC...',
                'maxlength': 100
            }),
            'compagnie': forms.Select(attrs={
                'class': 'form-select'
            }),
            'type_avion': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        labels = {
            'nom': 'Nom/Immatriculation',
            'compagnie': 'Compagnie',
            'type_avion': 'Type d\'avion',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['compagnie'].queryset = Compagnie.objects.all().order_by('nom')
        self.fields['compagnie'].empty_label = "Sélectionner une compagnie"
        self.fields['type_avion'].queryset = TypeAvion.objects.all().order_by('marque', 'modele')
        self.fields['type_avion'].empty_label = "Sélectionner un type d'avion"


class VolForm(forms.ModelForm):
    class Meta:
        model = Vol
        fields = [
            'avion', 'pilote', 'aeroport_depart', 'date_heure_depart',
            'aeroport_arrivee', 'date_heure_arrivee'
        ]
        widgets = {
            'avion': forms.Select(attrs={
                'class': 'form-select'
            }),
            'pilote': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Capitaine Dupont, Jean Martin...',
                'maxlength': 100
            }),
            'aeroport_depart': forms.Select(attrs={
                'class': 'form-select'
            }),
            'date_heure_depart': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'placeholder': 'YYYY-MM-DD HH:MM'
            }),
            'aeroport_arrivee': forms.Select(attrs={
                'class': 'form-select'
            }),
            'date_heure_arrivee': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'placeholder': 'YYYY-MM-DD HH:MM'
            }),
        }
        labels = {
            'avion': 'Avion',
            'pilote': 'Pilote',
            'aeroport_depart': 'Aéroport de départ',
            'date_heure_depart': 'Date et heure de départ',
            'aeroport_arrivee': 'Aéroport d\'arrivée',
            'date_heure_arrivee': 'Date et heure d\'arrivée',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avion'].queryset = Avion.objects.select_related('compagnie', 'type_avion').order_by('nom')
        self.fields['avion'].empty_label = "Sélectionner un avion"
        
        aeroports = Aeroport.objects.all().order_by('nom')
        self.fields['aeroport_depart'].queryset = aeroports
        self.fields['aeroport_depart'].empty_label = "Sélectionner l'aéroport de départ"
        self.fields['aeroport_arrivee'].queryset = aeroports
        self.fields['aeroport_arrivee'].empty_label = "Sélectionner l'aéroport d'arrivée"

    def clean(self):
        cleaned_data = super().clean()
        aeroport_depart = cleaned_data.get('aeroport_depart')
        aeroport_arrivee = cleaned_data.get('aeroport_arrivee')
        date_heure_depart = cleaned_data.get('date_heure_depart')
        date_heure_arrivee = cleaned_data.get('date_heure_arrivee')
        avion = cleaned_data.get('avion')

        # Vérifier que les aéroports de départ et d'arrivée sont différents
        if aeroport_depart and aeroport_arrivee and aeroport_depart == aeroport_arrivee:
            raise forms.ValidationError(
                "L'aéroport de départ et d'arrivée ne peuvent pas être identiques."
            )

        # Vérifier que la date d'arrivée est postérieure à la date de départ
        if date_heure_depart and date_heure_arrivee:
            if date_heure_arrivee <= date_heure_depart:
                raise forms.ValidationError(
                    "La date et heure d'arrivée doivent être postérieures à celles de départ."
                )

        # Vérifier que l'avion peut utiliser la piste de l'aéroport de départ
        if avion and aeroport_depart:
            pistes_adequates = aeroport_depart.pistes.filter(
                longueur__gte=avion.type_avion.longueur_piste_necessaire
            )
            if not pistes_adequates.exists():
                raise forms.ValidationError(
                    f"Aucune piste de l'aéroport {aeroport_depart.nom} n'est assez longue "
                    f"pour ce type d'avion (minimum requis: {avion.type_avion.longueur_piste_necessaire}m)."
                )

        return cleaned_data


# Formulaires de recherche/filtrage
class VolSearchForm(forms.Form):
    aeroport_depart = forms.ModelChoiceField(
        queryset=Aeroport.objects.all().order_by('nom'),
        required=False,
        empty_label="Tous les aéroports de départ",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    aeroport_arrivee = forms.ModelChoiceField(
        queryset=Aeroport.objects.all().order_by('nom'),
        required=False,
        empty_label="Tous les aéroports d'arrivée",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    compagnie = forms.ModelChoiceField(
        queryset=Compagnie.objects.all().order_by('nom'),
        required=False,
        empty_label="Toutes les compagnies",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date_debut = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label="À partir du"
    )
    date_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label="Jusqu'au"
    )