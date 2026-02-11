# Projet : SSH Toolbox & Chiffrement In-Place

Ce projet est un outil de chiffrement écrit en Python. Il permet de gérer le cycle de vie de la sécurité des fichiers : de la génération de clés cryptographiques au transfert sécurisé (SFTP), jusqu'au chiffrement local des données.



## 🛠Fonctionnalités

Le script est divisé en 5 parties principales :

* **Partie A - Vérification :** Contrôle de la version de Python (3.8+) et gestion automatique des dépendances via `requirements.txt`.
* **Partie B - Menu :** Interface textuelle interactive avec validation stricte des saisies utilisateur.
* **Partie C - Gestion des Clés :** * Génération de clés **AES** ou **PBKDF2**.
    * Choix de la longueur (128, 192, 256 bits).
    * Stockage sécurisé avec permissions restreintes (**chmod 600**).
* **Partie D - Transfert SFTP :**
    * Connexion SSH sécurisée (Paramiko).
    * Transfert de la clé de chiffrement vers le serveur distant.
    * Sélection libre et multiple de fichiers ou dossiers à transférer.
    * Barre de progression visuelle intégrée.
* **Partie E - Chiffrement :**
    * Chiffrement symétrique **Fernet** (basé sur AES-128 et HMAC).
    * Mode "In-place" : le fichier original est remplacé par sa version chiffrée.
    * Support des fichiers individuels et des dossiers complets (récursif).

---

## Prérequis

Pour utiliser cet outil, vous devez disposer de :
* **Python 3.8** ou supérieur.
* Un accès réseau au serveur distant pour les fonctions SFTP.
* Le fichier `requirements.txt` contenant :
    ```text
    cryptography
    paramiko
    setuptools
    ```

---

## Installation et Lancement

1.  **Cloner ou copier** les fichiers `main.py` et `requirements.txt` dans un dossier.
2.  **Lancer le script** :
    ```bash
    sudo python3 main.py
    ```
3.  **Dépendances** : Au premier lancement, acceptez l'installation des modules si le script vous le demande.

---

## Guide d'Utilisation

### 1. Génération de Clés
Le script tente de sauvegarder les clés dans `/var/keys/`. Si vous n'avez pas les droits `sudo`, il créera automatiquement un dossier `./keys/` dans le répertoire actuel.


### 2. Transfert SFTP
* Connectez-vous au serveur via son IP et vos identifiants.
* Transférez d'abord la clé pour que le serveur puisse (plus tard) traiter les fichiers.
* Saisissez les chemins des fichiers/dossiers à envoyer. Tapez **"ok"** quand votre sélection est terminée pour lancer l'envoi groupé.

### 3. Chiffrement
Indiquez le chemin de votre clé et la cible. 
> **Attention :** Le chiffrement remplace le fichier original. Assurez-vous de conserver votre clé en lieu sûr, sans quoi les données seront définitivement perdues.


[Image of AES encryption process diagram]


---

## Sécurité et Bonnes Pratiques

* **Permissions :** L'utilisation de `os.open` avec le mode `0o600` garantit que seul le propriétaire peut lire les clés générées.
* **Confidentialité :** Les mots de passe saisis ne sont jamais stockés en clair et les échanges réseau sont protégés par le protocole SSH.
* **Validation :** Chaque entrée utilisateur est vérifiée par une boucle de contrôle pour éviter les plantages du script.

---