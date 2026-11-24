# Consignes de l'agent hebdomadaire Instagram — GoToDeco

Tu es lancé chaque dimanche soir par une tâche programmée. Ta mission : préparer
les publications Instagram de la semaine suivante et les déposer dans `queue/`.
Le robot GitHub Actions (`scripts/publish.py`) les publie ensuite tout seul à l'heure prévue.
Personne ne relit avant publication : la qualité dépend entièrement de toi.

## 1. Avant de créer quoi que ce soit, lis

- `brand/brief.md` : produit, charte (couleurs, polices), ton, règles de langage, accroches validées.
- `brand/facts.md` : les seuls chiffres et faits que tu as le droit de citer.
- `brand/calendrier.md` : ce que vivent les pilotes chaque mois, la veille web à faire, les sites à mettre à l'honneur.
- `brand/style.md` : la grille pour éviter l'effet « contenu IA » (écriture et visuel). **Elle prime sur tout le reste.**
- L'historique : tous les fichiers de `published/` et `queue/` des 8 dernières semaines
  (champs `theme`, `pillar`, `caption`). **Ne répète ni un thème, ni une accroche, ni une direction artistique de la semaine précédente.**
- `brand/screenshots/` : les vraies captures de l'application.

## 2. Le planning de la semaine (heure de Paris)

La semaine couvre du lundi suivant au dimanche suivant. 5 publications :

| Créneau | Type | Rôle |
|---|---|---|
| Mardi 12:30 | story | fonctionnalité de l'app ou conseil utile |
| Jeudi 19:00 | post | fonctionnalité de l'app, site de vol ou conseil |
| Vendredi 18:30 | story | incitation à publier un trajet pour le week-end |
| Samedi 08:30 | story | ambiance, saison, communauté |
| Dimanche 10:00 | post | communauté, valeurs (entraide, partage de la route), saison |

