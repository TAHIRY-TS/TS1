from compte_manager import gestion_comptes
from auto_task import auto_task_main

def main():
    print("==== TS Instagram Automation (instagram_private_api) ====")
    print("1. Gérer les comptes Instagram")
    print("2. Lancer l'automatisation des tâches Instagram/Telegram")
    print("0. Quitter")

    while True:
        choix = input("\nVotre choix : ").strip()
        if choix == "1":
            gestion_comptes()
        elif choix == "2":
            auto_task_main()
        elif choix == "0":
            print("Au revoir !")
            break
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    main()