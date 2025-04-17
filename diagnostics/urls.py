# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('analyse/', views.analyser_frottis, name='analyse_frottis'),
   # path('liste/', views.liste_patients, name='liste_patients'),  # Vue à définir
]
