#!/bin/bash

echo "=== Installation automatique TS Instagram Bot ==="
echo

# Demande le dossier d'installation
read -p "Nom du dossier du projet (ex: TS-INSTAGRAPI ou TS-PRIVATEAPI): " PROJECT_DIR
if [[ -z "$PROJECT_DIR" ]]; then
    echo "Nom de dossier vide. Abandon."
    exit 1
fi

# Crée le dossier
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR" || exit 1

# Crée les dossiers nécessaires
for d in sessions selected_user logs; do
    mkdir -p "$d"
done

# Détection ou choix de la version
API_LIB=""
if [[ -f requirements.txt ]]; then
    if grep -q "instagram_private_api" requirements.txt; then
        API_LIB="instagram_private_api"
    elif grep -q "instagrapi" requirements.txt; then
        API_LIB="instagrapi"
    fi
fi

if [[ -z "$API_LIB" ]]; then
    echo "Quelle version voulez-vous installer ?"
    select API_LIB in "instagrapi (recommandé)" "instagram_private_api"; do
        case $REPLY in
            1) API_LIB="instagrapi" ; break ;;
            2) API_LIB="instagram_private_api" ; break ;;
        esac
    done
fi

# Prépare requirements.txt selon version détectée ou choisie
if [[ ! -f requirements.txt ]]; then
    echo -e "$API_LIB\ntelethon\ncolorama" > requirements.txt
fi

# Fichiers de config d'exemple si absents
if [[ ! -f config.json ]]; then
    cat <<EOF > config.json
{
  "api_id": "1234567",
  "api_hash": "VOTRE_API_HASH",
  "session": ""
}
EOF
    echo "Fichier config.json exemple créé."
fi

if [[ ! -f utilisateur.json ]]; then
    cat <<EOF > utilisateur.json
[
  {"moncompte1": "motdepasse1"},
  {"moncompte2": "motdepasse2"}
]
EOF
    echo "Fichier utilisateur.json exemple créé."
fi

if [[ ! -f blacklist.json ]]; then
    echo "[]" > blacklist.json
    echo "Fichier blacklist.json créé."
fi

# Installation des dépendances python
echo
echo "Installation des dépendances Python..."
pip install -r requirements.txt

echo
echo "Structure prête !"
echo "Version détectée : $API_LIB"
echo "Place tes scripts .py dans $PROJECT_DIR"
echo

read -p "Voulez-vous lancer le menu principal maintenant ? (o/n) : " REP
if [[ "$REP" == "o" || "$REP" == "O" ]]; then
    python3 main.py
else
    echo "Installation terminée. Lancez python3 main.py quand vous êtes prêt."
fi