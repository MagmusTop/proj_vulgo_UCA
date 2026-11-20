
from django.shortcuts import render
from django.db.models import Avg, Count, Q
from django.contrib.sessions.models import Session
from ranked.models.models import Visitor, Vote


def afficher_accueil(request):

    # Statistiques générales
    note_moyenne = Visitor.objects.aggregate(
        Avg('note')
    )['note__avg'] or 0

    total_avis = Visitor.objects.count()

    # Récupération du critère de tri
    tri = request.GET.get('tri', 'recent')

    # Liste des avis avec calcul des votes
    liste_avis = Visitor.objects.select_related(
        'comment'
    ).annotate(
        agree_count=Count(
            'comment__votes',
            filter=Q(comment__votes__vote_type='agree'),
            distinct=True
        ),
        disagree_count=Count(
            'comment__votes',
            filter=Q(comment__votes__vote_type='not_agree'),
            distinct=True
        )
    )

    # Application du tri
    tris_disponibles = {
        'note_desc': ['-note', '-modified_at'],
        'note_asc': ['note', '-modified_at'],
        'agree_desc': ['-agree_count', '-modified_at'],
        'agree_asc': ['agree_count', '-modified_at'],
        'recent': ['-modified_at', '-comment__modified_at'],
    }

    liste_avis = liste_avis.order_by(
        *tris_disponibles.get(tri, tris_disponibles['recent'])
    )

    # Avis de l'utilisateur actuel
    mon_avis = None

    if request.session.session_key:
        mon_avis = Visitor.objects.filter(
            session__session_key=request.session.session_key
        ).first()

    # Votes de l'utilisateur actuel
    agree_ids = []
    disagree_ids = []

    if request.session.session_key:
        session_obj = Session.objects.filter(
            session_key=request.session.session_key
        ).first()

        if session_obj:
            user_votes = Vote.objects.filter(session=session_obj)

            agree_ids = [
                v.comment_id for v in user_votes
                if v.vote_type == 'agree'
            ]

            disagree_ids = [
                v.comment_id for v in user_votes
                if v.vote_type == 'not_agree'
            ]

    context = {
        'note_moyenne': round(note_moyenne, 1),
        'total_avis': total_avis,
        'avis': liste_avis,
        'mon_avis': mon_avis,
        'agree_ids': agree_ids,
        'disagree_ids': disagree_ids,
        'tri_actuel': tri,
    }

    return render(request, 'ranked/accueil.html', context)
