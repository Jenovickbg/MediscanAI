from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Q
from .forms import BloodSmearForm
from .models import BloodSmear
from patients.models import Patient
import random
from django.urls import reverse
from django.contrib import messages
from .models import MedicalReport
import os
from datetime import datetime
from django.core.files.base import ContentFile
from bson import ObjectId
from django.http import Http404

# Simulation de diagnostic (en attendant le vrai modèle)
def simulate_diagnostic():
    diagnostics = [
        "Paludisme", "Anémie", "Leucémie", "Normal", "Infection bactérienne"
    ]
    diagnostic = random.choice(diagnostics)
    confiance = random.uniform(85.0, 99.9)
    return diagnostic, round(confiance, 1)

# Vue principale - Page d'analyse des frottis sanguins
def analyse_frottis_sanguins(request):
    # Récupérer tous les frottis pour l'historique
    frottis_list = BloodSmear.objects.all().order_by('-uploaded_at')
    
    return render(request, 'diagnostics/analyse_frottis.html', {
        'frottis_list': frottis_list
    })

# Vue pour rechercher un patient
def rechercher_patient(request):
    query = request.GET.get('q', '')
    patients = []
    
    if query:
        patients = Patient.objects.filter(
            Q(nom__icontains=query) | 
            Q(prenom__icontains=query) |
            Q(telephone__icontains=query)
        )[:10]  # Limiter à 10 résultats
    
    return render(request, 'diagnostics/recherche_patient.html', {
        'patients': patients,
        'query': query
    })

# Vue pour uploader et analyser un frottis
def upload_analyse_frottis(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        form = BloodSmearForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Créer l'objet BloodSmear
                frottis = BloodSmear()
                frottis.patient = patient
                frottis.image = form.cleaned_data['image']
                
                # Simulation du diagnostic
                diagnostic, confiance = simulate_diagnostic()
                frottis.diagnostic = diagnostic
                frottis.confiance = confiance
                
                # Sauvegarder explicitement
                frottis.save()
                
                print(f"Frottis sauvegardé avec ID: {frottis.id}")
                
                return JsonResponse({
                    'success': True,
                    'diagnostic': diagnostic,
                    'confiance': confiance,
                    'patient_nom': patient.nom,
                    'patient_prenom': patient.prenom,
                    'frottis_id': str(frottis.id)  # Convertir ObjectId en string
                })
            except Exception as e:
                print(f"Erreur lors de la sauvegarde: {str(e)}")
                return JsonResponse({
                    'success': False,
                    'error': f'Erreur lors de la sauvegarde: {str(e)}'
                })
        else:
            # Formulaire invalide
            errors = form.errors
            print(f"Erreurs de formulaire: {errors}")
            return JsonResponse({
                'success': False,
                'error': 'Formulaire invalide',
                'form_errors': errors
            })
    else:
        form = BloodSmearForm()

    return render(request, 'diagnostics/upload_analyse.html', {
        'form': form,
        'patient': patient
    })

# Vue pour l'historique des analyses d'un patient
def historique_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    frottis_list = BloodSmear.objects.filter(patient=patient).order_by('-uploaded_at')
    print(f"Patient: {patient.nom} {patient.prenom}")
    print(f"Nombre de frottis valides: {frottis_list.count()}")
    for frottis in frottis_list:
        print(f"Frottis ID: {frottis.id}, Diagnostic: {frottis.diagnostic}")
    return render(request, 'diagnostics/historique_patient.html', {
        'patient': patient,
        'frottis_list': frottis_list
    })

# Vue pour voir le détail d'un frottis
def detail_frottis(request, frottis_id):
    frottis = get_object_or_404(BloodSmear, id=frottis_id)
    return render(request, 'diagnostics/detail_frottis.html', {'frottis': frottis})

def liste_rapports(request, patient_id):
    from .models import MedicalReport
    patient = get_object_or_404(Patient, id=patient_id)
    rapports = MedicalReport.objects.filter(patient=patient).order_by('-created_at')
    return render(request, 'diagnostics/liste_rapports.html', {
        'patient': patient,
        'rapports': rapports
    })

def tous_les_rapports(request):
    from .models import MedicalReport
    rapports = MedicalReport.objects.all().order_by('-created_at')
    return render(request, 'diagnostics/tous_les_rapports.html', {
        'rapports': rapports
    })

def generate_medical_report(request, frottis_id):
    import os
    from django.conf import settings
    from datetime import datetime
    from reportlab.pdfgen import canvas
    frottis = get_object_or_404(BloodSmear, id=frottis_id)
    patient = frottis.patient
    frottis.save()

    from .models import MedicalReport
    from django.contrib import messages
    from django.urls import reverse

    if MedicalReport.objects.filter(frottis=frottis).exists():
        messages.info(request, "Un rapport existe déjà pour cette analyse.")
        return redirect(reverse('diagnostics:detail_frottis', args=[frottis.id]))

    filename = f"rapport_{patient.nom}_{patient.prenom}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf_dir = os.path.join(settings.MEDIA_ROOT, 'rapports_pdfs')
    os.makedirs(pdf_dir, exist_ok=True)
    pdf_path = os.path.join('rapports_pdfs', filename)
    full_pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_path)

    # Génération du PDF avec ReportLab
    c = canvas.Canvas(full_pdf_path)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 800, "Rapport Médical - MEDISCAN AI")
    c.setFont("Helvetica", 12)
    c.drawString(100, 770, f"Patient : {patient.nom} {patient.prenom}")
    c.drawString(100, 750, f"Diagnostic : {frottis.diagnostic}")
    c.drawString(100, 730, f"Confiance : {frottis.confiance}%")
    c.drawString(100, 710, f"Date : {frottis.uploaded_at.strftime('%d/%m/%Y %H:%M')}")
    c.drawString(100, 690, f"Explication : ...")
    c.drawString(100, 670, f"Recommandations : ...")
    c.save()

    rapport = MedicalReport.objects.create(
        patient=patient,
        frottis=frottis,
        explication="Explication médicale à compléter...",
        recommandations="Recommandations à compléter...",
        pdf_path=pdf_path
    )
    messages.success(request, "Rapport médical généré avec succès !")
    return redirect(reverse('diagnostics:detail_frottis', args=[frottis.id]))
