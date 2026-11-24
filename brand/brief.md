# Brief visuel — GoToDeco

Document de contexte destiné à une IA générative, pour concevoir des visuels cohérents avec l'identité de la marque.

---

## 1. Le produit

**GoToDeco** est une application de covoiturage dédiée aux parapentistes. Elle permet de publier ou de rejoindre un trajet vers un site de décollage.

**Positionnement en une phrase :**
> GoToDeco, c'est le BlaBlaCar des parapentistes : trouver un covoiturage pour aller voler, au sein d'une communauté dédiée au parapente.

**Le problème d'origine :** les demandes de covoiturage vers les décollages se perdent entre les groupes WhatsApp, Facebook et les forums. Quelqu'un qui cherche une place ne croise jamais celui qui en propose une. L'application centralise tout au même endroit.

**Historique :** projet développé pendant 3 ans par Bérenger, parapentiste et développeur. Application sortie récemment sur iPhone, Android et en web app. Plus de 400 pilotes inscrits à ce jour.

---

## 2. Liens et contacts

| Élément | Valeur |
|---|---|
| Site web | **gotodeco.fr** |
| Email | **contact@gotodeco.fr** |
| Vidéo de présentation | https://youtu.be/wuLs2cMZFq0 |
| Plateformes | iPhone · Android · Web app |

**Important :** écrire « iPhone » plutôt que « iOS » sur les supports grand public — le terme est compris par tout le monde, y compris les pilotes plus âgés.

---

## 3. Identité visuelle

### Couleurs

| Rôle | Hex | RGB |
|---|---|---|
| Turquoise principal (couleur de marque) | `#0BAEC8` | 11, 174, 200 |
| Turquoise foncé | `#087A91` | 8, 120, 142 |
| Turquoise très foncé (fonds) | `#064A5C` | 6, 74, 92 |
| Turquoise clair (accents sur fond sombre) | `#8CE6F7` | 140, 230, 247 |
| Encre / texte principal | `#1C2026` | 28, 32, 38 |
| Gris texte secondaire | `#78808A` | 120, 128, 138 |
| Fond clair (blanc cassé) | `#F7F9FA` | 247, 249, 250 |
| Ambre (usage saisonnier automne uniquement) | `#EEAA54` | 238, 170, 84 |

### Typographie

**Montserrat**, en poids contrastés :
- **800 (ExtraBold)** pour les titres
- **700 (Bold)** pour les sous-titres et libellés
- **500 (Medium)** pour le corps de texte
- **300 (Light)** pour les textes secondaires et sous-titres aérés

Le contraste fort entre un titre en 800 et un sous-titre en 300 est une signature du style.

### Logo

Le logo associe un **pictogramme de parapente** (dégradé bleu turquoise vers bleu profond) et le mot-symbole **« GoToDeco »**.

**Contrainte technique majeure :** dans le fichier SVG, le texte est vectoriel mais **le pictogramme parapente est une image bitmap dont le dessin ne fait que 413 × 412 pixels**. Au-delà, il devient flou. Ne jamais l'afficher à plus de ~400 px de large. Pour du grand format, le faire vectoriser par un graphiste.

Déclinaisons existantes : version couleur (pour fonds clairs), version entièrement blanche (pour fonds sombres).

---

## 4. Principes de design

### Ce qui fonctionne

- Beaucoup d'espace négatif, les visuels doivent respirer
- Composition alignée à gauche (style éditorial) plutôt que tout centré
- Titres très gros sur 2 à 3 lignes, avec la dernière ligne en couleur d'accent
- Cercles décoratifs translucides (opacité 10-20/255) pour la profondeur
- Cartes blanches à coins arrondis avec ombre douce pour mettre en valeur les captures d'écran
- Listes numérotées épurées (01, 02, 03) avec filets de séparation
- Un petit trait turquoise + un mot en capitales espacées comme « eyebrow » au-dessus des titres

### Ce qu'il faut éviter

- Les effets clinquants, les badges arrondis multiples, les ombres artificielles
- Le style « template auto-généré »
- **Ne jamais dessiner de parapente en illustration vectorielle** — toutes les tentatives ont échoué. Utiliser le pictogramme du logo, une photo réelle, ou des formes abstraites (montagnes, dégradés de ciel, courbes de niveau)
- Le contraste insuffisant : du blanc sur turquoise clair donne un ratio de 2,6 et paraît flou. Toujours viser un ratio supérieur à 4,5 en fonçant le fond
- Répéter le logo et l'URL sur les stories Instagram : le nom du compte est déjà affiché par la plateforme

