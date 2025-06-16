from django.db import models


class Aeroport(models.Model):
    nom = models.CharField(max_length=100)
    pays = models.CharField(max_length=100)

    class Meta:
        db_table = 'aeroport'
        verbose_name = 'Aéroport'
        verbose_name_plural = 'Aéroports'

    def __str__(self):
        return self.nom


class Piste(models.Model):
    numero = models.IntegerField()
    aeroport = models.ForeignKey(
        Aeroport,
        on_delete=models.CASCADE,
        related_name='pistes'
    )
    longueur = models.IntegerField()

    class Meta:
        db_table = 'piste'
        verbose_name = 'Piste'
        verbose_name_plural = 'Pistes'
        unique_together = (('numero', 'aeroport'),)

    def __str__(self):
        return f"Piste {self.numero} - {self.aeroport.nom}"


class Compagnie(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    pays_rattachement = models.CharField(max_length=100)

    class Meta:
        db_table = 'compagnie'
        verbose_name = 'Compagnie'
        verbose_name_plural = 'Compagnies'

    def __str__(self):
        return self.nom


class TypeAvion(models.Model):
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    longueur_piste_necessaire = models.IntegerField()

    class Meta:
        db_table = 'type_avion'
        verbose_name = "Type d'Avion"
        verbose_name_plural = "Types d'Avion"

    def __str__(self):
        return f"{self.marque} {self.modele}"


class Avion(models.Model):
    nom = models.CharField(max_length=100)
    compagnie = models.ForeignKey(
        Compagnie,
        on_delete=models.CASCADE,
        related_name='avions'
    )
    type_avion = models.ForeignKey(
        TypeAvion,
        on_delete=models.CASCADE,
        related_name='avions'
    )

    class Meta:
        db_table = 'avion'
        verbose_name = 'Avion'
        verbose_name_plural = 'Avions'

    def __str__(self):
        return self.nom


class Vol(models.Model):
    avion = models.ForeignKey(
        Avion,
        on_delete=models.CASCADE,
        related_name='vols'
    )
    pilote = models.CharField(max_length=100)
    aeroport_depart = models.ForeignKey(
        Aeroport,
        on_delete=models.CASCADE,
        related_name='vols_depart'
    )
    date_heure_depart = models.DateTimeField()
    aeroport_arrivee = models.ForeignKey(
        Aeroport,
        on_delete=models.CASCADE,
        related_name='vols_arrivee'
    )
    date_heure_arrivee = models.DateTimeField()

    class Meta:
        db_table = 'vol'
        verbose_name = 'Vol'
        verbose_name_plural = 'Vols'
        ordering = ['date_heure_depart']

    def __str__(self):
        return f"Vol {self.id} - {self.pilote} ({self.aeroport_depart} → {self.aeroport_arrivee})"
