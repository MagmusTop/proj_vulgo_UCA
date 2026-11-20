from django.urls import path
from ranked.controllers import accueil, avis  # 👈 Correction de la faute de frappe
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('welcome/',  views.loading_welcome,  name='loading_welcome'),
    path('/accueil', accueil.afficher_accueil, name='accueil'),
    path('avis/nouveau/', avis.soumettre_avis, name='soumettre_avis'),
    path('avis/<int:avis_id>/vote/<str:type_vote>/', avis.voter_avis, name='voter_avis'),
]