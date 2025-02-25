"""
URL configuration for seahawks_nester project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from sondes.views import home  # Import de la vue home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('sondes.urls')),  # API REST pour les franchises
    path('sondes/', include('sondes.urls')),  # Ajout de l'application sondes
    path('', home, name='home'),  # Page d'accueil principale
]

