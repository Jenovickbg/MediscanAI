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
import textwrap

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
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.utils import ImageReader
    from reportlab.lib import colors
    from reportlab.platypus import Table, TableStyle
    from django.http import JsonResponse
    import json
    frottis = get_object_or_404(BloodSmear, id=frottis_id)
    patient = frottis.patient
    frottis.save()

    from .models import MedicalReport

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Méthode non autorisée.'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        explication = data.get('explication', '').strip()
        recommandations = data.get('recommandation', '').strip()
        if not explication or not recommandations:
            return JsonResponse({'success': False, 'error': 'Tous les champs sont obligatoires.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': 'Erreur de données envoyées.'})

    if MedicalReport.objects.filter(frottis=frottis).exists():
        return JsonResponse({'success': False, 'error': 'Un rapport existe déjà pour cette analyse.'})

    filename = f"rapport_{patient.nom}_{patient.prenom}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf_dir = os.path.join(settings.MEDIA_ROOT, 'rapports_pdfs')
    os.makedirs(pdf_dir, exist_ok=True)
    pdf_path = os.path.join('rapports_pdfs', filename)
    full_pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_path)

    # --- Début génération PDF stylisé ---
    c = canvas.Canvas(full_pdf_path, pagesize=A4)
    width, height = A4

    # Logo (supposé dans static/images/logo.png)
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'logo.png')
    if os.path.exists(logo_path):
        c.drawImage(logo_path, 60, height - 100, width=80, height=60, mask='auto')
        c.drawImage(logo_path, width - 140, height - 100, width=80, height=60, mask='auto')

    # En-tête
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 60, "ESPACE MEDISCAN AI")
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, height - 75, " Avenue de Libération,Kinshasa/Lingwala")

    # Titre
    c.setFont("Helvetica-Bold", 15)
    c.setFillColor(colors.HexColor("#2b6d8c"))
    c.drawCentredString(width / 2, height - 120, "CERTIFICAT D'ANALYSE MÉDICALE")
    c.setFillColor(colors.black)
    c.line(width/2 - 120, height - 125, width/2 + 120, height - 125)

    # Corps du texte
    y = height - 160
    c.setFont("Helvetica", 11)
    c.drawString(60, y, f"Je soussigné(e), Docteur, certifie que l'état de santé de :")
    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(60, y, f"Mr/Mme, Mlle : {patient.nom.upper()} {patient.prenom.title()}")
    y -= 20
    c.setFont("Helvetica", 11)
    c.drawString(60, y, f"a nécessité une analyse médicale dans notre centre.")
    y -= 20
    c.drawString(60, y, f"Date de l'analyse : {frottis.uploaded_at.strftime('%d/%m/%Y %H:%M')}")
    y -= 20
    c.drawString(60, y, f"Diagnostic : ")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(130, y, f"{frottis.diagnostic}")
    c.setFont("Helvetica", 11)
    y -= 20
    c.drawString(60, y, f"Confiance : ")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(130, y, f"{frottis.confiance}%")
    c.setFont("Helvetica", 11)
    y -= 30

    # Explication et recommandations
    c.setFont("Helvetica-Bold", 11)
    c.drawString(60, y, "Explication médicale :")
    c.setFont("Helvetica", 11)
    y -= 18
    for line in explication.split('\n'):
        for wrapped in textwrap.wrap(line, width=90):
            c.drawString(70, y, wrapped)
            y -= 15
    y -= 10
    c.setFont("Helvetica-Bold", 11)
    c.drawString(60, y, "Recommandations :")
    c.setFont("Helvetica", 11)
    y -= 18
    for line in recommandations.split('\n'):
        for wrapped in textwrap.wrap(line, width=90):
            c.drawString(70, y, wrapped)
            y -= 15
    y -= 10

    # Tableau des frais (exemple)
    data = [
        ["Nature", "Montant (CDF)"] ,
        ["Analyse frottis sanguin", "15000"],
        ["Consultation", "10000"],
        ["Prestations diverses", "500"],
        ["TOTAL", "500"]
    ]
    table = Table(data, colWidths=[200, 100])
    style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2b6d8c")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('BACKGROUND', (0,1), (-1,-2), colors.whitesmoke),
        ('GRID', (0,0), (-1,-1), 1, colors.grey),
        ('FONTNAME', (-1,-1), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
    ])
    table.setStyle(style)
    table.wrapOn(c, width, height)
    table.drawOn(c, 60, y-100)

    # Pied de page
    c.setFont("Helvetica-Oblique", 9)
    c.setFillColor(colors.HexColor("#888888"))
    c.drawCentredString(width / 2, 100, "L'analyse a été effectuée par MediScan AI, un système intelligent d'aide au diagnostic médical.")
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10)
    c.drawString(60, 80, f"Fait à Kinshasa le {datetime.now().strftime('%d/%m/%Y')}")
    c.drawString(width - 180, 80, "Signature médecin")
    c.line(width - 180, 75, width - 80, 75)

    c.save()

    rapport = MedicalReport.objects.create(
        patient=patient,
        frottis=frottis,
        explication=explication,
        recommandations=recommandations,
        pdf_path=pdf_path
    )
    return JsonResponse({'success': True})
