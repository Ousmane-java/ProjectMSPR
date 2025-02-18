from django.db import models

class Franchise(models.Model):
    """Représente une franchise (client)."""
    name = models.CharField(max_length=100, unique=True, help_text="Nom de la franchise")
    ip_address = models.GenericIPAddressField(help_text="Adresse IP de la franchise")
    location = models.CharField(max_length=255, blank=True, null=True, help_text="Localisation de la franchise")
    last_seen = models.DateTimeField(auto_now=True, help_text="Dernière activité enregistrée")
    contact_person = models.CharField(max_length=100, blank=True, null=True, help_text="Personne à contacter")
    contact_email = models.EmailField(blank=True, null=True, help_text="Email de contact")
    contact_phone = models.CharField(max_length=20, blank=True, null=True, help_text="Téléphone de contact")
    sondes = models.TextField(blank=True, null=True, help_text="Liste des sondes en format texte")
    ports_open = models.CharField(max_length=255, blank=True, null=True, help_text="Liste des ports ouverts")

    def __str__(self):
        return self.name


class ScanReport(models.Model):
    """Rapport de scan réseau effectué par une franchise."""
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE, related_name='scan_reports')
    scan_data = models.JSONField(help_text="Résultats du scan en format JSON (machines connectées, ports)")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date du scan")

    def __str__(self):
        return f"Rapport de scan pour {self.franchise.name} le {self.created_at}"


class SondaStatus(models.Model):
    """État de la connectivité des sondes (clients Seahawks Harvester)."""
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE, related_name='sonda_status')
    status = models.CharField(max_length=20, choices=[('connected', 'Connecté'), ('disconnected', 'Déconnecté')], default='disconnected', help_text="Statut de la sonde")
    updated_at = models.DateTimeField(auto_now=True, help_text="Dernière mise à jour du statut")

    def __str__(self):
        return f"{self.franchise.name} - {self.status}"


class NetworkLatency(models.Model):
    """Latence WAN enregistrée par une franchise."""
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE, related_name='latencies')
    latency = models.FloatField(help_text="Latence moyenne (ms)")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="Date et heure de la mesure")

    def __str__(self):
        return f"Latence pour {self.franchise.name} : {self.latency} ms"


class ApplicationVersion(models.Model):
    """Version de l'application installée sur une franchise."""
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE, related_name='application_versions')
    version = models.CharField(max_length=50, help_text="Version de l'application déployée")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date de mise à jour")

    def __str__(self):
        return f"Version {self.version} pour {self.franchise.name}"
