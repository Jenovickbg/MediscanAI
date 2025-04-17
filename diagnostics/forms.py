from django import forms
from .models import BloodSmear

class BloodSmearForm(forms.ModelForm):
    class Meta:
        model = BloodSmear
        fields = ['patient_id', 'image']
