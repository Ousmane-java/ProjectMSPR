from django.contrib import admin
from .models import Franchise, ScanReport, SondaStatus, NetworkLatency, ApplicationVersion

# Enregistrer les modèles dans l'administration
admin.site.register(Franchise)
admin.site.register(ScanReport)
admin.site.register(SondaStatus)
admin.site.register(NetworkLatency)
admin.site.register(ApplicationVersion)
