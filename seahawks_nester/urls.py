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
from django.urls import path
from sondes import views  # Importer les vues de votre app sondes
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),  # URL pour accéder à l'interface admin
    path('', views.home, name='home'),  # Vue par défaut pour l'URL racine
    path('sondes/', include('sondes.urls')),  # Inclure les URLs de l'app sondes
]
