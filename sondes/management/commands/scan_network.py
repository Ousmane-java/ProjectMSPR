import nmap
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from sondes.models import Franchise, NetworkScan

class Command(BaseCommand):
    help = "Scanne le réseau et enregistre les résultats."

    def handle(self, *args, **kwargs):
        nm = nmap.PortScanner()
        franchises = Franchise.objects.all()

        for franchise in franchises:
            try:
                print(f"🔍 Scan de {franchise.name} ({franchise.ip_address}) en cours...")
                nm.scan(franchise.ip_address, arguments="-p 1-65535 -O -sV")  # Détection OS + Scan des services

                if franchise.ip_address not in nm.all_hosts():
                    print(f"❌ Aucun hôte trouvé pour {franchise.name}")
                    continue

                open_ports = []
                services = []
                os_detected = "Inconnu"
                vulnerabilities = []
                latency = None

                # 🔹 Détecter les ports ouverts et services actifs
                for port, info in nm[franchise.ip_address].get("tcp", {}).items():
                    if info["state"] == "open":
                        open_ports.append(str(port))
                        service_name = info.get("name", "Inconnu")
                        service_version = info.get("version", "Inconnu")
                        services.append(f"{port}/{service_name} ({service_version})")

                # 🔹 Détection du système d'exploitation
                if "osmatch" in nm[franchise.ip_address]:
                    os_matches = nm[franchise.ip_address]["osmatch"]
                    if os_matches:
                        os_detected = os_matches[0]["name"]

                # 🔹 Vérifier la latence réseau
                if "times" in nm[franchise.ip_address]:
                    latency = nm[franchise.ip_address]["times"].get("srtt", 0) / 1000.0  # Convertir en ms

                # 🔹 Détection de vulnérabilités basiques
                vuln_ports = {
                    21: "⚠️ FTP (port 21) peut être vulnérable.",
                    23: "⚠️ Telnet (port 23) non sécurisé.",
                    3389: "⚠️ RDP (port 3389) peut être à risque.",
                }
                for port in open_ports:
                    if int(port) in vuln_ports:
                        vulnerabilities.append(vuln_ports[int(port)])

                # 🔹 Enregistrement des résultats
                NetworkScan.objects.create(
                    franchise=franchise,
                    ip_address=franchise.ip_address,
                    open_ports=", ".join(open_ports) if open_ports else "Aucun",
                    services=", ".join(services) if services else "Aucun",
                    os_detected=os_detected,
                    vulnerabilities=", ".join(vulnerabilities) if vulnerabilities else "Aucune",
                    latency=latency,
                    scan_time=now()
                )

                # 🔹 Affichage des résultats
                print(f"✅ Résultat pour {franchise.name} ({franchise.ip_address}):")
                print(f"   - Ports ouverts : {', '.join(open_ports) if open_ports else 'Aucun'}")
                print(f"   - Services actifs : {', '.join(services) if services else 'Aucun'}")
                print(f"   - OS détecté : {os_detected}")
                print(f"   - Vulnérabilités : {', '.join(vulnerabilities) if vulnerabilities else 'Aucune'}")
                print(f"   - Latence : {latency} ms\n")

            except Exception as e:
                print(f"❌ Erreur lors du scan de {franchise.name}: {e}")

        self.stdout.write(self.style.SUCCESS("✅ Scan terminé avec succès !"))
