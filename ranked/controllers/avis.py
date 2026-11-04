import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.sessions.models import Session
from ranked.models.models import Visitor, Vote, Comment

def soumettre_avis(request):
    visiteur_existant = None
    if request.session.session_key:
        visiteur_existant = Visitor.objects.filter(session__session_key=request.session.session_key).first()

    if request.method == "POST":
        note = request.POST.get('note')
        commentaire_texte = request.POST.get('commentaire', '').strip()

        if note:
            if not request.session.session_key:
                request.session.create()
            session_obj = Session.objects.filter(session_key=request.session.session_key).first()
            
            pseudo = request.session.get('visitor_pseudo')
            if not pseudo:
                pseudo = f"Visiteur_{uuid.uuid4().hex[:6]}"
                request.session['visitor_pseudo'] = pseudo
            
            if visiteur_existant:
                visiteur_existant.note = int(note)
                
                # 👇 GESTION DU COMMENTAIRE ET RESET DES VOTES
                if commentaire_texte:
                    if not visiteur_existant.comment:
                        # Nouveau commentaire
                        visiteur_existant.comment = Comment.objects.create(text=commentaire_texte)
                    elif visiteur_existant.comment.text != commentaire_texte:
                        # Le texte a changé : on supprime l'ancien et on en crée un nouveau
                        old_comment = visiteur_existant.comment
                        visiteur_existant.comment = Comment.objects.create(text=commentaire_texte)
                        old_comment.delete() # Supprime l'ancien commentaire et ses votes
                else:
                    # L'utilisateur a vidé son commentaire
                    if visiteur_existant.comment:
                        old_comment = visiteur_existant.comment
                        visiteur_existant.comment = None
                        old_comment.delete()

                visiteur_existant.save()
                messages.success(request, f"Merci {pseudo} ! Votre avis a bien été modifié.")
            else:
                comment_obj = None
                if commentaire_texte:
                    comment_obj = Comment.objects.create(text=commentaire_texte)
                
                Visitor.objects.create(
                    user_anonymos=pseudo,
                    session=session_obj,
                    note=int(note),
                    comment=comment_obj
                )
                messages.success(request, f"Merci {pseudo} ! Votre avis a bien été enregistré.")
                
            return redirect('accueil')
        else:
            messages.error(request, "Veuillez au moins sélectionner une note.")

    pseudo_actuel = request.session.get('visitor_pseudo', 'Nouveau visiteur')
    note_existante = visiteur_existant.note if visiteur_existant else None
    commentaire_existant = visiteur_existant.comment.text if visiteur_existant and visiteur_existant.comment else ""

    return render(request, 'ranked/formulaire.html', {
        'pseudo': pseudo_actuel,
        'note_existante': note_existante,
        'commentaire_existant': commentaire_existant
    })

def voter_avis(request, avis_id, type_vote):
    avis = get_object_or_404(Visitor, id=avis_id)
    
    if not avis.comment:
        messages.error(request, "Impossible de voter, cet avis n'a pas de commentaire.")
        return redirect(request.META.get('HTTP_REFERER', 'accueil'))
        
    if not request.session.session_key:
        request.session.create()
    
    session_obj = Session.objects.filter(session_key=request.session.session_key).first()

    # 👇 LA MAGIE EST ICI : update_or_create
    # - Si l'utilisateur n'a pas voté : ça crée le vote.
    # - S'il a voté "agree" et clique sur "not_agree" : ça met à jour la ligne existante.
    vote, created = Vote.objects.update_or_create(
        comment=avis.comment,
        session=session_obj,
        defaults={'vote_type': type_vote}
    )
    
    if created:
        messages.success(request, "Votre vote a été enregistré.")
    else:
        messages.success(request, "Votre vote a été modifié.")
        
    return redirect(request.META.get('HTTP_REFERER', 'accueil'))