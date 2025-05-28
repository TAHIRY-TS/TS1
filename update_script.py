import os
import subprocess
import sys
import time

def banner():
    print("\033[1;35m" + "="*55)
    print("            MISE À JOUR TS Instagram/Telegram            ")
    print("="*55 + "\033[0m\n")

def run_cmd(cmd, desc):
    print(f"\033[1;34m{desc}...\033[0m")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"\033[1;32mSuccès:\033[0m {result.stdout.strip()}\n")
    except subprocess.CalledProcessError as e:
        print(f"\033[1;31mErreur lors de: {desc}\033[0m")
        print(e.stderr)
        sys.exit(1)

def main():
    banner()

    # Vérifier si on est bien dans un repo git
    if not os.path.exists(".git"):
        print("\033[1;31mCe dossier n'est pas un repository git.\033[0m")
        sys.exit(1)

    # 1. Pull des dernières modifications
    run_cmd("git pull", "Récupération des dernières modifications du dépôt")

    # 2. Mise à jour des dépendances Python
    if os.path.exists("requirements.txt"):
        run_cmd(f"{sys.executable} -m pip install --upgrade pip", "Mise à jour de pip")
        run_cmd(f"{sys.executable} -m pip install -r requirements.txt", "Mise à jour des dépendances Python")
    else:
        print("\033[1;33mAucun requirements.txt trouvé, dépendances non mises à jour.\033[0m\n")

    print("\033[1;32mMise à jour terminée avec succès !\033[0m\n")
    print("Vous pouvez maintenant relancer le bot.")

if __name__ == "__main__":
    main()