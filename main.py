#Import
import sys
import subprocess
import importlib.metadata

## Installation des dependances ##
def verification():
    # Vérification Python version python
    if sys.version_info < (3, 8):
        print(f"Python 3.8+ requis. Version actuelle : {sys.version.split()[0]}")
        return
    print(f"Python {sys.version.split()[0]}")

    # Lecture de requirements.txt
    try:
        with open('requirements.txt', 'r') as f:
            dependances = [line.strip() for line in f if line.strip() and not line.startswith('-')]
    except FileNotFoundError:
        print("Erreur : fichier requirements.txt introuvable.")
        return

    # Verification des dependances
    manquants = []
    for dependance in dependances:
        try:
            # On vérifie si le package est installé
            importlib.metadata.version(dependance)
        except importlib.metadata.PackageNotFoundError:
            manquants.append(dependance)

    # Installation
    if manquants:
        print(f"Dependances manquantes : {', '.join(manquants)}")
        choix = input("Voulez-vous les installer maintenant ? (o/n) : ")

        if choix.lower() == 'o':
            for dependance in manquants:
                try:
                    print(f"Installation de {dependance}...")
                    subprocess.check_call([sys.executable, "-m", "pip", "install", dependance])
                    print(f"{dependance} installé.")
                except Exception as e:
                    print(f"Erreur lors de l'installation de {dependance} : {e}")
        else:
            print("Installation annulée.")
    else:
        print("Toutes les dépendances sont déjà présentes.")
if __name__ == "__main__":
    verification()