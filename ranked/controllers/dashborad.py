from django.shortcuts import render
from django.db.models import Avg
from ranked.models.models import *  # 👈 Import corrigé

def afficher_dashboard(request):
    note_moyenne = Rank.objects.aggregate(Avg('rank'))['rank__avg'] or 0
    total_avis = Rank.objects.count()
    liste_avis = Rank.objects.all().order_by('-id')

    context = {
        'note_moyenne': round(note_moyenne, 1),
        'total_avis': total_avis,
        'avis': liste_avis,
    }

    # 👈 Redirection vers le template dans le dossier 'ranked'
    return render(request, 'ranked/dashboard.html', context)