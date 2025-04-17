# patients/models.py
from django.db import models

class Patient(models.Model):
    SEX_CHOICES = [('M', 'Masculin'), ('F', 'Féminin')]
    
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    age = models.IntegerField()
    sexe = models.CharField(max_length=1, choices=SEX_CHOICES)
    taille = models.FloatField()  # en cm
    poids = models.FloatField()  # en kg
    adresse = models.TextField()
    telephone = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='patients_photos/')
    date_enregistrement = models.DateTimeField(auto_now_add=True)  # Ajout de la date d'enregistrement
    
    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.age} ans)"

