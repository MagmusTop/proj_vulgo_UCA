from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import F
from ranked.models.models import * # 👈 Import corrigé

def soumettre_avis(request):
    if request.method == "POST":
        note = request.POST.get('rank')
        commentaire = request.POST.get('commentaire')
        pseudo = request.POST.get('user_anonymos')

        if note and commentaire and pseudo:
            nouvel_avis = Rank.objects.create(
                rank=int(note),
                commentaire=commentaire
            )
            Visitor.objects.create(
                user_anonymos=pseudo,
                rank=nouvel_avis
            )
            messages.success(request, "Merci ! Votre avis a bien été enregistré.")
            return redirect('dashboard')
        else:
            messages.error(request, "Veuillez remplir tous les champs.")

    # 👈 Redirection vers le template dans le dossier 'ranked'
    return render(request, 'ranked/formulaire.html')

def voter_avis(request, avis_id, type_vote):
    avis = get_object_or_404(Rank, id=avis_id)
    
    if type_vote == 'agree':
        avis.nb_agree = F('nb_agree') + 1
    elif type_vote == 'not_agree':
        avis.nb_not_agree = F('nb_not_agree') + 1
        
    avis.save()
    messages.success(request, "Votre vote a été pris en compte.")
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))