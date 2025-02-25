from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import franchise_change_log  # Vérifie que cette ligne est bien présente
from .views import franchise_change_log, franchise_list  # Import des vues nécessaires
from .views import franchise_devices  # Import de la vue pour les équipements
from .views import (
    FranchiseViewSet, SondaStatusViewSet, ScanReportViewSet,
    NetworkLatencyViewSet, ApplicationVersionViewSet,
    update_sonda_status, franchise_list, franchise_detail
)

# Définition du routeur pour l'API REST
router = DefaultRouter()
router.register(r'franchises', FranchiseViewSet)
router.register(r'sondastatuses', SondaStatusViewSet)
router.register(r'scanreports', ScanReportViewSet)
router.register(r'latencies', NetworkLatencyViewSet)
router.register(r'applicationversions', ApplicationVersionViewSet)

# URL patterns
urlpatterns = [
    # Routes pour les vues Django classiques
    path('', franchise_list, name='franchise_list'),  
    path('<int:franchise_id>/', franchise_detail, name='franchise_detail'),  
    
    # Routes API (Correction : suppression du préfixe `api/` ici)
    path('', include(router.urls)),  


    # Route pour la liste des franchises en HTML
    path('', franchise_list, name='franchise_list'), 

     # Route pour afficher une franchise spécifique
    path('<int:franchise_id>/', franchise_detail, name='franchise_detail'), 
    
    # Route pour mettre à jour l'état des sondes
    path('update-sonda-status/', update_sonda_status, name='update_sonda_status'),

    # Route pour afficher l'historique des changements
    path('change-log/', franchise_change_log, name='franchise_change_log'),

    # Route pour afficher les équipements d'une franchise
    path('franchises/<int:franchise_id>/devices/', franchise_devices, name='franchise_devices'),
    path('<int:franchise_id>/devices/', franchise_devices, name='franchise_devices_shortcut'),  # Nouvelle route


]
