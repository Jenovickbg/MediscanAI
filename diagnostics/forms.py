from django import forms
from .models import BloodSmear

class BloodSmearForm(forms.ModelForm):
    class Meta:
        model = BloodSmear
        fields = ['image']  # On retire 'patient' car il sera assigné dans la vue
