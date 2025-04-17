from django.shortcuts import render, redirect
from .forms import PatientForm
from .models import Patient
def enregistrer_patient(request):
    if request.method == "POST":
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('patients:liste_patients')  # Redirection après succès
    else:
        form = PatientForm()
    return render(request, 'patients/enregistrer_patient.html', {'form': form})

def liste_patients(request):
    patients = Patient.objects.all()
    return render(request, 'patients/liste_patients.html', {'patients': patients})