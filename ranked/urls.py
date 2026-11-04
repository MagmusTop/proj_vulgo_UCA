from django.urls import path
from ranked.controllers import accueil, avis  # 👈 Correction de la faute de frappe

urlpatterns = [
    path('', accueil.afficher_accueil, name='accueil'),
    path('avis/nouveau/', avis.soumettre_avis, name='soumettre_avis'),
    path('avis/<int:avis_id>/vote/<str:type_vote>/', avis.voter_avis, name='voter_avis'),
]