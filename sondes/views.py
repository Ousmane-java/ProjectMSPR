from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Franchise
from rest_framework import viewsets
from .models import Franchise, SondaStatus, ScanReport, NetworkLatency, ApplicationVersion
from .serializers import FranchiseSerializer, SondaStatusSerializer, ScanReportSerializer, NetworkLatencySerializer, ApplicationVersionSerializer

# Vue pour la page d'accueil
def home(request):
    return HttpResponse("<h1>Bienvenue sur Seahawks Nester</h1><p>Ceci est la page d'accueil de votre projet.</p>")

# Vue pour la liste des franchises
def franchise_list(request):
    franchises = Franchise.objects.all()  # Récupère toutes les franchises

    # Processer les ports ouverts/fermés pour affichage
    for franchise in franchises:
        if franchise.ports_open:
            # Sépare les ports en une liste et ajoute des indicateurs d'état
            ports = franchise.ports_open.split(", ")
            franchise.ports_display = [
                {"port": port, "status": "open" if int(port) < 1024 else "closed"} for port in ports
            ]

    return render(request, 'sondes/franchise_list.html', {'franchises': franchises})

# Vue pour les détails d'une franchise
def franchise_detail(request, franchise_id):
    franchise = get_object_or_404(Franchise, id=franchise_id)  # Récupère une franchise ou retourne une erreur 404
    return render(request, 'sondes/franchise_detail.html', {'franchise': franchise})


class FranchiseViewSet(viewsets.ModelViewSet):
    queryset = Franchise.objects.all()
    serializer_class = FranchiseSerializer

class SondaStatusViewSet(viewsets.ModelViewSet):
    queryset = SondaStatus.objects.all()
    serializer_class = SondaStatusSerializer

class ScanReportViewSet(viewsets.ModelViewSet):
    queryset = ScanReport.objects.all()
    serializer_class = ScanReportSerializer

class NetworkLatencyViewSet(viewsets.ModelViewSet):
    queryset = NetworkLatency.objects.all()
    serializer_class = NetworkLatencySerializer

class ApplicationVersionViewSet(viewsets.ModelViewSet):
    queryset = ApplicationVersion.objects.all()
    serializer_class = ApplicationVersionSerializer


    

#Mettre à jour les états des sondes
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.timezone import now

@api_view(['POST'])
def update_sonda_status(request):
    franchise_id = request.data.get('franchise_id')
    status = request.data.get('status')  # "connected" ou "disconnected"

    if not franchise_id or not status:
        return Response({"error": "Franchise ID et statut sont obligatoires"}, status=400)

    try:
        franchise = Franchise.objects.get(id=franchise_id)
        SondaStatus.objects.create(franchise=franchise, status=status, updated_at=now())
        return Response({"message": "Statut mis à jour avec succès"})
    except Franchise.DoesNotExist:
        return Response({"error": "Franchise introuvable"}, status=404)


#Envoyer des mises à jour en temps réel
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Franchise

# Vue pour la page d'accueil
def home(request):
    return HttpResponse("<h1>Bienvenue sur Seahawks Nester</h1><p>Ceci est la page d'accueil de votre projet.</p>")

# Vue pour la liste des franchises
def franchise_list(request):
    franchises = Franchise.objects.all()  # Récupère toutes les franchises

    # Processer les ports ouverts/fermés pour affichage
    for franchise in franchises:
        if franchise.ports_open:
            # Sépare les ports en une liste et ajoute des indicateurs d'état
            ports = franchise.ports_open.split(", ")
            franchise.ports_display = [
                {"port": port, "status": "open" if int(port) < 1024 else "closed"} for port in ports
            ]

    return render(request, 'sondes/franchise_list.html', {'franchises': franchises})

# Vue pour les détails d'une franchise
def franchise_detail(request, franchise_id):
    franchise = get_object_or_404(Franchise, id=franchise_id)  # Récupère une franchise ou retourne une erreur 404
    return render(request, 'sondes/franchise_detail.html', {'franchise': franchise})
