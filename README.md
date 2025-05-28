# TS-PRIVATEAPI

**Bot Instagram & Telegram – Version instagram_private_api**

## Installation

1. `pip install -r requirements.txt`
2. Remplis `utilisateur.json` et `config.json` (exemples ci-dessous)
3. Lance `python main.py`

## Exemples de fichiers de config

### utilisateur.json

```json
[
  {"moncompte1": "motdepasse1"},
  {"moncompte2": "motdepasse2"}
]
```

### config.json

```json
{
  "api_id": "1234567",
  "api_hash": "VOTRE_API_HASH",
  "session": ""
}
```

### blacklist.json

```json
[]
```

---

- Certaines actions (story view, video view) sont simulées ou limitées.
- Les comptes sont gérés via `utilisateur.json` (login/mot de passe).
- La session n’est pas stockée sur disque : login à chaque tâche (API non officielle).
- Pour la gestion des comptes, le nettoyage, etc., les scripts sont identiques à la version instagrapi.
