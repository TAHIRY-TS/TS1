import os
import json
import webbrowser

CONFIG_PATH = "config.json"

def create_config():
    print("Fichier config.json manquant.")
    print("Vous devez créer une application Telegram pour obtenir vos identifiants.")
    print("Ouverture de https://my.telegram.org dans votre navigateur...")
    webbrowser.open("https://my.telegram.org")
    api_id = input("Entrez votre api_id Telegram : ").strip()
    api_hash = input("Entrez votre api_hash Telegram : ").strip()
    config = {
        "api_id": api_id,
        "api_hash": api_hash,
        "session": ""
    }
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
    print("Fichier config.json créé avec succès !")

def main():
    if not os.path.exists(CONFIG_PATH):
        create_config()
    # Ici, appelez votre fonction de connexion automatique ou l'automatisation du bot
    print("Connexion automatique en cours...")
    # from auto_task import auto_task_main
    # auto_task_main()  # décommentez si vous souhaitez lancer la tâche automatiquement

if __name__ == "__main__":
    main()
