from django import forms
from .models import Patient, HistoriqueMedical

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['nom', 'prenom', 'age', 'sexe', 'taille', 'poids', 'adresse', 'telephone', 'photo']

class HistoriqueMedicalForm(forms.ModelForm):
    class Meta:
        model = HistoriqueMedical
        fields = ['type_acte', 'description']
