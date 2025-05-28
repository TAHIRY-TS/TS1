import os
from config import SESSION_DIR, UTILISATEUR_PATH

def clean_sessions():
    users = set()
    if os.path.exists(UTILISATEUR_PATH):
        import json
        with open(UTILISATEUR_PATH) as f:
            for entry in json.load(f):
                users.update(entry.keys())
    for session_file in os.listdir(SESSION_DIR):
        username = os.path.splitext(session_file)[0]
        if username not in users:
            print(f"Suppression session orpheline pour {username}")
            os.remove(os.path.join(SESSION_DIR, session_file))

if __name__ == "__main__":
    clean_sessions()
