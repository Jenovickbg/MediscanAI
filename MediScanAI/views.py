from django.shortcuts import render
from patients.models import Patient
from diagnostics.models import BloodSmear, MedicalReport
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

def home(request):
    # Statistiques globales
    total_patients = Patient.objects.count()
    total_analyses = BloodSmear.objects.count()
    total_rapports = MedicalReport.objects.count()
    total_positifs = BloodSmear.objects.exclude(diagnostic__iexact='Normal').count()

    # Analyses récentes (5 dernières)
    recent_analyses = BloodSmear.objects.select_related('patient').order_by('-uploaded_at')[:5]

    # Derniers patients (5 derniers)
    recent_patients = Patient.objects.order_by('-date_enregistrement')[:5]

    # Données pour le graphique (diagnostics positifs par jour sur 7 jours)
    today = timezone.now().date()
    days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    day_labels = [d.strftime('%a') for d in days]
    diagnostics_per_day = []
    for d in days:
        count = BloodSmear.objects.filter(uploaded_at__date=d).exclude(diagnostic__iexact='Normal').count()
        diagnostics_per_day.append(count)

    context = {
        'total_patients': total_patients,
        'total_analyses': total_analyses,
        'total_rapports': total_rapports,
        'total_positifs': total_positifs,
        'recent_analyses': recent_analyses,
        'recent_patients': recent_patients,
        'chart_labels': day_labels,
        'chart_data': diagnostics_per_day,
    }
    return render(request, 'home.html', context)