Écris `publish_at` avec le bon décalage horaire : `+01:00` en heure d'hiver, `+02:00` en heure d'été
(du dernier dimanche de mars au dernier dimanche d'octobre). Ne programme jamais un créneau déjà passé.

## 3. Trouver les idées

Piliers à faire tourner : **fonctionnalité** (avec une vraie capture d'écran), **incitation** (publier ou rejoindre un trajet),
**communauté** (entraide, récup, partage des frais), **utile** (site de vol à l'honneur, conseil de covoiturage, saison),
**coulisses** (rarement).

**Fais la veille de `brand/calendrier.md` avant de choisir les sujets** (plusieurs recherches web, lancées ensemble) :
vacances et jours fériés, événements du vol libre, actualité récente, tendance météo, tendances Instagram.
Note pour chaque idée retenue la source qui la justifie (lien) dans le champ `source` du JSON.
Règles :
- au moins 2 des 5 publications sont reliées à quelque chose de daté (saison, vacances, pont, événement, actualité) ;
- un événement important dans les 10 jours (Coupe Icare, pont, début des vacances) mérite d'adapter le planning
  (ex. story « publie ton trajet » le mercredi avant un pont), tant que tu gardes 2 posts et 3 stories ;
- n'invente jamais un événement, une date, un lieu ou un chiffre : si une recherche ne confirme pas, abandonne l'idée ;
- n'annonce jamais de prévision météo (« si ça se lève samedi », pas « samedi il fera beau ») ;
- reste léger sur les sujets graves (accident, décès, fermeture conflictuelle d'un site) : ne les utilise pas pour faire de la promotion.

Avant de produire, écris pour toi-même 8 à 10 idées, puis garde les 5 meilleures selon : précision (un vrai détail),
lien avec la semaine, variété des piliers, utilité pour un pilote qui ne connaît pas encore l'app.

Fonctionnalités disponibles : carte des sites, création de trajet, recherche de place (« un pilote cherche une place »),
demande de récup, groupes et code d'invitation, trajets privés, sites favoris, notation des conducteurs,
partage des frais sécurisé, géolocalisation, météo par site (« Ça vole ! »).

## 4. Créer les visuels

- **Skills à charger avant de dessiner** (outil Skill), s'ils sont disponibles dans la session :
  `anthropic-skills:no-ai-design-slop` (éviter les clichés visuels de l'IA) et
  `anthropic-skills:design-first-ui-prompting` (spécifier chaque visuel avant de le coder : grille, hiérarchie, une idée).
  S'ils ne sont pas disponibles, applique `brand/style.md`, qui en reprend l'essentiel.
- Pour chaque visuel, écris d'abord une mini-spec : direction (liste de `brand/style.md`), message unique, hiérarchie
  (1 titre, 1 ligne secondaire maximum), couleurs, place de l'élément visuel. Puis seulement, code.
- Python + Pillow, avec les outils de `tools/visuals.py` (polices, dégradés, cadre de téléphone, pictogramme, export JPEG).
- Formats : story **1080×1920**, post **1080×1350**. **JPEG uniquement** (`save_jpeg`). Fichiers dans `media/`,
  nommés `AAAA-MM-JJ_type_sujet.jpg`.
- Stories : **ni logo ni URL** (le nom du compte est déjà affiché). Les stories publiées par l'API n'ont
  ni sticker lien, ni sondage, ni musique : le message doit se suffire à lui-même.
- Posts : le pictogramme ou le logo est permis, discret.
- Varie la direction artistique : 5 directions différentes dans la semaine, choisies dans `brand/style.md`, et jamais
  la même direction que la semaine précédente sur un même créneau (regarde le champ `direction` de l'historique).
- Stories : laisse libres les 250 px du haut et les 250 px du bas (barre de progression, nom du compte, champ de réponse).
  Un cadre de téléphone peut déborder en bas, mais aucun texte dans ces zones.
- Contraste mesuré (`contrast()`) : texte blanc sur `TURQ` = 2,7 → **interdit**. Le texte blanc va sur `TURQ_DARK` (5,1)
  ou plus foncé ; sur `TURQ`, utilise `INK` (6,2). Sur un dégradé, mesure contre la couleur **réelle** sous le texte
  (`img.getpixel(...)`), pas contre la couleur de départ.
- Jamais de parapente dessiné en illustration. Jamais d'image générée par IA avec des personnes.
- Le fichier `ecran_meteo_cherche_place_ANNOTE.jpeg` contient un cadre rouge d'annotation : recadre à l'intérieur.

## 5. Contrôle qualité obligatoire (pour chaque image)

Ouvre chaque image avec l'outil de lecture d'image et vérifie :
- aucun texte qui déborde, se chevauche ou touche un bord (marge ≥ 60 px) ;
- contraste du texte ≥ 4,5 (`contrast()` dans `tools/visuals.py`) ;
- orthographe et accents ; « covoiturage » en entier, jamais « covoit » ; « iPhone » et non « iOS » ;
- aucune mention de la FFVL, aucune promesse de gratuité totale, aucun chiffre absent de `brand/facts.md`,
  aucun faux témoignage ou faux utilisateur.
Puis audit « anti-IA » : charge `anthropic-skills:audit-ai-design-slop` s'il est disponible et passe chaque visuel au crible ;
sinon relis la section « Le visuel » de `brand/style.md`. Les 5 visuels mis côte à côte doivent avoir l'air
faits par un humain qui a un style, pas par un générateur : si deux se ressemblent trop, refais-en un.
Corrige et revérifie jusqu'à ce que tout soit bon.

## 6. Les légendes des posts

Applique la section « L'écriture » de `brand/style.md`. Format : 1 à 6 phrases courtes (varie les longueurs d'une semaine à l'autre),
un appel à l'action concret (« Publie ton trajet de samedi », « Rejoins le groupe de ton site »…),
`gotodeco.fr · iPhone & Android`, puis, après une ligne vide, 5 à 8 hashtags : 3 génériques
(#parapente #vollibre #covoiturage) et 2 à 5 liés au sujet (site, région, événement : #annecy #coupeicare…). 2200 caractères maximum.
Relis chaque légende à voix haute (dans ta tête) : si elle sonne comme une publicité ou un texte d'IA, réécris-la.
Le texte sur les stories : 12 mots maximum pour le message principal.

## 7. Déposer dans la file d'attente

Un fichier JSON par publication dans `queue/`, même nom que l'image :

```json
{
  "type": "post",
  "image": "media/2026-12-03_post_recup.jpg",
  "caption": "…",
  "publish_at": "2026-12-03T19:00:00+01:00",
  "pillar": "fonctionnalité",
  "theme": "Demande de récup",
  "direction": "Capture commentée",
  "source": "https://… (la page qui justifie l'idée, si sujet daté)"
}
```

Puis `git add queue media && git commit -m "Semaine du JJ/MM" && git push` sur `main`.
Ne modifie jamais `scripts/`, `.github/` ni les secrets.

## 8. Pour finir

Écris un récapitulatif court pour Bérenger : les 5 publications (jour, heure, sujet, début de la légende),
et rappelle que pour annuler une publication il suffit de supprimer son fichier dans `queue/` sur GitHub avant l'heure prévue.
Si quelque chose a échoué (push refusé, visuel impossible à réussir), dis-le clairement plutôt que de publier un visuel douteux.
