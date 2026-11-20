from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Clé de session marquant que la loading page a déjà été vue
SESSION_FLAG = 'bienvenue_vue'


def home(request):
    """Racine du site : loading page à la 1ère visite, sinon notation."""
    if not request.session.get(SESSION_FLAG):
        # Écrire dans la session crée la session Django côté serveur
        request.session[SESSION_FLAG] = True
        return redirect('loading_welcome')
    return redirect('soumettre_avis')


def loading_welcome(request):
    """Page tampon affichée une seule fois par session."""
    return render(request, 'ranked/loading.html')


@login_required  # à retirer si la notation est publique
def notation(request):
    # Marque aussi la session si l'utilisateur arrive ici par un autre chemin
    # (lien direct, favori, etc.) → évite de revoir la loading page après
    request.session[SESSION_FLAG] = True
    return render(request, 'commentaires/notation.html')