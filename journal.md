# Journal de l'agent marketing Brooze

Le plus récent en haut. Une entrée par post, puis les chiffres à J+2.

---

## 25/10 — Exécution hebdomadaire : rien à ajouter
- Fenêtre 26/10 → 01/11 déjà complète dans Metricool (7 jours de stories, carrousels lundi 26, mercredi 28, vendredi 30 à 18 h). Aucun doublon créé, aucun post ajouté. Réserve de stories : 7 disponibles. Mesures J+2 : non relevées dans cette exécution (portée trop faible pour conclure de toute façon).

---

## Registre des Reels (anti-redite : relire les 5 dernières lignes avant chaque concept)
Une ligne par Reel programmé, la plus récente en bas. Interdit de reprendre le **concept visuel**, l'**effet
signature** ou la **structure** d'un des 5 derniers ; chaque Reel ajoute au moins une **technique nouvelle** (en gras).

| Date | Id | Concept visuel | Effet signature | Structure | Techniques (nouvelle en gras) | Outils |
|---|---|---|---|---|---|---|
| 23/10 | 2026-10-23-apple-montre (v3 publiée) | « dire vs montrer » : une fiche technique imprimée sans fin (ce qu'on dit) contre des photos d'objets du quotidien sublimés (ce qu'on montre), autour d'un téléphone générique | **relief 2,5D** des rendus photoréalistes (parallaxe par pixel) | opposition qui bascule : la fiche domine, puis les photos prennent toute la place, titre-question, fin sur fond noir | photoréalisme fixe animé, **carte de profondeur + WebGL**, coups de zoom sur 4 mots, whip | Blender, moteur HTML |
| 25/10 | 2026-10-24-spotify-wrapped | une carte « bilan » qui se duplique en champ de milliers, puis se retourne sur des visages | **retournement en vague de cartes (instanciation GPU)** | plan-séquence à caméra continue : accumulation exponentielle, rupture, plongée | **three.js InstancedMesh + shader, barres pilotées par la voix**, titres sur vidéo continue | three.js, moteur HTML |

---

## 24/10 — Reel Spotify v2 programmé à la place de la v1 (demande de Zak)
- Même créneau : 25/10 à 18 h (Metricool id 404840123, uuid 108377246694589694), teaser de 18 h 30 inchangé, aucun doublon.
- Ce qui change : champ 3D v2 avec 22 relances de caméra calées sur les attaques des mots forts (pousse, pan, tilt, visée, recul, roulis), 6 vagues de cartes sur « partagent / publier / envoyer / comparer / partages / partagent-ils », poussières au premier plan, plus de carton de fin : la carte du début revient au pixel près (boucle parfaite), CTA en surimpression, son en boucle, 27 bruitages calés, titres effacés après leur temps de lecture.
- Mesures (engagement.py) : 0 zone morte (v1 : fin morte), relance max 3,3 s (v1 : 4,4 s), raccord couleur fin/début 0,16 (v1 : 0,69), son de fin −21,5 dB (v1 : −180). controle.py : 0 problème. Sceptique : sceptique_v2.md (passe ennui), publiable.
- Appris : le moteur découvrait des bords pendant le tremblé (corrigé pour tous les Reels) ; le contrôle bord_decouvert donnait une fausse alerte sur scène sombre (corrigé).


## Reel · 2026-10-23 · 13:30 · Claire · « Apple a compris… » (banque de voix, mémo du 22/10)
- **Source** : brooze-voix `audio/2026-10/memo-2026-10-22-1.m4a` (38,5 s). Verdict `ok`. Une erreur d'écoute corrigée d'après le contexte : « il se base » → « il se passe ». À relire par Zak : « Je vois la différence » (pourrait être « Tu vois la différence »).
- **Idée** : ne dis pas que ton produit est exceptionnel, montre-le (campagne « Shoot on iPhone », citée par Zak ; aucun chiffre, aucun logo).
- **Hooks** : retenu « Apple a compris quelque chose que beaucoup de marques n'ont toujours pas compris en publicité. » (intrigante, HSS 8) · écartés : « Apple aurait pu nous présenter une liste interminable… Mais au lieu de ça… » (démarre à 6,6 s) · « Arrêtez simplement de dire que votre produit est exceptionnel. » (provocatrice, en fin d'audio : on ne réordonne pas).
- **Hypothèse** : un Reel qui FAIT ce qu'il dit (fiche technique interminable coupée net, photographies qui arrivent, « exceptionnel » barré) retient plus qu'un conseil en typo seule.
- **Choix créatifs** : 100 % 2D ; 3 nouvelles scènes du moteur (`specs`, `galerie`, `barre`), duel A/B corrigé ; photographies = paysages dessinés en code ; silence de musique sur « exceptionnel » barré ; 41,2 s, rendu 3 min 50.
- **Sceptique** : passe 1 → 3 corrections (hook sans action, scène vide 0,9 s, duel vide) ; passe 2 → prête. `controle.py` : 0 problème, 0 glitch.
- **Metricool** : [Reel 23/10 13 h 30](https://app.metricool.com/planner/calendar?blogId=7268093&openWithPostUuid=-4757902081379974094) · [teaser 14 h](https://app.metricool.com/planner/calendar?blogId=7268093&openWithPostUuid=7464285017798757392)

---

## Reel TEST · 2026-10-22 · audio de démonstration (voix de synthèse) · BROUILLON, non publié
- **Source** : `inbox/traite/demo-premiere-seconde.m4a` (30,9 s, bruit de fond ajouté exprès). Compréhension : verdict
  `ok`, parole/bruit 41 dB, 0 saturation ; 4 erreurs d'écoute de Whisper corrigées d'après le contexte (« raffimais »
  → « as filmé », « Brose » → « Brooze »…), hallucination « [Bruit de » filtrée.
- **Idée** : la première seconde décide ; pas besoin de refilmer, on remonte l'existant. **Cible** : Karim.
- **Hooks** (instagram-hook-engine) : « Ta caméra n'est pas le problème. » (86) · « Filmé cent fois. Personne ne
  s'arrête. » (84) · **retenu** : mots exacts « Tu as filmé ton restaurant cent fois. » sur un fil qui défile (90).
- **Hypothèse** : un Reel qui FAIT ce qu'il dit (fil qui défile, chrono d'1 s, musique coupée sur « coupe le son »,
  rushs qui se rangent sur une timeline) retient plus qu'un Reel explicatif.
- **Choix créatifs** : 100 % 2D (pas de 3D : aucun objet ne la justifiait), 13 scènes, poussées plein cadre avec flou
  de mouvement, silence total de 16,3 à 18,7 s, son synthétisé (−14 LUFS).
- **Contrôle** : sceptique passe 1 → 6 corrections (sous-titres en double, hook muet, 2 idées sans visuel, fondu) ;
  passe 2 → prête à publier. `controle.py` : 0 problème, 0 glitch. Rendu 32,4 s en 2 min 32.
- **Metricool (draft)** : [Reel 24/10 18 h](https://app.metricool.com/planner/calendar?blogId=7268093&openWithPostUuid=6826725370241827805) ·
  [teaser 18 h 30](https://app.metricool.com/planner/calendar?blogId=7268093&openWithPostUuid=-6175005210685454902)

## Semaine du 23/10 au 01/11 · programmée le 22/10 (exécution test, en session)

**Analyse** : 3 posts depuis septembre, portée 8 à 11, 0 enregistrement, 0 partage : audience trop petite pour conclure, on compare des taux. Aucun concurrent suivi dans Metricool ; la recherche web ne donne que des fiches d'agences (Auguste & Louise, freelances Malt), pas de comptes Instagram lisibles : rien d'exploitable cette semaine. Air du temps : le marché de Noël de Strasbourg ouvre fin novembre (le 27 selon la plupart des sources), les commerçants préparent leurs contenus maintenant. Instagram dit que les carrousels gagnent en élan (enregistrements, référence). Décision : semaine Noël + preuve à la direction, 3 nouveaux formats testés (question en story, teaser du carrousel, avant/après d'accroches).

### 2026-10-23 · 10:00 · Story · Claire · Diagnostic
- **Hook** : « Ta vidéo est propre. C'est le problème. »
- **Hypothèse** : Une accusation douce (« propre, c'est le problème ») pour Claire fait moins de sorties / portée qu'un conseil neutre, parce qu'elle touche sa douleur exacte : des contenus propres mais sans impact.
- **Nouveau format** : non · **Contrôle** : charte OK, aucun débordement, relu.
- **Visuels** : `posts/2026-10-23-propre-pas-impact/` · **Metricool** : [image 1](https://app.metricool.com/planner/calendar?blogId=7268093&openWithPostUuid=-7469041722787412187) · [image 2](https://app.metricool.com/planner/calendar?blogId=7268093&openWithPostUuid=-2893102338234890709)
- **Chiffres J+2** : à relever.

### 2026-10-24 · 10:00 · Story · Karim · Méthode
- **Hook** : « Filme 10 secondes de ta salle pleine. »
- **Hypothèse** : Une micro-action à faire le jour même (« filme 10 secondes ce soir ») pour Karim obtient plus de réponses / portée qu'une story d'idée, parce qu'elle est faisable tout de suite.
- **Nouveau format** : non · **Contrôle** : charte OK, aucun débordement, relu.
- **Visuels** : `posts/2026-10-24-filme-ce-soir/` · **Metricool** : [image 1](https://app.metricool.com/planner/calendar?blogId=7268093&openWithPostUuid=-1455375601961188571)
- **Chiffres J+2** : à relever.

### 2026-10-25 · 10:00 · Story · Karim · Question directe
- **Hook** : « Tu publies le soir… ou entre deux clients ? »
- **Hypothèse** : Une question binaire en story (nouveau format) obtient plus de réponses / portée que nos stories d'affirmation, parce que répondre demande un seul mot.
- **Nouveau format** : oui · **Contrôle** : charte OK, aucun débordement, relu.
- **Visuels** : `posts/2026-10-25-question-soir-journee/` · **Metricool** : [image 1](https://app.metricool.com/planner/calendar?blogId=7268093&openWithPostUuid=-645618301177674576)
- **Chiffres J+2** : à relever.

### 2026-10-26 · 10:00 · Story · Karim · Teaser
- **Hook** : « Noël se joue en novembre. »
- **Hypothèse** : Une story qui annonce le carrousel du soir augmente sa portée par rapport aux carrousels non annoncés, parce qu'elle crée un rendez-vous.
- **Nouveau format** : oui · **Contrôle** : charte OK, aucun débordement, relu.
- **Visuels** : `posts/2026-10-26-teaser-noel/` · **Metricool** : [image 1](https://app.metricool.com/planner/calendar?blogId=7268093&openWithPostUuid=6052599164177106086)
- **Chiffres J+2** : à relever.

### 2026-10-26 · 18:00 · Carrousel · Karim · Méthode saisonnière
- **Hook** : « Ta vidéo de Noël est déjà dans ton téléphone. »
- **Hypothèse** : Un carrousel saisonnier (Noël) ancré dans « rien à tourner » obtient plus d'enregistrements / portée que notre carrousel du 19/10 (0 enregistrement), parce qu'il répond à un besoin daté et concret.
- **Nouveau format** : non · **Contrôle** : charte OK, aucun débordement, relu.
- **Visuels** : `posts/2026-10-26-noel-dans-ta-galerie/` · **Metricool** : [carrousel](https://app.metricool.com/planner/calendar?blogId=7268093&openWithPostUuid=-7240985071627909766)
- **Chiffres J+2** : à relever.

### 2026-10-27 · 10:00 · Story · Claire · Méthode
- **Hook** : « Écris la seule action que tu attends. »
- **Hypothèse** : Une story sur la preuve à la direction pour Claire obtient plus de réponses / portée que nos stories pour Karim, parce que c'est sa pression principale.
- **Nouveau format** : non · **Contrôle** : charte OK, aucun débordement, relu.
- **Visuels** : `posts/2026-10-27-direction-resultats/` · **Metricool** : [image 1](https://app.metricool.com/planner/calendar?blogId=7268093&openWithPostUuid=7732706882180893246)
- **Chiffres J+2** : à relever.

### 2026-10-28 · 10:00 · Story · Claire · Teaser
- **Hook** : « Même vidéo. Autre 1re phrase. »
- **Hypothèse** : Le teaser « même vidéo, deux premières secondes » augmente la portée du carrousel avant/après du soir.
- **Nouveau format** : oui · **Contrôle** : charte OK, aucun débordement, relu.
- **Visuels** : `posts/2026-10-28-teaser-accroches/` · **Metricool** : [image 1](https://app.metricool.com/planner/calendar?blogId=7268093&openWithPostUuid=7003585979674739409) · [image 2](https://app.metricool.com/planner/calendar?blogId=7268093&openWithPostUuid=-1018742560818246430)
- **Chiffres J+2** : à relever.

### 2026-10-28 · 18:00 · Carrousel · Claire · Méthode : avant / après
- **Hook** : « 5 accroches réécrites. »
- **Hypothèse** : Le format « 5 accroches réécrites, avant / après » (nouveau) obtient plus d'enregistrements / portée que nos carrousels en étapes, parce qu'il donne des modèles réutilisables.
- **Nouveau format** : oui · **Contrôle** : charte OK, aucun débordement, relu.
- **Visuels** : `posts/2026-10-28-accroches-avant-apres/` · **Metricool** : [carrousel](https://app.metricool.com/planner/calendar?blogId=7268093&openWithPostUuid=-8344913388609778851)
- **Chiffres J+2** : à relever.

### 2026-10-29 · 10:00 · Story · Karim · Mythe / réalité
- **Hook** : « « Il me faut une meilleure caméra. » »
- **Hypothèse** : Le format mythe/réalité (nouveau) en story fait moins de sorties / portée qu'une affirmation simple, parce que le mythe crée une attente de correction.
- **Nouveau format** : oui · **Contrôle** : charte OK, aucun débordement, relu.
- **Visuels** : `posts/2026-10-29-mythe-camera/` · **Metricool** : [image 1](https://app.metricool.com/planner/calendar?blogId=7268093&openWithPostUuid=5294463350788801172) · [image 2](https://app.metricool.com/planner/calendar?blogId=7268093&openWithPostUuid=-7483241007448569454)
- **Chiffres J+2** : à relever.

### 2026-10-30 · 10:00 · Story · Claire · Teaser
- **Hook** : « Les vues ne prouvent rien à ta direction. »
- **Hypothèse** : Le teaser du carrousel « 3 chiffres pour ta direction » augmente sa portée.
- **Nouveau format** : non · **Contrôle** : charte OK, aucun débordement, relu.
- **Visuels** : `posts/2026-10-30-teaser-direction/` · **Metricool** : [image 1](https://app.metricool.com/planner/calendar?blogId=7268093&openWithPostUuid=-526030731838731933)
- **Chiffres J+2** : à relever.

### 2026-10-30 · 18:00 · Carrousel · Claire · Preuve : convaincre en interne
- **Hook** : « 3 chiffres à montrer à ta direction. »
- **Hypothèse** : Un carrousel « prouver à ta direction » pour Claire obtient plus de partages / portée que nos autres carrousels, parce qu'elle a quelqu'un à qui l'envoyer.
- **Nouveau format** : non · **Contrôle** : charte OK, aucun débordement, relu.
- **Visuels** : `posts/2026-10-30-trois-chiffres-direction/` · **Metricool** : [carrousel](https://app.metricool.com/planner/calendar?blogId=7268093&openWithPostUuid=-1796033734287801014)
- **Chiffres J+2** : à relever.

### 2026-10-31 · 10:00 · Story · Karim · Positionnement : on crée à partir de l'existant
- **Hook** : « Tes clients te filment déjà. »
- **Hypothèse** : Montrer à Karim une matière qu'il a déjà sans le savoir (les stories de ses clients) obtient des réponses, parce que ça lève l'objection « je n'ai pas le temps de filmer ».
- **Nouveau format** : non · **Contrôle** : charte OK, aucun débordement, relu.
- **Visuels** : `posts/2026-10-31-clients-te-filment/` · **Metricool** : [image 1](https://app.metricool.com/planner/calendar?blogId=7268093&openWithPostUuid=4941621310454974340)
- **Chiffres J+2** : à relever.

### 2026-11-01 · 10:00 · Story · Karim · Appel à l'action
- **Hook** : « Une vidéo n'a qu'un travail : donner une raison de venir chez toi. »
- **Hypothèse** : Une story d'offre directe (le mot-clé AUDIT déjà utilisé dans notre carrousel du 19/10) obtient plus de messages / portée en fin de semaine thématique.
- **Nouveau format** : non · **Contrôle** : charte OK, aucun débordement, relu.
- **Visuels** : `posts/2026-11-01-audit/` · **Metricool** : [image 1](https://app.metricool.com/planner/calendar?blogId=7268093&openWithPostUuid=-9000582887005142205) · [image 2](https://app.metricool.com/planner/calendar?blogId=7268093&openWithPostUuid=-3995574561896708644)
- **Chiffres J+2** : à relever.

### Refusés
- Carrousel « Ta vidéo se joue avant la 3e seconde » (posts/_exemple-carrousel) : angle trop proche du carrousel du 19/10.
- Diapo « 4 demandes en message » : chiffre d'exemple retiré par prudence (vérité).

---

## 2026-10-22 · Story · Karim · Positionnement
- **Hook** : « Tes meilleures vidéos dorment dans ta galerie. »
- **Images** : `posts/2026-10-22-rushs-galerie/` (2 images)
- **Hypothèse** : la story obtient des réponses « RUSH » en message (indicateur : IGST11 réponses / IGST10 portée).
- **Analyse** : 3 posts depuis septembre, portée 8 à 11, aucune story mesurée. Le carrousel du 19/10 a déjà pris
  l'angle « test des 3 secondes » : écarté. Aucun concurrent suivi dans Metricool.
- **Pourquoi ce choix** : parle à la douleur de Karim (« pas le temps de tourner ») avec notre vrai positionnement
  (on crée à partir de l'existant). Appel à l'action simple : répondre « RUSH ».
- **Publication** : programmée automatiquement à 18 h 00 et 18 h 01 (meilleur créneau restant du jeudi).
  [image 1](https://app.metricool.com/planner/calendar?blogId=7268093&openWithPostUuid=1423513364291535869) · [image 2](https://app.metricool.com/planner/calendar?blogId=7268093&openWithPostUuid=-4833918069163342851)
- **Contrôle** : charte OK, lisibilité OK, logo goutte retiré (vrai fichier absent).
- **Vérification 18 h 13** : les 2 images ne sont plus dans la file Metricool (traitées à l'heure prévue) ; les statistiques de stories ne remontent pas encore, publication à confirmer au relevé J+2.
- **Chiffres J+2** : à relever.

## 22/10 soir — Reel Apple remplacé par la v3 (demande de Zak)
- Le Reel du 23/10 à 13 h 30 (Metricool, uuid −4757902081379974094, nouvel id 403394583) porte maintenant la v3 :
  images photoréalistes en relief 2,5D, texte corrigé d'après Whisper medium (« Tu vois la différence ? »,
  « Cet appareil photo est performant », « pourquoi il l'est »), sous-titres révélés mot par mot à l'instant dit,
  16 bruitages sous limiteur de densité (obturateur sur « Shoot » et « photo », grave sur les coups de zoom…).
  Légende, date et teaser de 14 h inchangés.
- Leçon : small se trompe sur les pronoms et les questions → medium par défaut ; relire pronoms, « ? » et guillemets.

## Filet 2026-10-23 (3 h 41) : réserve de stories reconstituée
Réserve vide à l'ouverture → 7 stories R-001 à R-007 (intemporelles, sans chiffre, rendu vérifié à l'œil, charte respectée). Stories programmées sur J..J+9 : toutes présentes, aucune réserve consommée.

## Reel · 2026-10-25 · 18:00 · Claire · « Spotify a réussi… » (banque, mémo du 22/10)
- Hook retenu (mots exacts de Zak) ; chiffre à l'écran : « 620 millions », dit par Zak. Aucune marque/logo à l'écran.
- Sceptique passe 1 : mur de cartes en moiré (P1) → champ.html corrigé (distance max 31, espacement 1,0, teinte par carte), re-rendu. Passe 2 : plus de moiré, cartes lisibles. Restes : début un peu sobre (0–12 s), 1 coupe de titre non déclarée à 29,5 s (changement de titre sur vidéo continue), bord noir 0,16 s à 11,6 s.
- `cerveau.py comparer` : « EN DESSOUS » sur rythme et finition, mais contre une SEULE référence (Reel Apple v3, 2,6 s/plan) alors que ce Reel est un plan-séquence voulu : mesure peu comparable (supposé, non prouvé). Publié quand même ; à surveiller en durée moyenne regardée.
- Metricool : [Reel 25/10 18 h](https://app.metricool.com/planner/calendar?blogId=7268093&openWithPostUuid=108377246694589694) · [teaser 18 h 30](https://app.metricool.com/planner/calendar?blogId=7268093&openWithPostUuid=-4281141811443580516)
