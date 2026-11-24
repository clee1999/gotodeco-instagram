#!/usr/bin/env python3
"""Robot de publication Instagram de GoToDeco.

Lit les publications en attente dans queue/*.json et publie sur Instagram
celles dont l'heure est arrivée, via l'API officielle (Instagram Login).

Format d'une entrée de file d'attente (queue/<id>.json) :
{
  "type": "post" | "story",
  "image": "media/2026-11-27_post.jpg",        # JPEG, chemin dans le dépôt
  "caption": "Texte du post…",                  # ignoré pour les stories
  "publish_at": "2026-11-27T19:00:00+01:00"     # ISO 8601 avec fuseau
}

Variables d'environnement :
  IG_ACCESS_TOKEN   (secret)  code d'accès : soit un code Instagram (commence par IGAA,
                    passe par graph.instagram.com), soit un code Facebook d'utilisateur
                    système issu de la connexion unifiée (commence par EAA, graph.facebook.com)
  IG_USER_ID        (secret)  identifiant du compte Instagram ; obligatoire avec un code EAA,
                    lu via /me sinon
  PUBLIC_BASE_URL   (optionnel) URL publique de la racine du dépôt
  IG_API_VERSION    (optionnel) ex. v24.0
  DRY_RUN=1         n'appelle pas Instagram, affiche ce qui serait publié
"""
import json, os, sys, time, shutil, urllib.parse, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUEUE, DONE, FAILED = ROOT / "queue", ROOT / "published", ROOT / "failed"
TOKEN = os.environ.get("IG_ACCESS_TOKEN", "").strip()
IG_TOKEN = TOKEN.startswith("IG")                # code Instagram ; sinon code Facebook (EAA…)
HOST = "graph.instagram.com" if IG_TOKEN else "graph.facebook.com"
API = f"https://{HOST}/{os.environ.get('IG_API_VERSION', 'v24.0')}"
DRY = os.environ.get("DRY_RUN") == "1"
MAX_ATTEMPTS = 3
MAX_LATENESS = timedelta(hours=24)   # au-delà, la publication est abandonnée


def public_base():
    base = os.environ.get("PUBLIC_BASE_URL", "").strip().rstrip("/")
    if base:
        return base
    repo = os.environ.get("GITHUB_REPOSITORY")
    branch = os.environ.get("GITHUB_REF_NAME", "main")
    if not repo:
        sys.exit("PUBLIC_BASE_URL ou GITHUB_REPOSITORY doit être défini.")
    return f"https://raw.githubusercontent.com/{repo}/{branch}"


def call(method, path, params):
    params = dict(params, access_token=TOKEN)
    data = urllib.parse.urlencode(params).encode()
    if method == "GET":
        req = urllib.request.Request(f"{API}/{path}?{data.decode()}")
    else:
        req = urllib.request.Request(f"{API}/{path}", data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise RuntimeError(f"HTTP {e.code} sur {path} : {body[:500]}") from None


def check_public(url):
    req = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            if r.status != 200:
                raise RuntimeError(f"Image inaccessible ({r.status}) : {url}")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Image inaccessible ({e.code}) : {url}") from None


def publish(entry, user_id, base):
    url = f"{base}/{entry['image']}"
    if not entry["image"].lower().endswith((".jpg", ".jpeg")):
        raise RuntimeError("Instagram n'accepte que des images JPEG.")
    if DRY:
        print(f"  [DRY_RUN] {entry['type']} ← {url}")
        return "dry-run"
    check_public(url)
    params = {"image_url": url}
    if entry["type"] == "story":
        params["media_type"] = "STORIES"
    else:
        params["caption"] = entry.get("caption", "")[:2200]
    container = call("POST", f"{user_id}/media", params)["id"]
    for _ in range(30):                       # attend que Meta ait traité l'image
        status = call("GET", container, {"fields": "status_code"}).get("status_code")
        if status == "FINISHED":
            break
        if status in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"Conteneur {container} en état {status}")
        time.sleep(5)
    else:
        raise RuntimeError(f"Conteneur {container} jamais prêt")
    return call("POST", f"{user_id}/media_publish", {"creation_id": container})["id"]


def move(path, folder, entry):
    folder.mkdir(exist_ok=True)
    (folder / path.name).write_text(json.dumps(entry, ensure_ascii=False, indent=2) + "\n")
    path.unlink()


def main():
    if not TOKEN and not DRY:
        sys.exit("IG_ACCESS_TOKEN manquant.")
    now = datetime.now(timezone.utc)
    base = public_base()
    user_id = os.environ.get("IG_USER_ID", "").strip()
    if not user_id:
        if DRY:
            user_id = "me"
        elif IG_TOKEN:
            user_id = call("GET", "me", {"fields": "user_id"})["user_id"]
        else:
            sys.exit("IG_USER_ID manquant (obligatoire avec un code Facebook EAA…).")
    if not DRY:                               # vérifie le code à chaque passage
        account = call("GET", user_id, {"fields": "username"})
        print(f"Compte Instagram : @{account.get('username')} (via {HOST})")
    errors = 0
    for path in sorted(QUEUE.glob("*.json")):
        entry = json.loads(path.read_text())
        when = datetime.fromisoformat(entry["publish_at"])
        if when.tzinfo is None:
            raise SystemExit(f"{path.name} : publish_at doit contenir un fuseau horaire.")
        if when > now:
            continue
        print(f"→ {path.name} ({entry['type']}, prévu {entry['publish_at']})")
        if now - when > MAX_LATENESS:
            entry["error"] = "Abandonnée : heure de publication dépassée de plus de 24 h."
            move(path, FAILED, entry); errors += 1
            print("  abandonnée (trop en retard)")
            continue
        try:
            media_id = publish(entry, user_id, base)
            entry.update(published_at=now.isoformat(), media_id=media_id)
            if not DRY:
                move(path, DONE, entry)
            print(f"  publiée ✓ ({media_id})")
        except Exception as e:                # noqa: BLE001
            entry["attempts"] = entry.get("attempts", 0) + 1
            entry["error"] = str(e)
            print(f"  échec ({entry['attempts']}/{MAX_ATTEMPTS}) : {e}")
            if entry["attempts"] >= MAX_ATTEMPTS:
                move(path, FAILED, entry)
            else:
                path.write_text(json.dumps(entry, ensure_ascii=False, indent=2) + "\n")
            errors += 1
    if errors:
        sys.exit(1)                           # fait échouer le job : GitHub t'envoie un e-mail


if __name__ == "__main__":
    main()
