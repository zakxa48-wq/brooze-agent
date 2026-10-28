# Verdict, tentative 1 : **À REPRENDRE**

## Pourquoi ce n'est pas publiable

### V1-1 · P1 · glitchs : alertes FLASH/SAUT/NOIR/COUPE, voir les bandes
- où : — · source : controle.py
- preuve : controle.json
- exigé : aucun bloquant
- **condition pour passer** : controle.py ne signale plus : « glitchs : alertes FLASH/SAUT/NOIR/COUPE, voir les bandes »

### V1-2 · P2 · engagement · pas de relance pendant 5.9 s (4.8–10.7 s) : viser une relance toutes les 1,5 à 3 s
- où : 4.8–10.7 s · source : controle.py (à justifier)
- preuve : controle.json
- exigé : corrigé, ou justifié dans reel.json « justifications » et accepté par l'évaluation
- **condition pour passer** : corriger, ou écrire pourquoi ce Reel fait exception (reel.json → justifications)

### V1-3 · P2 · engagement · pas de relance pendant 3.4 s (11.2–14.6 s) : viser une relance toutes les 1,5 à 3 s
- où : 11.2–14.6 s · source : controle.py (à justifier)
- preuve : controle.json
- exigé : corrigé, ou justifié dans reel.json « justifications » et accepté par l'évaluation
- **condition pour passer** : corriger, ou écrire pourquoi ce Reel fait exception (reel.json → justifications)

### V1-4 · P2 · engagement · pas de relance pendant 9.2 s (18.8–28.0 s) : viser une relance toutes les 1,5 à 3 s
- où : 18.8–28.0 s · source : controle.py (à justifier)
- preuve : controle.json
- exigé : corrigé, ou justifié dans reel.json « justifications » et accepté par l'évaluation
- **condition pour passer** : corriger, ou écrire pourquoi ce Reel fait exception (reel.json → justifications)

### V1-5 · P2 · engagement · pas de relance pendant 3.3 s (28.6–31.9 s) : viser une relance toutes les 1,5 à 3 s
- où : 28.6–31.9 s · source : controle.py (à justifier)
- preuve : controle.json
- exigé : corrigé, ou justifié dans reel.json « justifications » et accepté par l'évaluation
- **condition pour passer** : corriger, ou écrire pourquoi ce Reel fait exception (reel.json → justifications)

### V1-6 · P2 · engagement · boucle : la fin est immobile, la reprise se verra (garder le mouvement jusqu'à la dernière image)
- où : tout le Reel · source : controle.py (à justifier)
- preuve : controle.json
- exigé : corrigé, ou justifié dans reel.json « justifications » et accepté par l'évaluation
- **condition pour passer** : justification refusée : refusée : mouvement_fin 0,03 vs 2,62 au début, écart_image 14,7, visage 15 % plus grand à la fin ; défaut P2 41.0–42.39.

### V1-7 · P2 · engagement · durée 42.4 s : la plus courte possible pour l'idée (souvent 15–30 s), couper ce qui ne sert pas
- où : 15–30 s · source : controle.py (à justifier)
- preuve : controle.json
- exigé : corrigé, ou justifié dans reel.json « justifications » et accepté par l'évaluation
- **condition pour passer** : corriger, ou écrire pourquoi ce Reel fait exception (reel.json → justifications)

