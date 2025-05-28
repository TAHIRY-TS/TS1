import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SESSION_DIR = os.path.join(BASE_DIR, 'sessions')
SELECTED_USER_DIR = os.path.join(BASE_DIR, 'selected_user')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')
BLACKLIST_PATH = os.path.join(BASE_DIR, 'blacklist.json')
UTILISATEUR_PATH = os.path.join(BASE_DIR, 'utilisateur.json')
TASK_DATA_PATH = os.path.join(BASE_DIR, 'task_data.txt')
ERROR_LOG = os.path.join(LOGS_DIR, 'errors.txt')

os.makedirs(SESSION_DIR, exist_ok=True)
os.makedirs(SELECTED_USER_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
