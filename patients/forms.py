from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['nom', 'prenom', 'age', 'sexe', 'taille', 'poids', 'adresse', 'telephone', 'photo']
