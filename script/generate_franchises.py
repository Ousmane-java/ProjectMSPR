import pandas as pd

# Création des données pour les 18 franchises
franchises = [
    {"Nom": "Franchise Paris 1", "Adresse IP": "192.168.1.10", "Localisation": "Paris, France",
     "Contact": "Jean Dupont", "Email": "jean.dupont@paris1.com", "Téléphone": "+33 6 12 34 56 78",
     "Sondes": "Sonda 1: En ligne; Sonda 2: Hors ligne", "Ports ouverts": "80, 443, 22"},
    {"Nom": "Franchise Marseille 1", "Adresse IP": "192.168.1.11", "Localisation": "Marseille, France",
     "Contact": "Marie Dubois", "Email": "marie.dubois@marseille1.com", "Téléphone": "+33 6 98 76 54 32",
     "Sondes": "Sonda 1: En ligne; Sonda 2: En ligne", "Ports ouverts": "80, 443, 3306"},
    {"Nom": "Franchise Lyon 1", "Adresse IP": "192.168.1.12", "Localisation": "Lyon, France",
     "Contact": "Jacques Martin", "Email": "jacques.martin@lyon1.com", "Téléphone": "+33 6 22 33 44 55",
     "Sondes": "Sonda 1: En ligne", "Ports ouverts": "22, 3389"},
    {"Nom": "Franchise Bordeaux 1", "Adresse IP": "192.168.1.13", "Localisation": "Bordeaux, France",
     "Contact": "Alice Renault", "Email": "alice.renault@bordeaux1.com", "Téléphone": "+33 6 11 22 33 44",
     "Sondes": "Sonda 1: En ligne; Sonda 2: Hors ligne", "Ports ouverts": "443, 25, 110"},
    {"Nom": "Franchise Lille 1", "Adresse IP": "192.168.1.14", "Localisation": "Lille, France",
     "Contact": "Paul Lefevre", "Email": "paul.lefevre@lille1.com", "Téléphone": "+33 6 99 88 77 66",
     "Sondes": "Sonda 1: Hors ligne", "Ports ouverts": "80, 443, 21"},
] + [{"Nom": f"Franchise Générique {i}", "Adresse IP": f"192.168.2.{i}", "Localisation": f"Ville Générique {i}, France",
      "Contact": f"Contact {i}", "Email": f"contact{i}@generic{i}.com", "Téléphone": f"+33 6 {i}2 34 56 78",
      "Sondes": f"Sonda 1: En ligne; Sonda 2: Hors ligne", "Ports ouverts": "22, 443"}
     for i in range(6, 19)]

# Convertir les données en DataFrame
df = pd.DataFrame(franchises)

# Sauvegarder dans un fichier CSV
df.to_csv("franchises_data.csv", index=False)

print("Le fichier CSV a été créé : franchises_data.csv")
