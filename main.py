#Import
import sys
import subprocess
import importlib.metadata
import os

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

## Menu Principal ##

def afficher_menu():
    """Affiche l'interface visuelle du menu."""
    print("\n" + "=" * 30)
    print("Menu principal")
    print("=" * 30)
    print("1. Gestion des clés")
    print("2. Transfert de fichiers")
    print("3. Chiffrement")
    print("4. Quitter")
    print("=" * 30)


def menu_principal():
    while True:
        afficher_menu()
        choix = input("Choisissez une option (1-4) : ").strip()

        if choix == '1':
            print("\n[Action] Accès à la gestion des clés")
            # Appeler la fonction de la Partie C ici
            input("\nAppuyez sur Entrée pour revenir au menu...")

        elif choix == '2':
            print("\n[Action] Transfert de fichiers")
            # Appeler la fonction de la Partie D ici
            input("\nAppuyez sur Entrée pour revenir au menu...")

        elif choix == '3':
            print("\n[Action] Module de chiffrement")
            input("\nAppuyez sur Entrée pour revenir au menu...")

        elif choix == '4':
            print("Fermeture du programme.")
            break  # Sortie de la boucle while

        else:
            print(f"\nErreur : '{choix}' n'est pas une option valide. Veuillez saisir un chiffre entre 1 et 4.")

if __name__ == "__main__":
    verification()
    menu_principal()