### Directions artistiques déjà explorées (à varier pour ne pas lasser)

1. Fond turquoise dégradé + cartes translucides — la plus utilisée, à espacer
2. Fond clair + grande diagonale turquoise
3. Fond sombre + courbes de niveau topographiques — très apprécié mais surexploité
4. Fond sombre + lignes horizontales déformées par un relief, avec un cercle-soleil en dégradé
5. Affiche éditoriale : fond clair, bloc turquoise en biais, pictogrammes illustratifs

---

## 5. Ton éditorial

- Chaleureux et communautaire, **entre pilotes** — jamais corporate
- Tutoiement sur les réseaux sociaux, vouvoiement sur les supports professionnels (clubs, écoles, presse)
- **Toujours écrire « covoiturage » en entier**, jamais « covoit » (les pilotes plus âgés ne comprennent pas l'abréviation)
- Ne pas dénigrer WhatsApp : formuler positivement ce que l'application apporte
- Ne pas promettre la gratuité totale : il y a des frais de service et un partage des frais de trajet. Dire plutôt « sans abonnement » ou insister sur la simplicité
- Éviter les chiffres en typographie géante isolée qui attirent l'attention sur leur modestie ; les intégrer dans une phrase

---

## 6. Fonctionnalités à illustrer

| Fonctionnalité | Angle de communication |
|---|---|
| Carte interactive | Tous les sites de vol de France, trajets à proximité |
| Création de trajet | Départ, site de décollage, date, places, véhicule, capacité matériel, aller/retour |
| Recherche de place | Signaler qu'on cherche un covoiturage sans attendre qu'un trajet existe |
| Demande de récup | Posé loin du déco ? Partager sa position GPS aux pilotes autour |
| Groupes | Rejoindre le groupe de son site ou de son club, ou créer le sien |
| Trajets privés par code | Réservés aux membres d'un club ou aux stagiaires d'une école |
| Canaux de discussion | Espace dédié par club ou école |
| Sites favoris | Garder ses décollages préférés à portée de main |
| Notation des conducteurs | Système de confiance entre pilotes après chaque trajet |
| Paiement Stripe | Partage des frais sécurisé |
| Géolocalisation | Centrer la carte sur sa position |
| Météo intégrée | Conditions de vol par site, avec indicateur « Ça vole ! » |

**Note importante :** l'application n'utilise PAS l'API de la FFVL. Ne jamais mentionner la FFVL sur un support.

---

## 7. Formats utilisés

| Support | Dimensions |
|---|---|
| Story Instagram | 1080 × 1920 |
| Post Instagram | 1080 × 1080 |
| Bannière web / Facebook / Open Graph | 1200 × 630 |
| Slide de présentation | 1600 × 900 |
| Miniature YouTube | 1280 × 720 |
| Bannière de chaîne YouTube | 2560 × 1440 (zone sûre centrale 1546 × 423) |
| Photo de profil | 800 × 800 (affichée en cercle) |
| Filigrane vidéo YouTube | 512 × 512, fond transparent |
| Bannière publicitaire forum | 192 × 108 (affichée en 96 × 54) |
| Sticker rond | 1200 × 1200, découpe à la forme |
| Flyer A6 | 1240 × 1748 + 3 mm de fond perdu |

---

## 8. Accroches validées

- « Le covoiturage des parapentistes »
- « Une place libre, ça se partage »
- « 3 pilotes. 1 voiture. 0 prise de tête. »
- « Tu montes voler ce week-end ? Crée ton trajet. »
- « Posé au milieu de nulle part ? »
- « Le vol libre, c'est aussi l'entraide »
- « Le relief nous rassemble »
- « Voler léger, ça commence sur la route »
- « Plus il y a de pilotes, plus chacun trouve son trajet »

---

## 9. Contexte stratégique

Le principal enjeu actuel est l'**amorçage** : beaucoup d'inscrits mais peu de trajets publiés, car les pilotes sont dispersés géographiquement. Les visuels doivent donc en priorité **inciter à publier un trajet** plutôt qu'à en chercher un, et encourager la **densité locale** (rejoindre le groupe de son site, inviter les pilotes de son club).

Cibles secondaires : les **clubs** (relais de diffusion auprès de leurs membres) et les **écoles** (vrai besoin logistique pour leurs stages, via les trajets privés par code).
