# Publication Instagram automatique — GoToDeco

- Chaque dimanche soir, Claude prépare les 5 publications de la semaine (2 posts, 3 stories) et les dépose dans `queue/`.
- Toutes les 20 minutes, GitHub Actions publie sur Instagram ce dont l'heure est arrivée.
- Les publications réussies passent dans `published/`, les échecs dans `failed/` (GitHub t'envoie alors un e-mail).

**Annuler une publication :** supprime son fichier `.json` dans `queue/` avant l'heure prévue.
**Mettre à jour un chiffre (nombre d'inscrits…) :** modifie `brand/facts.md`.

## Configuration (une seule fois)

Dans *Settings → Secrets and variables → Actions* du dépôt :

| Secret | Contenu |
|---|---|
| `IG_ACCESS_TOKEN` | code d'accès Instagram longue durée (application Meta) |
| `IG_USER_ID` | identifiant Instagram du compte GoToDeco |
| `GH_PAT` | jeton GitHub à granularité fine, accès *Secrets : lecture et écriture* sur ce dépôt (sert au renouvellement automatique du code Instagram) |

Le dépôt doit rester **public** : Instagram va chercher les images à une adresse publique.
Les secrets, eux, ne sont jamais visibles.

## Tester

*Actions → Publier sur Instagram → Run workflow* lance une vérification immédiate.
