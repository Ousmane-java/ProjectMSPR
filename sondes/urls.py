from django.urls import path, include
from rest_framework.routers import DefaultRouter
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
    
    # Route pour mettre à jour l'état des sondes
    path('update-sonda-status/', update_sonda_status, name='update_sonda_status'),
]
