# urls.py
from django.urls import path
from . import views

app_name = 'diagnostics'

urlpatterns = [
    path('', views.analyse_frottis_sanguins, name='analyse_frottis_sanguins'),
    path('recherche-patient/', views.rechercher_patient, name='recherche_patient'),
    path('upload/<int:patient_id>/', views.upload_analyse_frottis, name='upload_analyse_frottis'),
    path('historique/<int:patient_id>/', views.historique_patient, name='historique_patient'),
    path('detail/<int:frottis_id>/', views.detail_frottis, name='detail_frottis'),
    path('rapports/<int:patient_id>/', views.liste_rapports, name='liste_rapports'),
    path('rapports/', views.tous_les_rapports, name='tous_les_rapports'),
    path('generate-rapport/<int:frottis_id>/', views.generate_medical_report, name='generate_medical_report'),
]
