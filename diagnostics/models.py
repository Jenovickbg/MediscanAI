from django.db import models
from patients.models import Patient
import uuid

class BloodSmear(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='frottis')
    image = models.ImageField(upload_to='blood_smears/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    diagnostic = models.CharField(max_length=100)  # Diagnostic simulé (ex: Paludisme, Anémie...)
    confiance = models.FloatField(null=True, blank=True, default=0)  # Pourcentage de confiance simulé

    def __str__(self):
        return f"Frottis de {self.patient.nom} {self.patient.prenom} - {self.uploaded_at.strftime('%Y-%m-%d')}"

class MedicalReport(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='rapports')
    frottis = models.ForeignKey(BloodSmear, on_delete=models.CASCADE, related_name='rapports')
    pdf_path = models.CharField(max_length=255, blank=True)  # Chemin du PDF généré
    created_at = models.DateTimeField(auto_now_add=True)
    explication = models.TextField(blank=True)
    recommandations = models.TextField(blank=True)

    def __str__(self):
        return f"Rapport de {self.patient.nom} {self.patient.prenom} - {self.created_at.strftime('%Y-%m-%d')}"