### V1-11 · P1 · Image identique pendant ~6 s (grille 3 scènes, même cadrage, même rythme) et le concept-titre « l'effet Koulechov » (voix 22.39) n'a aucun événement visuel : seuls les sous-titres changent. C'est le pivot de la vidéo et le moment où un spectateur décroche. Le contrôle ne le voit pas car la dérive lente de caméra donne une énergie ~0,5 au-dessus du seuil.
- où : 19.0–25.5 s · source : évaluation indépendante
- preuve : planche_cles.jpg / reel_sceptique/planche.jpg lignes 19.0–25.0 : 12 vignettes quasi identiques ; engagement.png plateau bas 19.5–25.5 ; relances.json : écart 18.8→28.0 = 9.2 s (a_justifier) ; diff d'images 19.6 vs 25.0 : seulement 5–8 % de pixels changent, tous par dérive de zoom, aucun élément nouveau.
- exigé : —
- **condition pour passer** : Un changement visuel net (>= 1 élément qui apparaît/bouge/change d'échelle, énergie engagement.png > 2) posé à 22.39 ±0.15 s sur « Koulechov », ET aucun intervalle sans relance > 3,5 s entre 18.8 et 28.0 (relances.json).
- piste : Faire vivre la grille : le visage cloné pulse/clignote à tour de rôle sur « n'a jamais changé » (19.9), le nom « KOULECHOV » en gros texte Inter 800 s'écrit à 22.39, les 3 lignes s'allument une par une sur « associant deux images » au lieu de rester statiques 6 s.

### V1-12 · P1 · Phrase cassée : la voix dit « l'ordre dans lequel tu… [Le montage], c'est de la manipulation » ; le mot « montres » du storyboard est absent de la voix (mots.json : « tu » @32.92, « Le » @33.13, trou de 0,2 s). Le sous-titre affiche « TU LE MONTAGE, » (deux phrases fusionnées, « Le » majuscule au milieu). Le texte est fidèle à ce qui est dit, mais ce qui est dit est une phrase tronquée par la coupe de voix, donc incompréhensible pour qui écoute : la ligne-clé de la thèse (« c'est l'ordre dans lequel tu le montres ») est perdue.
- où : 32.2–33.9 s · source : évaluation indépendante
- preuve : mots.json : …lequel@32.38 tu@32.92 Le@33.13 montage,@33.29 ; sous_titres.txt ligne 32.92 « TU LE MONTAGE, » ; frames 33.0 à 33.6 : sous-titre « tu Le montage, » ; storyboard_zak.md ligne 00:40-00:48 : « …dans lequel tu le montres ».
- exigé : —
- **condition pour passer** : L'audio contient « montres » entre 32.92 et 33.13 (ré-extraire la prise ou rendre le raccord naturel) ; les sous-titres lisent « L'ordre dans lequel tu le montres. » puis « Le montage, c'est… » sans fusion ; mots.json à jour et un groupe de sous-titres ne mélange pas deux phrases.
- piste : Chercher « montres » dans la source audio (39.99 s de fenêtre) ; sinon recoller depuis une autre occurrence ou couper la phrase à « l'ordre » + « Le montage, c'est de la manipulation pure » proprement avec silence de respiration, et séparer les groupes TU / LE MONTAGE.

### V1-13 · P2 · Raccord de boucle visible : le visage final (largeur 247 px à 360 de large, haut 161) est ~15 % plus grand que le visage de la 1re image (largeur 215, haut 186) et décalé ; la première image réintroduit le sous-titre « Regarde » et le halo. À 41.0–41.4 un résidu du bouton (pastille cuivre couleur chair) et le fantôme du tampon traversent le visage. Le clin d'œil déclaré (« même dessin, même place, même taille ») est faux à la mesure. En plus, 39.5→41.4 est immobile (énergie ~0 sur engagement.png) alors que la voix est finie à ~39.3 : ~3 s de vide avant la reprise.
- où : 41.0–42.4 s · source : évaluation indépendante
- preuve : jonction.jpg (panneaux 1-2 : tampon fantôme + pastille ; panneaux 5→6 : saut de taille du visage) ; mesure bbox : 42.3 s x 56–303 y 161–450 ; 0.1 s x 72–287 y 186–517 ; engagement.json boucle.ecart_image = 14.7, mouvement_fin 0.03 vs mouvement_début 2.62 ; engagement.png plateau 39.5–41.4.
- exigé : —
- **condition pour passer** : bbox du visage à la dernière image = bbox à la première (écart <= 2 px, même échelle) ; aucun résidu de tampon ou de bouton sur le visage après 41.0 ; mouvement_fin >= 0,5 (boucle.mouvement_fin) ; plus de 1,2 s sans changement entre 39.3 et 42.4 interdit.
- piste : Faire revenir le visage à la taille exacte de l'ouverture en glissant pendant que le bouton repart (sans pastille chair), garder une micro-animation (clignement, halo qui commence à enfler) jusqu'à la dernière image, et raccourcir les 3 s de queue après la voix.

### V1-14 · P2 · Scène des frites : 4,8 s sans relance (4.8→10.7) sur la même image (visage + assiette, vapeur lente), seul le sous-titre bouge. Les trois scènes visage+objet (frites 5.9, tombe 11.1, chiot 15.0) ont la même structure : carte vide qui glisse, objet qui entre, 3-5 s immobile, ce qui donne une cadence mécanique « template ».
- où : 5.9–10.7 s · source : évaluation indépendante
- preuve : planche_cles.jpg lignes 6.0–10.5 : 10 vignettes identiques ; engagement.png creux 5.5–10.5 (énergie ~0,5) ; relances.json 4.8→10.7 ; entrées mesurées à 5.87, 11.0, 15.0 (même geste de glissé).
- exigé : —
- **condition pour passer** : Au moins une relance visible (réaction du visage, objet qui réagit, cadrage) entre 7.0 et 9.5 s ; les trois entrées d'objet ne partagent pas le même mouvement et la même durée de plan à ±0,5 s.
- piste : Sur « il a faim » faire fondre la vapeur / lueur cuivre sur les yeux, sur la tombe la pluie s'intensifie, sur le chiot la queue bat : une relance par scène, de type différent. Le visage ne bouge pas d'un pixel (storyboard), donc agir sur l'objet et le fond.

### V1-15 · P2 · Composition déséquilibrée : la grille 3×2 occupe la moitié gauche (cartes de x≈55 à 312 sur 540) et ~40 % de la largeur à droite est vide jusqu'à l'arrivée des flèches (25.5). En vrai zoom arrière « côte à côte » on attendait un cadre rempli ; on a l'impression d'un calque oublié.
- où : 19.0–25.5 s · source : évaluation indépendante
- preuve : frames 21.5 et 25.0 (reel.mp4, scale 540 de large) : tout le contenu à gauche, vide à droite.
- exigé : —
- **condition pour passer** : Boîte englobante du contenu centrée à ±5 % de la largeur sur 19.5–25.0 (ou le vide est occupé par un élément voulu).
- piste : Centrer la grille, ou faire entrer les colonnes « = faim / triste / attendri » dès 22.4 pour remplir la droite.

### V1-16 · P2 · « Logo » Brooze Production du tampon : recomposé en typo (Inter 900 « BROOZE » + « PRODUCTION » en capitales espacées dans un cadre incliné), fichier logo « non fourni » (scene.py l. 194). La charte : « uniquement le vrai fichier, jamais redessiné ». Un tampon recréé peut être pris pour le logo officiel de l'agence, et la graisse 900 sort de la charte (Inter 800 max).
- où : 35.6–37.0 s · source : évaluation indépendante
- preuve : scene.py l. 194–202 (commentaire « le fichier logo n'est pas fourni », Texte('BROOZE', graisse=900)) ; charte.md ligne Logo ; frame 36.3 ; aucun assets/logo.* dans le dépôt.
- exigé : —
- **condition pour passer** : Soit le vrai fichier logo est utilisé tel quel, soit Zak valide par écrit la version typographique comme « wordmark » (Space Grotesk 700 caps, ou Inter 800) ; plus aucune graisse 900.
- piste : Demander le fichier à Zak ; en attendant, passer au wordmark Space Grotesk de la charte sans cadre imitant un logo, en gardant le tampon comme geste (CLAC) autour d'un mot, pas d'un faux logo.

## Toutes les conditions à remplir pour la tentative suivante (et rien d'autre ne sera exigé, sauf P1 ou régression)

- [ ] V1-1 : controle.py ne signale plus : « glitchs : alertes FLASH/SAUT/NOIR/COUPE, voir les bandes »
- [ ] V1-2 : corriger, ou écrire pourquoi ce Reel fait exception (reel.json → justifications)
- [ ] V1-3 : corriger, ou écrire pourquoi ce Reel fait exception (reel.json → justifications)
- [ ] V1-4 : corriger, ou écrire pourquoi ce Reel fait exception (reel.json → justifications)
- [ ] V1-5 : corriger, ou écrire pourquoi ce Reel fait exception (reel.json → justifications)
- [ ] V1-6 : justification refusée : refusée : mouvement_fin 0,03 vs 2,62 au début, écart_image 14,7, visage 15 % plus grand à la fin ; défaut P2 41.0–42.39.
- [ ] V1-7 : corriger, ou écrire pourquoi ce Reel fait exception (reel.json → justifications)
- [ ] V1-11 : Un changement visuel net (>= 1 élément qui apparaît/bouge/change d'échelle, énergie engagement.png > 2) posé à 22.39 ±0.15 s sur « Koulechov », ET aucun intervalle sans relance > 3,5 s entre 18.8 et 28.0 (relances.json).
- [ ] V1-12 : L'audio contient « montres » entre 32.92 et 33.13 (ré-extraire la prise ou rendre le raccord naturel) ; les sous-titres lisent « L'ordre dans lequel tu le montres. » puis « Le montage, c'est… » sans fusion ; mots.json à jour et un groupe de sous-titres ne mélange pas deux phrases.
- [ ] V1-13 : bbox du visage à la dernière image = bbox à la première (écart <= 2 px, même échelle) ; aucun résidu de tampon ou de bouton sur le visage après 41.0 ; mouvement_fin >= 0,5 (boucle.mouvement_fin) ; plus de 1,2 s sans changement entre 39.3 et 42.4 interdit.
- [ ] V1-14 : Au moins une relance visible (réaction du visage, objet qui réagit, cadrage) entre 7.0 et 9.5 s ; les trois entrées d'objet ne partagent pas le même mouvement et la même durée de plan à ±0,5 s.
- [ ] V1-15 : Boîte englobante du contenu centrée à ±5 % de la largeur sur 19.5–25.0 (ou le vide est occupé par un élément voulu).
- [ ] V1-16 : Soit le vrai fichier logo est utilisé tel quel, soit Zak valide par écrit la version typographique comme « wordmark » (Space Grotesk 700 caps, ou Inter 800) ; plus aucune graisse 900.

## Conseils (ne bloquent pas)

- V1-8 : plans trop longs en moyenne → durée moyenne des plans ≤ 3.48 s (couper ou relancer dans les plans longs) (indicatif : moins de 3 références de qualité ≥ 7)
- V1-9 : aucune coupe dans les 3 premières secondes → au moins une coupe ou un changement de plan avant 3 s (indicatif : moins de 3 références de qualité ≥ 7)
- V1-10 : coupes pas assez calées sur les attaques du son → part des coupes sur une attaque ≥ 0.13 (indicatif : moins de 3 références de qualité ≥ 7)
- V1-17 : Timeline : 3,7 s sans relance (28.6→31.9) et la timeline n'occupe que le tiers supérieur du cadre (y 230–540 sur 960), le bas est vide ; l'inversion promise (« blocs qui s'inversent rapidement ») n'a lieu que de 32.7 à 34.5, bien après « ce que tu filmes ». → Une inversion de blocs ou un déplacement de tête de lecture visible (relance) entre 29.5 et 31.5 ; timeline centrée verticalement (zone sûre y 220–1700).
- V1-18 : Étiquette « piste 1 » minuscule (~14 px à 540 px de large, donc ~28 px à 1080) sous le minimum de 34 px de la charte, illisible sur mobile ; décor seulement, mais la charte est stricte. → Étiquette supprimée ou >= 34 px à 1080 de large.
- V1-19 : L'alerte FLASH 33.567 n'est pas un défaut : c'est l'inversion voulue (blocs noirs devenant blancs, luma moyenne de la zone timeline 175,6 → 188,7 à 33.2 → 193 à 33.5 → 205,6 à 33.83 : trois marches, 0 pixel >= 250 en aplat). Seul tic : 33.5 (198,2) / 33.533 (193,0) / 33.567 (197,0) fait un rebond d'une image, qui ressemble à un accroc de rendu plutôt qu'à une inversion franche. → Luma de la zone monotone sur 33.5–33.6 (pas de rebond > 2 unités d'une image à l'autre) ou rebond assumé par un son/une image intermédiaire.
