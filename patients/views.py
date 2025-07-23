from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import PatientForm, HistoriqueMedicalForm
from .models import Patient, HistoriqueMedical

def liste_patients(request):
    patients = Patient.objects.all().order_by('-date_enregistrement')
    return render(request, 'patients/liste_patients.html', {'patients': patients})

# Modal: Ajout patient

def ajouter_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    else:
        form = PatientForm()
    return render(request, 'patients/form_modal.html', {'form': form, 'action': 'ajouter'})

# Modal: Modifier patient

def modifier_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES, instance=patient)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patients/form_modal.html', {'form': form, 'action': 'modifier', 'patient': patient})

# Modal: Supprimer patient

def supprimer_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        return JsonResponse({'success': True})
    return render(request, 'patients/delete_modal.html', {'patient': patient})

# Modal: Historique médical

def historique_medical(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    historiques = patient.historiques.all().order_by('-date')
    return render(request, 'patients/historique_modal.html', {'patient': patient, 'historiques': historiques})

# Modal: Ajouter acte médical

def ajouter_acte_medical(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = HistoriqueMedicalForm(request.POST)
        if form.is_valid():
            acte = form.save(commit=False)
            acte.patient = patient
            acte.save()
            return JsonResponse({'success': True})
    else:
        form = HistoriqueMedicalForm()
    return render(request, 'patients/acte_form_modal.html', {'form': form, 'patient': patient})