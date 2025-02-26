from django.db import models
from django.utils.timezone import now, timedelta

class Franchise(models.Model):
    """Représente une franchise (client Seahawks Harvester)."""
    
    name = models.CharField(max_length=100, unique=True, help_text="Nom de la franchise")
    ip_address = models.GenericIPAddressField(help_text="Adresse IP de la franchise")
    location = models.CharField(max_length=255, blank=True, null=True, help_text="Localisation")
    ports_open = models.CharField(max_length=255, blank=True, null=True, help_text="Liste des ports ouverts")
    
    # Suivi des modifications
    last_modified = models.DateTimeField(null=True, blank=True, help_text="Dernière mise à jour générale")  
    ip_address_last_modified = models.DateTimeField(null=True, blank=True, help_text="Dernière modification de l'IP")
    ports_open_last_modified = models.DateTimeField(null=True, blank=True, help_text="Dernière modification des ports")

    # Contact
    contact_person = models.CharField(max_length=100, blank=True, null=True, help_text="Contact principal")
    contact_email = models.EmailField(blank=True, null=True, help_text="Email du contact")
    contact_phone = models.CharField(max_length=20, blank=True, null=True, help_text="Téléphone")
    
    last_seen = models.DateTimeField(auto_now=True, help_text="Dernière activité")

    # Statut de la franchise
    STATUS_CHOICES = [
        ("connected", "Connecté"),
        ("disconnected", "Déconnecté"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="connected", help_text="État actuel de la franchise")

    def is_recently_modified(self):
        """Retourne True si l'IP ou les ports ont été modifiés dans les 2 dernières heures."""
        two_hours_ago = now() - timedelta(hours=2)
        return (
            (self.ip_address_last_modified and self.ip_address_last_modified >= two_hours_ago) or
            (self.ports_open_last_modified and self.ports_open_last_modified >= two_hours_ago)
        )

    def __str__(self):
        return f"{self.name} - {self.status}"


class NetworkDevice(models.Model):
    """Équipement réseau (serveur, switch, routeur) appartenant à une franchise."""
    
    DEVICE_TYPES = [
        ("server", "Serveur"),
        ("router", "Routeur"),
        ("switch", "Switch"),
        ("firewall", "Pare-feu"),
    ]

    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE, related_name="network_devices")
    name = models.CharField(max_length=100, help_text="Nom de l'équipement")
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPES, help_text="Type d'équipement")
    ip_address = models.GenericIPAddressField(help_text="Adresse IP de l'équipement")
    status = models.CharField(max_length=20, choices=[("online", "En ligne"), ("offline", "Hors ligne")], default="online")
    last_modified = models.DateTimeField(auto_now=True, help_text="Dernière mise à jour")

    def __str__(self):
        return f"{self.name} ({self.device_type}) - {self.franchise.name}"


class FranchiseChangeLog(models.Model):
    """Stocke l'historique des modifications de l'IP et des ports ouverts d'une franchise."""
    
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE, related_name="change_logs")
    old_ip_address = models.GenericIPAddressField(blank=True, null=True, help_text="Ancienne adresse IP")
    new_ip_address = models.GenericIPAddressField(blank=True, null=True, help_text="Nouvelle adresse IP")
    old_ports_open = models.CharField(max_length=255, blank=True, null=True, help_text="Anciens ports ouverts")
    new_ports_open = models.CharField(max_length=255, blank=True, null=True, help_text="Nouveaux ports ouverts")
    changed_at = models.DateTimeField(auto_now_add=True, help_text="Date et heure du changement")

    def __str__(self):
        return f"Changement {self.franchise.name} - {self.changed_at.strftime('%Y-%m-%d %H:%M:%S')}"


class ScanReport(models.Model):
    """Rapport de scan réseau effectué par une franchise."""
    
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE, related_name='scan_reports')
    scan_data = models.JSONField(help_text="Résultats du scan en format JSON (machines connectées, ports)")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date du scan")

    def __str__(self):
        return f"Scan pour {self.franchise.name} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"


class SondaStatus(models.Model):
    """État de la connectivité des sondes (clients Seahawks Harvester)."""
    
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE, related_name='sonda_status')
    status = models.CharField(max_length=20, choices=[('connected', 'Connecté'), ('disconnected', 'Déconnecté')], default='connected', help_text="Statut de la sonde")
    updated_at = models.DateTimeField(auto_now=True, help_text="Dernière mise à jour du statut")

    def __str__(self):
        return f"{self.franchise.name} - {self.status}"


class NetworkLatency(models.Model):
    """Latence WAN enregistrée par une franchise."""
    
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE, related_name='latencies')
    latency = models.FloatField(help_text="Latence moyenne (ms)")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="Date et heure de la mesure")

    def __str__(self):
        return f"Latence {self.latency} ms - {self.franchise.name} ({self.timestamp.strftime('%Y-%m-%d %H:%M:%S')})"


class ApplicationVersion(models.Model):
    """Version de l'application installée sur une franchise."""
    
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE, related_name='application_versions')
    version = models.CharField(max_length=50, help_text="Version de l'application déployée")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date de mise à jour")

    def __str__(self):
        return f"Version {self.version} - {self.franchise.name} ({self.updated_at.strftime('%Y-%m-%d %H:%M:%S')})"


class NetworkScan(models.Model):
    """Stocke les résultats des scans réseau."""
    
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE, related_name="network_scans")
    ip_address = models.GenericIPAddressField(help_text="Adresse IP scannée")
    open_ports = models.TextField(blank=True, null=True, help_text="Liste des ports ouverts")
    services = models.TextField(blank=True, null=True, help_text="Services détectés sur la machine")
    os_detected = models.CharField(max_length=255, blank=True, null=True, help_text="Système d'exploitation détecté")
    vulnerabilities = models.TextField(blank=True, null=True, help_text="Liste des vulnérabilités détectées")
    latency = models.FloatField(blank=True, null=True, help_text="Temps de réponse en ms")
    scan_time = models.DateTimeField(default=now, help_text="Date et heure du scan")

    def __str__(self):
        return f"Scan de {self.franchise.name} - {self.ip_address} ({self.scan_time})"
