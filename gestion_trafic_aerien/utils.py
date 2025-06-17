from datetime import datetime, timedelta
from django.db.models import Q
from .models import Vol, Avion, Aeroport

class VolCSVValidator:
    """Classe pour valider les vols du CSV avec la même logique que VolForm"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def is_piste_available(self, aeroport, heure_cible, avion, vols_existants=None, vol_actuel_ligne=None):
        """
        Vérifie si une piste compatible est disponible à l'heure donnée.
        Inclut les vols déjà traités du CSV.
        """
        # Vérifier qu'il y a des pistes compatibles
        pistes_compatibles = aeroport.pistes.filter(
            longueur__gte=avion.type_avion.longueur_piste_necessaire
        )
        
        if not pistes_compatibles.exists():
            return False, None
        
        # Récupérer tous les vols existants en DB le même jour
        date_cible = heure_cible.date()
        vols_db = Vol.objects.filter(
            Q(aeroport_depart=aeroport, date_heure_depart__date=date_cible) |
            Q(aeroport_arrivee=aeroport, date_heure_arrivee__date=date_cible)
        )
        
        # Collecter les occupations des vols en DB
        occupations = []
        for vol in vols_db:
            if vol.aeroport_depart == aeroport:
                debut = vol.date_heure_depart
                fin = debut + timedelta(minutes=10)
                occupations.append((debut, fin))
            
            if vol.aeroport_arrivee == aeroport:
                debut = vol.date_heure_arrivee
                fin = debut + timedelta(minutes=10)
                occupations.append((debut, fin))
        
        # Ajouter les occupations des vols du CSV déjà traités
        if vols_existants:
            for i, vol_data in enumerate(vols_existants):
                if i == vol_actuel_ligne:  # Ne pas se comparer à soi-même
                    continue
                    
                try:
                    avion_csv = Avion.objects.get(id=vol_data['avion_id'])
                    aeroport_depart_csv = Aeroport.objects.get(id=vol_data['aeroport_depart_id'])
                    aeroport_arrivee_csv = Aeroport.objects.get(id=vol_data['aeroport_arrivee_id'])
                    date_depart = datetime.strptime(vol_data['date_heure_depart'], '%Y-%m-%d %H:%M:%S')
                    date_arrivee = datetime.strptime(vol_data['date_heure_arrivee'], '%Y-%m-%d %H:%M:%S')
                    
                    # Occupation au départ
                    if aeroport_depart_csv == aeroport and date_depart.date() == date_cible:
                        debut = date_depart
                        fin = debut + timedelta(minutes=10)
                        occupations.append((debut, fin))
                    
                    # Occupation à l'arrivée
                    if aeroport_arrivee_csv == aeroport and date_arrivee.date() == date_cible:
                        debut = date_arrivee
                        fin = debut + timedelta(minutes=10)
                        occupations.append((debut, fin))
                        
                except (Avion.DoesNotExist, Aeroport.DoesNotExist, ValueError):
                    continue
        
        # Vérifier les conflits
        heure_fin_utilisation = heure_cible + timedelta(minutes=10)
        
        for debut_occupation, fin_occupation in occupations:
            if not (heure_fin_utilisation <= debut_occupation or heure_cible >= fin_occupation):
                return False, fin_occupation
        
        return True, None
    
    def suggest_next_available_time(self, aeroport, heure_souhaitee, avion, vols_existants=None, vol_actuel_ligne=None):
        """Trouve le prochain créneau libre"""
        pistes_compatibles = aeroport.pistes.filter(
            longueur__gte=avion.type_avion.longueur_piste_necessaire
        )
        
        if not pistes_compatibles.exists():
            return None
        
        heure_test = heure_souhaitee
        date_cible = heure_souhaitee.date()
        
        # Essayer jusqu'à 24h plus tard
        while heure_test.date() == date_cible:
            disponible, _ = self.is_piste_available(aeroport, heure_test, avion, vols_existants, vol_actuel_ligne)
            if disponible:
                return heure_test
            heure_test += timedelta(minutes=10)
        
        return None
    
    def validate_vol_data(self, vol_data, ligne_numero, vols_existants=None):
        """Valide un vol avec la même logique que VolForm"""
        try:
            # Récupérer les objets
            avion = Avion.objects.get(id=vol_data['avion_id'])
            aeroport_depart = Aeroport.objects.get(id=vol_data['aeroport_depart_id'])
            aeroport_arrivee = Aeroport.objects.get(id=vol_data['aeroport_arrivee_id'])
            
            # Parser les dates
            date_heure_depart = datetime.strptime(vol_data['date_heure_depart'], '%Y-%m-%d %H:%M:%S')
            date_heure_arrivee = datetime.strptime(vol_data['date_heure_arrivee'], '%Y-%m-%d %H:%M:%S')
            
        except Avion.DoesNotExist:
            self.errors.append(f"Ligne {ligne_numero}: Avion avec l'ID {vol_data['avion_id']} introuvable")
            return False
        except Aeroport.DoesNotExist as e:
            aeroport_id = vol_data.get('aeroport_depart_id', vol_data.get('aeroport_arrivee_id', 'inconnu'))
            self.errors.append(f"Ligne {ligne_numero}: Aéroport avec l'ID {aeroport_id} introuvable")
            return False
        except ValueError as e:
            self.errors.append(f"Ligne {ligne_numero}: Format de date invalide - {str(e)}")
            return False
        except KeyError as e:
            self.errors.append(f"Ligne {ligne_numero}: Colonne manquante - {str(e)}")
            return False
        
        # Vérifications de base
        if aeroport_depart == aeroport_arrivee:
            self.errors.append(f"Ligne {ligne_numero}: L'aéroport de départ et d'arrivée ne peuvent pas être identiques")
            return False
        
        if date_heure_arrivee <= date_heure_depart:
            self.errors.append(f"Ligne {ligne_numero}: La date d'arrivée doit être postérieure à celle de départ")
            return False
        
        # Vérifier la compatibilité des pistes
        pistes_depart = aeroport_depart.pistes.filter(
            longueur__gte=avion.type_avion.longueur_piste_necessaire
        )
        if not pistes_depart.exists():
            self.errors.append(
                f"Ligne {ligne_numero}: Aucune piste de l'aéroport {aeroport_depart.nom} n'est assez longue "
                f"pour l'avion {avion.nom} (minimum requis: {avion.type_avion.longueur_piste_necessaire}m)"
            )
            return False
        
        pistes_arrivee = aeroport_arrivee.pistes.filter(
            longueur__gte=avion.type_avion.longueur_piste_necessaire
        )
        if not pistes_arrivee.exists():
            self.errors.append(
                f"Ligne {ligne_numero}: Aucune piste de l'aéroport {aeroport_arrivee.nom} n'est assez longue "
                f"pour l'avion {avion.nom} (minimum requis: {avion.type_avion.longueur_piste_necessaire}m)"
            )
            return False
        
        # Vérifier la disponibilité au départ
        disponible_depart, _ = self.is_piste_available(aeroport_depart, date_heure_depart, avion, vols_existants, ligne_numero-2)
        if not disponible_depart:
            heure_proposee = self.suggest_next_available_time(aeroport_depart, date_heure_depart, avion, vols_existants, ligne_numero-2)
            if heure_proposee:
                self.errors.append(
                    f"Ligne {ligne_numero}: Aucune piste disponible à l'aéroport {aeroport_depart.nom} "
                    f"le {date_heure_depart.strftime('%d/%m/%Y à %H:%M')}. "
                    f"Prochain créneau: {heure_proposee.strftime('%d/%m/%Y à %H:%M')}"
                )
            else:
                self.errors.append(f"Ligne {ligne_numero}: Aucune piste compatible à l'aéroport {aeroport_depart.nom}")
            return False
        
        # Vérifier la disponibilité à l'arrivée
        disponible_arrivee, _ = self.is_piste_available(aeroport_arrivee, date_heure_arrivee, avion, vols_existants, ligne_numero-2)
        if not disponible_arrivee:
            heure_proposee = self.suggest_next_available_time(aeroport_arrivee, date_heure_arrivee, avion, vols_existants, ligne_numero-2)
            if heure_proposee:
                self.errors.append(
                    f"Ligne {ligne_numero}: Aucune piste disponible à l'aéroport {aeroport_arrivee.nom} "
                    f"le {date_heure_arrivee.strftime('%d/%m/%Y à %H:%M')}. "
                    f"Prochain créneau: {heure_proposee.strftime('%d/%m/%Y à %H:%M')}"
                )
            else:
                self.errors.append(f"Ligne {ligne_numero}: Aucune piste compatible à l'aéroport {aeroport_arrivee.nom}")
            return False
        
        return True