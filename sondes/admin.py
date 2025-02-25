from django.contrib import admin
from django.utils.timezone import now
from .models import Franchise, NetworkDevice, FranchiseChangeLog, ScanReport, SondaStatus, NetworkLatency, ApplicationVersion

class NetworkDeviceInline(admin.TabularInline):
    """Permet d'ajouter des équipements réseau directement dans l'admin de Franchise."""
    model = NetworkDevice
    extra = 1  # Permet d'ajouter plusieurs équipements


class FranchiseAdmin(admin.ModelAdmin):
    """Configuration de l'affichage de la Franchise dans l'admin."""
    list_display = ("name", "ip_address", "ports_open", "status", "last_modified")
    list_filter = ("status",)
    search_fields = ("name", "ip_address")
    ordering = ("name",)
    inlines = [NetworkDeviceInline]  # Permet d'ajouter des équipements réseau depuis l'admin

    def save_model(self, request, obj, form, change):
        """
        Surcharge la sauvegarde pour détecter si IP ou Ports ont changé et enregistrer dans FranchiseChangeLog.
        """
        if change:  # Vérifie s'il s'agit d'une modification existante
            old_instance = Franchise.objects.get(pk=obj.pk)

            if old_instance.ip_address != obj.ip_address or old_instance.ports_open != obj.ports_open:
                # Enregistrer l'ancien et le nouveau changement dans FranchiseChangeLog
                FranchiseChangeLog.objects.create(
                    franchise=obj,
                    old_ip_address=old_instance.ip_address,
                    new_ip_address=obj.ip_address,
                    old_ports_open=old_instance.ports_open,
                    new_ports_open=obj.ports_open
                )

            obj.last_modified = now()  # Met à jour la dernière modification

        super().save_model(request, obj, form, change)


# 📌 Vérifier que le modèle Franchise n'est pas déjà enregistré avant de l'ajouter
if not admin.site.is_registered(Franchise):
    admin.site.register(Franchise, FranchiseAdmin)

# 📌 Enregistrement des autres modèles dans l'interface d'administration Django
admin.site.register(NetworkDevice)
admin.site.register(FranchiseChangeLog)
admin.site.register(ScanReport)
admin.site.register(SondaStatus)
admin.site.register(NetworkLatency)
admin.site.register(ApplicationVersion)
