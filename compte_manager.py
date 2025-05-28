import os
import json
import time
from config import UTILISATEUR_PATH, SESSION_DIR, LOGS_DIR

def gestion_comptes():
    while True:
        print("\n=== Gestion des comptes Instagram ===")
        print("1. Ajouter un compte")
        print("2. Lister les comptes")
        print("3. Supprimer un compte")
        print("4. Nettoyer les sessions orphelines")
        print("0. Retour menu principal")
        choix = input("\nVotre choix : ").strip()
        if choix == "1":
            ajouter_compte()
        elif choix == "2":
            lister_comptes()
        elif choix == "3":
            supprimer_compte()
        elif choix == "4":
            nettoyer_sessions()
        elif choix == "0":
            break
        else:
            print("Choix invalide.")

def ajouter_compte():
    print("\n=== Ajouter un compte Instagram ===")
    username = input("Nom d'utilisateur Instagram : ").strip()
    password = input("Mot de passe Instagram : ").strip()
    if not username or not password:
        print("Champs obligatoires.")
        return
    comptes = []
    if os.path.exists(UTILISATEUR_PATH):
        with open(UTILISATEUR_PATH, "r") as f:
            comptes = json.load(f)
    for item in comptes:
        if username in item:
            print("Ce compte existe déjà.")
            return
    comptes.append({username: password})
    with open(UTILISATEUR_PATH, "w") as f:
        json.dump(comptes, f, indent=2)
    print("Compte ajouté.")

def lister_comptes():
    print("\n=== Liste des comptes ===")
    if not os.path.exists(UTILISATEUR_PATH):
        print("Aucun compte enregistré.")
        return
    with open(UTILISATEUR_PATH, "r") as f:
        comptes = json.load(f)
    for item in comptes:
        for u in item:
            print("-", u)

def supprimer_compte():
    print("\n=== Supprimer un compte ===")
    if not os.path.exists(UTILISATEUR_PATH):
        print("Aucun compte enregistré.")
        return
    with open(UTILISATEUR_PATH, "r") as f:
        comptes = json.load(f)
    usernames = [list(item.keys())[0] for item in comptes]
    for i, u in enumerate(usernames, 1):
        print(f"{i}. {u}")
    num = input("Numéro du compte à supprimer : ").strip()
    if not num.isdigit() or not (1 <= int(num) <= len(usernames)):
        print("Numéro invalide.")
        return
    idx = int(num) - 1
    suppr = usernames[idx]
    comptes = [item for item in comptes if suppr not in item]
    with open(UTILISATEUR_PATH, "w") as f:
        json.dump(comptes, f, indent=2)
    print("Compte supprimé.")

def nettoyer_sessions():
    print("\nNettoyage des sessions orphelines...")
    if not os.path.exists(SESSION_DIR):
        print("Aucune session à nettoyer.")
        return
    comptes = []
    if os.path.exists(UTILISATEUR_PATH):
        with open(UTILISATEUR_PATH, "r") as f:
            comptes = json.load(f)
    users = {list(item.keys())[0] for item in comptes}
    for session_file in os.listdir(SESSION_DIR):
        username = os.path.splitext(session_file)[0]
        if username not in users:
            os.remove(os.path.join(SESSION_DIR, session_file))
            print(f"Session orpheline supprimée : {session_file}")
    print("Nettoyage terminé.")
