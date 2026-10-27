from django.urls import path
from ranked.controllers import dashborad,avis   # 👈 Import corrigé

urlpatterns = [
    path('', dashborad.afficher_dashboard, name='dashboard'),
    path('avis/nouveau/', avis.soumettre_avis, name='soumettre_avis'),
    path('avis/<int:avis_id>/vote/<str:type_vote>/', avis.voter_avis, name='voter_avis'),
]