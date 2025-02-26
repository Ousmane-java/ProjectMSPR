from django.core.management.base import BaseCommand
from sondes.models import Franchise
import nmap

class Command(BaseCommand):
    help = "Ajouter des machines et scanner le réseau"

    def handle(self, *args, **kwargs):
        # Création des franchises
        machines = [
            {"name": "MacBook Host", "ip_address": "172.16.49.1", "location": "MacBook Pro", "status": "connected"},
            {"name": "Ubuntu VM", "ip_address": "172.16.49.149", "location": "VMware", "status": "connected"},
            {"name": "Kali VM", "ip_address": "172.16.49.137", "location": "VMware", "status": "connected"},
        ]
        
        # Ajouter les machines à la base de données si elles n'existent pas
        for machine in machines:
            Franchise.objects.get_or_create(**machine)
            self.stdout.write(self.style.SUCCESS(f"Machine {machine['name']} ajoutée à la base de données"))

        # Scanner le réseau pour obtenir des informations sur les ports ouverts
        scanner = nmap.PortScanner()

        for machine in machines:
            ip = machine["ip_address"]
            self.stdout.write(f"Scanning {ip}...")

            # Lancer un scan sur l'IP donnée
            scanner.scan(ip, '22-443')  # Exemple de port range: de 22 à 443

            # Afficher les résultats du scan
            if scanner.all_hosts():
                for host in scanner.all_hosts():
                    self.stdout.write(f"Host : {host} ({scanner[host].hostname()})")
                    self.stdout.write(f"  State  : {scanner[host].state()}")
                    for proto in scanner[host].all_protocols():
                        lport = scanner[host][proto].keys()
                        for port in lport:
                            self.stdout.write(f"  Port : {port}  State : {scanner[host][proto][port]['state']}")
            else:
                self.stdout.write(f"Pas de réponse de {ip}")
