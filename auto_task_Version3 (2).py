import os
import json
import random
import time
import asyncio
import threading
from datetime import datetime
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon import events
from instagram_private_api import Client, ClientError

from config import *
from sessions_utils import get_password, log_error

def color(text, code):
    return f"\033[{code}m{text}\033[0m"

def horloge():
    return color(f"[{datetime.now().strftime('%H:%M:%S')}]", "1;34")

def printc(msg, code="1;36"):
    print(color(msg, code))

def choisir_utilisateur_random():
    users = []
    if os.path.exists(UTILISATEUR_PATH):
        with open(UTILISATEUR_PATH) as f:
            users = [list(item.keys())[0] for item in json.load(f)]
    if not users:
        return None
    return random.choice(users)

def connexion_instagram(username):
    password = get_password(username)
    if not password:
        printc("Mot de passe introuvable.", "1;31")
        return None
    try:
        user_agent = 'Instagram 123.0.0.21.114 Android'
        cl = Client(username, password, user_agent=user_agent)
        printc(f"Session Instagram prête pour {username}", "1;32")
        return cl
    except ClientError as e:
        printc(f"Echec login {username}: {e}", "1;31")
        log_error(f"Login failed for {username}: {e}")
        return None

def extraire_infos(msg):
    import re
    lien_match = re.search(r'https?://(www\.)?instagram.com/[^\s]+', msg)
    action_match = re.search(r'Action\s*:\s*(Follow|Like|Story View|Comment|Video View)', msg, re.IGNORECASE)
    if lien_match and action_match:
        return lien_match.group(0), action_match.group(1).lower()
    return None, None

def extraire_id_depuis_lien(cl, lien, action):
    try:
        lien = lien.lower()
        if action in ['like', 'comment', 'video view', 'story view']:
            if "instagram.com/p/" in lien or "instagram.com/reel/" in lien:
                shortcode = lien.rstrip("/").split("/")[-1]
                media = cl.media_info2(shortcode)
                return media['id']
            elif "instagram.com/stories/" in lien:
                username = lien.split("stories/")[1].split("/")[0]
                user_info = cl.username_info(username)
                return user_info['user']['pk']
        elif action == 'follow':
            if "instagram.com/" in lien:
                username = lien.rstrip("/").split("/")[-1]
                user_info = cl.username_info(username)
                return user_info['user']['pk']
    except Exception as e:
        printc(f"Erreur extraction ID: {e}", "1;31")
        log_error(f"Erreur extraction ID: {e}")
    return None

async def effectuer_action(cl, action, id_cible, comment_text=None):
    try:
        if action == "follow":
            cl.friendships_create(id_cible)
            printc("[Action] Follow effectué", "1;32")
        elif action == "like":
            cl.post_like(id_cible)
            printc("[Action] Like effectué", "1;32")
        elif action == "comment":
            if not comment_text:
                printc("[Erreur] Texte du commentaire manquant", "1;33")
                return False
            cl.post_comment(id_cible, comment_text)
            printc("[Action] Commentaire effectué", "1;32")
        elif action == "story view":
            printc("[Action] Story view (non supporté nativement)", "1;33")
        elif action == "video view":
            cl.post_like(id_cible)
            await asyncio.sleep(2)
            printc("[Action] Video view: like simulé", "1;33")
        return True
    except Exception as e:
        log_error(f"[Action Error] {e}")
        printc(f"[Erreur action] {e}", "1;31")
        return False

def sauvegarder_task(lien, action, username):
    with open(TASK_DATA_PATH, "a") as f:
        f.write(f"{datetime.now().isoformat()} | {username} | {action} | {lien}\n")

def auto_task_main():
    if not os.path.exists(CONFIG_PATH):
        printc("Fichier config.json manquant.", "1;31")
        return
    with open(CONFIG_PATH) as f:
        cfg = json.load(f)
    api_id = cfg["api_id"]
    api_hash = cfg["api_hash"]
    session_str = cfg.get("session", "")

    client = TelegramClient(StringSession(session_str), api_id, api_hash)
    loop = asyncio.get_event_loop()

    @client.on(events.NewMessage(from_users="SmmKingdomTasksBot"))
    async def handler(event):
        msg = event.raw_text
        if "please give us your profile" in msg or "choose account from the list" in msg:
            user = choisir_utilisateur_random()
            if not user:
                printc("Aucun compte disponible.", "1;31")
                return
            await asyncio.sleep(random.randint(1, 3))
            await event.respond(user)
            return
        if "choose social network" in msg or "current status" in msg:
            await asyncio.sleep(random.randint(1, 3))
            await event.respond("Instagram")
            return
        if "no active tasks" in msg:
            printc("Pas de tâches disponibles sur ce compte.", "1;33")
            await asyncio.sleep(random.randint(1, 3))
            await event.respond("Instagram")
            return
        if "▪️" in msg and "link" in msg and "action" in msg:
            user = choisir_utilisateur_random()
            cl = connexion_instagram(user)
            if not cl:
                printc("Connexion Instagram impossible.", "1;31")
                return
            lien, action = extraire_infos(msg)
            if not lien or not action:
                printc("Tâche invalide.", "1;31")
                return
            id_cible = extraire_id_depuis_lien(cl, lien, action)
            if not id_cible:
                printc("Impossible d'extraire l'ID cible.", "1;31")
                return
            if action == "comment":
                printc("En attente du texte du commentaire...")
                def get_comment():
                    comment = input("Texte du commentaire: ")
                    loop.create_task(effectuer_action(cl, action, id_cible, comment_text=comment))
                threading.Thread(target=get_comment).start()
                return
            result = await effectuer_action(cl, action, id_cible)
            if result:
                await event.respond("✅Completed")
            else:
                await event.respond("❌Error")
            sauvegarder_task(lien, action, user)
            await asyncio.sleep(random.randint(5, 10))
            await client.send_message("SmmKingdomTasksBot", "📝Tasks📝")
            return

    printc("Connexion à Telegram...")
    client.start()
    client.run_until_disconnected()