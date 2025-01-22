from django.urls import path
from . import views

urlpatterns = [
    path('', views.franchise_list, name='franchise_list'),  # Liste des franchises
    path('<int:franchise_id>/', views.franchise_detail, name='franchise_detail'),  # Détails d'une franchise
]
