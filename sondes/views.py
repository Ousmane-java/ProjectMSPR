from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Franchise

# Vue pour la page d'accueil
def home(request):
    return HttpResponse("<h1>Bienvenue sur Seahawks Nester</h1><p>Ceci est la page d'accueil de votre projet.</p>")

# Vue pour la liste des franchises
def franchise_list(request):
    franchises = Franchise.objects.all()  # Récupère toutes les franchises
    return render(request, 'sondes/franchise_list.html', {'franchises': franchises})

# Vue pour les détails d'une franchise
def franchise_detail(request, franchise_id):
    franchise = get_object_or_404(Franchise, id=franchise_id)  # Récupère une franchise ou retourne une erreur 404
    return render(request, 'sondes/franchise_detail.html', {'franchise': franchise})
