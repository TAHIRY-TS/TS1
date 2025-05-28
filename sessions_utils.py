import os
import json
from config import UTILISATEUR_PATH, LOGS_DIR

def get_password(username):
    if not os.path.exists(UTILISATEUR_PATH):
        return None
    with open(UTILISATEUR_PATH) as f:
        for item in json.load(f):
            if username in item:
                return item[username]
    return None

def log_error(msg):
    with open(os.path.join(LOGS_DIR, "errors.txt"), "a") as f:
        f.write(str(msg) + "\n")
