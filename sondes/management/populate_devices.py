import random
from django.utils.timezone import now
from sondes.models import Franchise, NetworkDevice

# Liste des types d'équipements possibles
DEVICE_TYPES = ["server", "router", "switch", "firewall", "access point", "load balancer", "modem"]

# Fonction pour générer une adresse IP aléatoire
def generate_random_ip():
    return f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"

# Ajouter 15 équipements à chaque franchise
def populate_devices():
    franchises = Franchise.objects.all()
    
    for franchise in franchises:
        for _ in range(15):  # Ajouter 15 équipements
            device_name = f"{random.choice(['Alpha', 'Beta', 'Gamma', 'Delta', 'Sigma'])}-{random.randint(1, 100)}"
            device_type = random.choice(DEVICE_TYPES)
            ip_address = generate_random_ip()
            status = random.choice(["online", "offline"])

            NetworkDevice.objects.create(
                franchise=franchise,
                name=device_name,
                device_type=device_type,
                ip_address=ip_address,
                status=status,
                last_modified=now()
            )

        print(f"✅ Ajout de 15 équipements pour {franchise.name}")

    print("🚀 Tous les équipements ont été ajoutés avec succès !")

# Exécuter la fonction
populate_devices()
