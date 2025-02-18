import os
import sys
import django

# Ajouter le répertoire principal du projet au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurer Django pour exécuter le script
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seahawks_nester.settings')
django.setup()

from sondes.models import Franchise
import csv

# Chemin vers le fichier CSV
file_path = 'franchises_data.csv'

# Importer les données du fichier CSV
def import_csv():
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Créez ou mettez à jour une franchise
            Franchise.objects.update_or_create(
                name=row['Nom'],
                defaults={
                    'ip_address': row['Adresse IP'],
                    'location': row['Localisation'],
                    'contact_person': row['Contact'],
                    'contact_email': row['Email'],
                    'contact_phone': row['Téléphone'],
                    'sondes': row['Sondes'],
                    'ports_open': row['Ports ouverts'],
                }
            )
    print("Importation terminée avec succès !")

if __name__ == '__main__':
    import_csv()
