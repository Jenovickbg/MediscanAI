from django.urls import path
from .views import enregistrer_patient, liste_patients  # Importation de la vue

app_name = 'patients'  # Namespace pour éviter les conflits

urlpatterns = [
    path('enregistrer/', enregistrer_patient, name='enregistrer_patient'),
    path('liste/', liste_patients, name='liste_patients'),  # Ajout de la liste des patients
]
