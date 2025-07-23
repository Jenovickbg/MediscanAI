from django.urls import path
from .views import (
    liste_patients, ajouter_patient, modifier_patient, supprimer_patient,
    historique_medical, ajouter_acte_medical
)

app_name = 'patients'

urlpatterns = [
    path('', liste_patients, name='liste_patients'),
    path('ajouter/', ajouter_patient, name='ajouter_patient'),
    path('modifier/<int:pk>/', modifier_patient, name='modifier_patient'),
    path('supprimer/<int:pk>/', supprimer_patient, name='supprimer_patient'),
    path('historique/<int:pk>/', historique_medical, name='historique_medical'),
    path('ajouter-acte/<int:pk>/', ajouter_acte_medical, name='ajouter_acte_medical'),
]
