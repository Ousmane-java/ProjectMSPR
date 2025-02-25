import json
import logging
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.timezone import now, timedelta
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.shortcuts import render
from .models import FranchiseChangeLog
from .models import Franchise, SondaStatus, ScanReport, NetworkLatency, ApplicationVersion
from .serializers import FranchiseSerializer, SondaStatusSerializer, ScanReportSerializer, NetworkLatencySerializer, ApplicationVersionSerializer
from .models import Franchise, NetworkDevice

logger = logging.getLogger(__name__)

# 📌 Vue pour la page d'accueil
def home(request):
    return HttpResponse("<h1>Bienvenue sur Seahawks Nester</h1><p>Ceci est la page d'accueil de votre projet.</p>")

# 📌 Vue pour la liste des franchises
def franchise_list(request):
    franchises = Franchise.objects.all()

    # Récupérer leur dernier statut depuis la table SondaStatus
    for franchise in franchises:
        last_status = franchise.sonda_status.order_by('-updated_at').first()
        franchise.status = last_status.status if last_status else "connected"  # Connected par défaut
        franchise.recently_modified = franchise.is_recently_modified()

        # Vérifier si la modification de l'IP ou des ports date de moins de 2 heures
        franchise.recently_modified_ip = False
        franchise.recently_modified_ports = False

        if franchise.last_modified:
            time_since_modification = now() - franchise.last_modified

            if time_since_modification < timedelta(hours=2):
                # Vérifier si c'est une modification de l'IP ou des ports
                if franchise.ip_address_last_modified and time_since_modification < timedelta(hours=2):
                    franchise.recently_modified_ip = True
                
                if franchise.ports_open_last_modified and time_since_modification < timedelta(hours=2):
                    franchise.recently_modified_ports = True

    return render(request, 'sondes/franchise_list.html', {'franchises': franchises})

# 📌 Vue pour les détails d'une franchise
def franchise_detail(request, franchise_id):
    franchise = get_object_or_404(Franchise, id=franchise_id)
    return render(request, 'sondes/franchise_detail.html', {'franchise': franchise})

# 📌 API REST ViewSets
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

# 📌 Mettre à jour les états des sondes et envoyer des mises à jour WebSocket
@api_view(['POST'])
def update_sonda_status(request):
    franchise_id = request.data.get('franchise_id')
    status = request.data.get('status')  # "connected" ou "disconnected"

    if not franchise_id or not status:
        return Response({"error": "Franchise ID et statut sont obligatoires"}, status=400)

    try:
        franchise = Franchise.objects.get(id=franchise_id)
        
        # Mise à jour du statut directement sur la franchise
        franchise.status = status
        franchise.save()

        # Enregistrement dans la table SondaStatus pour garder un historique
        SondaStatus.objects.create(franchise=franchise, status=status, updated_at=now())

        # 📌 Envoi d'une mise à jour WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "sonda_updates",
            {
                "type": "sonda_status_update",
                "franchise_id": franchise.id,
                "status": status
            }
        )

        logger.info(f"Statut mis à jour pour {franchise.name}: {status}")
        return Response({"message": "Statut mis à jour avec succès"})
    except Franchise.DoesNotExist:
        return Response({"error": "Franchise introuvable"}, status=404)

# 📌 Mettre à jour les informations IP et Ports avec un marquage temporaire
@api_view(['POST'])
def update_franchise_info(request):
    """
    Met à jour les informations d'une franchise (IP et Ports) 
    et marque les changements comme temporaires.
    """
    franchise_id = request.data.get('franchise_id')
    new_ip = request.data.get('ip_address')
    new_ports = request.data.get('ports_open')

    if not franchise_id:
        return Response({"error": "Franchise ID est obligatoire"}, status=400)

    try:
        franchise = Franchise.objects.get(id=franchise_id)
        update_needed = False

        # Vérifier si l'IP a changé
        if new_ip and new_ip != franchise.ip_address:
            franchise.ip_address = new_ip
            franchise.ip_address_last_modified = now()  # Mise à jour spécifique pour l'IP
            update_needed = True

        # Vérifier si les ports ont changé
        if new_ports and new_ports != franchise.ports_open:
            franchise.ports_open = new_ports
            franchise.ports_open_last_modified = now()  # Mise à jour spécifique pour les ports
            update_needed = True

        if update_needed:
            franchise.last_modified = now()  # Marquer la mise à jour
            franchise.save()

            # 📌 Envoi d'une mise à jour WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "franchise_updates",
                {
                    "type": "franchise_update",
                    "franchise_id": franchise.id,
                    "ip_address": new_ip,
                    "ports_open": new_ports
                }
            )

            # Marquer le changement temporaire (ex: retour à la valeur par défaut après 2h)
            expiration_time = now() + timedelta(hours=2)
            franchise.last_modified = expiration_time
            franchise.save()

            return Response({"message": "Mise à jour effectuée avec succès, retour automatique dans 2h"})
        else:
            return Response({"message": "Aucune modification détectée"})

    except Franchise.DoesNotExist:
        return Response({"error": "Franchise introuvable"}, status=404)
    
from .models import Franchise, FranchiseChangeLog

def franchise_change_log(request):
    """Affiche l'historique des changements de ports et d'IP des franchises."""
    change_logs = FranchiseChangeLog.objects.all().order_by('-changed_at')
    return render(request, 'sondes/franchise_change_log.html', {'change_logs': change_logs})

def franchise_devices(request, franchise_id):
    """
    Vue pour afficher tous les équipements d'une franchise spécifique.
    """
    franchise = get_object_or_404(Franchise, id=franchise_id)
    devices = franchise.network_devices.all()  # Récupérer tous les équipements associés

    return render(request, 'sondes/franchise_devices.html', {'franchise': franchise, 'devices': devices})
