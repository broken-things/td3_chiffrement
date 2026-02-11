#Import
import sys
import subprocess
import importlib.metadata
import os
import secrets
import paramiko

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


## Dependances ##
def verification():
    # Verification de la version python
    if sys.version_info < (3, 8):
        print(f"Python 3.8+ requis. Version actuelle : {sys.version.split()[0]}")
        return
    print(f"Python {sys.version.split()[0]}")

    # Lecture du requirements.txt
    try:
        with open('requirements.txt', 'r') as f:
            dependances = [line.strip() for line in f if line.strip() and not line.startswith('-')]
    except FileNotFoundError:
        print("Erreur : fichier requirements.txt introuvable.")
        return

    # Verification de la presence des dependances
    manquants = []
    for dependance in dependances:
        try:
            importlib.metadata.version(dependance)
        except importlib.metadata.PackageNotFoundError:
            manquants.append(dependance)

    # Installation des dependances
    if manquants:
        print(f"Dependances manquantes : {', '.join(manquants)}")
        choix = input("Voulez-vous les installer maintenant ? (o/n) : ")

        if choix.lower() == 'o':
            for dependance in manquants:
                try:
                    print(f"Installation de {dependance}...")
                    subprocess.check_call([sys.executable, "-m", "pip", "install", dependance, "--break-system-packages"])
                    print(f"{dependance} installe.")
                except Exception as e:
                    print(f"Erreur lors de l'installation de {dependance} : {e}")
        else:
            print("Installation annulee.")
    else:
        print("Toutes les dependances sont deja presentes.")

## Gestion des cles ##
def gestion_cle():
    print("\n--- GENERATION DE CLE ---")

    # 1. Choix de l'algorithme
    algo_type = ""
    while algo_type not in ['1', '2']:
        print("1. AES")
        print("2. PBKDF2")
        algo_type = input("choix (1 ou 2) : ").strip()
        if algo_type not in (1, 2):
            print("Veuillez saisir 1 ou 2.")

    # 2. Choix de la longueur
    taille_map = {"128": 16, "192": 24, "256": 32}
    print("Longueurs disponibles : 128, 192, 256 bits")
    longueur = input("Longueur de la cle : ").strip()

    if longueur not in taille_map:
        print("Longueur invalide.")
        return

    nb_octets = taille_map[longueur]
    nom_fichier = input("Nom du fichier pour sauvegarder la cle : ")

    try:
        # generation
        if algo_type == '1':
            # Generation AES (octets aleatoires securises)
            cle = secrets.token_bytes(nb_octets)
            print(f"Cle AES {longueur} bits generee.")

        elif algo_type == '2':
            # Generation PBKDF2
            password = input("Entrez le mot de passe pour la derivation : ").encode()
            salt = secrets.token_bytes(16)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=nb_octets,
                salt=salt,
                iterations=100000,
            )
            cle = kdf.derive(password)
            print(f"Cle derivee via PBKDF2 ({longueur} bits) generee.")
        else:
            print("Choix d'algorithme invalide.")
            return

        # Stockage dans /var/keys/
        path = "/var/keys/"
        if not os.path.exists(path):
            os.makedirs(path, mode=0o755, exist_ok=True)

        full_path = os.path.join(path, nom_fichier)

        # Ecriture de la cle
        with os.fdopen(os.open(full_path, os.O_WRONLY | os.O_CREAT, 0o600), 'wb') as f:
            f.write(cle)

        print(f"Succes : Cle stockee dans {full_path}")
        print(f"Permissions : -rw-------")

    except PermissionError:
        print(f"Erreur de permissions impossible d'ecrire dans {path}.")
        print("Lancez le script en 'sudo' ou creez le dossier avec les bons droits.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
    else:
        menu_principal()




## Menu Principal ##

def afficher_menu():
    """Affiche l'interface visuelle du menu."""
    print("\n" + "=" * 30)
    print("Menu principal")
    print("=" * 30)
    print("1. Gestion des cles")
    print("2. Transfert de fichiers")
    print("3. Chiffrement")
    print("4. Quitter")
    print("=" * 30)

def menu_principal():
    while True:
        afficher_menu()
        choix = input("Choisissez une option (1-4) : ").strip()

        if choix == '1':
            print("\n[Action] Accès à la gestion des cles")
            gestion_cle()
            input("\nAppuyez sur Entree pour revenir au menu...")

        elif choix == '2':
            print("\n[Action] Transfert de fichiers")

            input("\nAppuyez sur Entree pour revenir au menu...")

        elif choix == '3':
            print("\n[Action] Module de chiffrement")
            input("\nAppuyez sur Entree pour revenir au menu...")

        elif choix == '4':
            print("Fermeture du programme.")
            break  # Sortie de la boucle while

        else:
            print(f"\nErreur : '{choix}' n'est pas une option valide. Veuillez saisir un chiffre entre 1 et 4.")



if __name__ == "__main__":
    verification()
    menu_principal()